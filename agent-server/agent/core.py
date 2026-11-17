"""智能体核心：AgentSession —— 行动循环 + 危险操作确认 + 轮数保险丝。

【整个循环没有框架，就是下面这些代码】
  循环六步（对照着读 send 方法）：
    1. 把对话历史 + 工具说明书发给模型
    2. 模型要么直接回答（结束），要么提议调用工具（tool_calls）
    3. 先把"提议"作为一条 assistant 消息写回历史（协议要求配对）
    4. 普通工具：立即执行，结果以 role="tool" 回灌进对话历史
    5. 危险操作：挂起循环，把控制权交回前端等用户确认
    6. 回到第 1 步 —— 模型读到工具结果后决定下一步，直到收工（或熔断收口）

  LangChain 的 create_agent / LangGraph 的状态机，封装的就是这个循环。
  想知道框架替你做了什么，答案全在这个文件里。

【事件模型】（前端靠它渲染"工具调用过程"）
    {"type": "tool_call",    "name": ..., "args": ...}            模型提议调用工具
    {"type": "tool_result",  "name": ..., "result": ...}          工具执行完成
    {"type": "confirm",      "name": ..., "args": ...}            危险操作，等待用户确认（循环暂停）
    {"type": "answer",       "content": ...}                      最终回复（循环结束）
"""

import json
import os
from dataclasses import dataclass, field

from openai import OpenAI

from agent.registry import CONFIRM_PREVIEW, CONFIRM_REQUIRED, TOOL_DISPATCH, TOOLS

# ---------- 系统提示词（兜底占位） ----------
# 这里的循环不认识任何具体业务：客户、订单、RBAC 权限这些字眼在 agent/ 目录下
# 一个都不该出现。真正生效的业务提示词由桥接层在建立会话时注入
# （bridge.build_prompt），它会把当前登录人、部门、角色、所在页面写进 messages[0]。
# 所以这个常量只承担"没有注入时也能正常对话"的兜底作用：
# 不点名任何工具，也不假设任何业务场景。

SYSTEM_PROMPT = """你是一个接入业务系统的智能助手。

行为准则：
1. 涉及具体数据的问题，必须调用工具获取真实结果，绝不编造。
2. 只使用工具说明书里列出的工具，不要臆造工具名或参数。
3. 工具报错或提示权限不足时，如实说明；不要换个说法把没查到的数据说成查到了。
4. 工具返回空结果时，直接告诉用户"没有查到"，不要猜测。
5. 用简洁友好的中文回答，金额带货币符号 ¥。
"""

# ---------- 轮数保险丝（防死循环 / 防 token 失控） ----------
# 模型理论上可能反复调工具不收工（尤其是提示词有歧义时）。
# 到了上限不能再"劝一句继续跑"—— 那正是死循环的来源：模型不服气就会
# 继续调工具，而且每次劝都往历史里塞一条消息，越转越长。
# 正确做法是**硬熔断**：这一轮不再提供 tools，模型没有工具可调，只能回答。
MAX_ROUNDS = 10


def _assistant_msg_dict(msg) -> dict:
    """把 SDK 返回的 message 对象转成可回填 messages 的字典。

    为什么需要它：OpenAI 协议规定，role="tool" 的消息前面必须
    有一条带 tool_calls 的 assistant 消息（提议和结果要配对），
    否则 API 直接报错。这是新手最常踩的协议坑。
    """
    tool_calls = [
        {
            "id": tc.id,
            "type": "function",
            "function": {"name": tc.function.name, "arguments": tc.function.arguments},
        }
        for tc in (msg.tool_calls or [])
    ]
    return {"role": "assistant", "content": msg.content or "", "tool_calls": tool_calls}


def _usage_field(usage, *path, default: int = 0) -> int:
    """按路径从 usage 里取一个整数。兼容对象和 dict 两种形态。

    为什么需要它：OpenAI SDK 把 usage 解析成对象（Pydantic 模型），但一部分
    兼容端点（智谱、DeepSeek 的某些版本）直接返回原始 dict。同一个 openai
    库连不同厂商，拿到的形态可能不一样，硬取 .prompt_tokens 会在其中一种上炸。
    """
    current = usage
    for key in path:
        if current is None:
            return default
        current = current.get(key) if isinstance(current, dict) else getattr(current, key, None)
    return current if isinstance(current, int) else default


def new_usage() -> dict:
    """会话级用量账本。字段含义见 usage_summary() 的说明。"""
    return {
        "requests": 0,   # 向模型发起的请求次数（一次问答可能多次：每调一轮工具就多一次）
        "prompt": 0,     # 输入 token 累计（含每轮重发的历史 + 工具说明书）
        "completion": 0,  # 输出 token 累计
        "cached": 0,     # 输入里命中上下文缓存的部分（各家字段名不同，见 _record_usage）
        "cache_write": 0,  # 本次写进缓存的前缀（智谱 prompt_tokens_details.cache_write_tokens）
        "reasoning": 0,  # 思考 token（若厂商单独计）
        "log": [],       # 逐次明细，用于看"输入 token 随轮次增长"的曲线
    }


# 明细日志最多留多少条。留着是为了回答"第 20 轮比第 1 轮贵几倍"，
# 但不能无上限——一个长会话跑一天，这份日志自己就会变成内存泄漏。
USAGE_LOG_LIMIT = 100


# 用量出口：由桥接层注入 callable(payload: dict) -> None。
# 核心循环不认识 Django、不认识 HTTP、不知道调用者是谁 —— 它只负责
# "这一笔花完了，把账报出去"。目标系统怎么存、存到哪，是桥接层的事。
# 这让"换一个业务系统"不需要动这个文件一行。
USAGE_SINK = None


@dataclass
class AgentSession:
    """一个用户的会话。生产环境"一个会话一个实例"，状态外置到 Redis 后可跨进程恢复。"""

    api_key: str
    base_url: str
    model: str
    # 对话历史 = 智能体的"短期记忆"。system 提示词常驻第一条。
    messages: list = field(default_factory=lambda: [{"role": "system", "content": SYSTEM_PROMPT}])
    pending_action: dict | None = None  # 挂起的危险操作 {call_id, name, args, assistant_msg}
    # 用量账本：这一整段对话在模型上花了多少。见 _record_usage / usage_summary。
    usage: dict = field(default_factory=new_usage)
    # 上报归属：{username, session_key, employee_id}。由桥接层在建立会话时填。
    # 会话本身是按令牌哈希分桶的，换浏览器就是新会话 —— 所以"按人聚合"
    # 只能靠这里显式带上 username，不能从会话 key 反推。
    identity: dict = field(default_factory=dict)

    def __post_init__(self):
        # 用 OpenAI SDK 直连兼容模式端点（百炼/DeepSeek 都是这个协议）。
        # 没有任何框架 —— 这就是"手写"的含义。
        self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)

    def _model_kwargs(self) -> dict:
        """按厂商拼装额外的请求参数（目前只用来关掉智谱的深度思考）。

        背景：智谱（open.bigmodel.cn）的新模型默认开启深度思考——模型在输出
        工具调用之前会先 internally 推理一段。对我们这种"查数据 / 调工具"的
        标准化任务是纯浪费，实测同一个"查订单"请求：

            开思考：3.5s，思考 42 token + 输出 68 token
            关思考：1.8s，输出 24 token，工具调用结果完全一样

        思考 token 照样计费，所以关掉 = 提速一倍 + 省掉一大半输出成本。

        只对智谱端点传这个参数（换 DeepSeek / 百炼时自动不传，避免未知字段报错）。
        想保留思考过程：.env 里设 LLM_DISABLE_THINKING=false。
        """
        if "bigmodel.cn" not in (self.base_url or ""):
            return {}
        if os.getenv("LLM_DISABLE_THINKING", "true").lower() == "false":
            return {}
        return {"extra_body": {"thinking": {"type": "disabled"}}}

    # ---------- 用量计量 ----------

    def _record_usage(self, resp, round_no: int) -> None:
        """把这一次请求的 token 消耗记进账本，并打一行日志。

        【为什么这一步比任何"优化"都优先】
            没有计量就没有优化：说不清一轮对话花多少，后面每一刀省了多少
            都只能靠感觉。而且"成本优化"这类经历在面试里唯一站得住的形态
            就是数字 —— 有账本才有数字。

        【缓存字段各家不一样，这里做兼容】
            OpenAI      : prompt_tokens_details.cached_tokens
            DeepSeek    : prompt_cache_hit_tokens（命中）/ prompt_cache_miss_tokens
            智谱        : 视版本而定，取不到就记 0，不编造
        """
        usage = getattr(resp, "usage", None)
        if usage is None:  # 少数端点不返回 usage，跳过而不是报错
            return

        prompt = _usage_field(usage, "prompt_tokens")
        completion = _usage_field(usage, "completion_tokens")
        cached = _usage_field(usage, "prompt_tokens_details", "cached_tokens")
        if not cached:
            cached = _usage_field(usage, "prompt_cache_hit_tokens")
        # 缓存写入量：>0 说明"命中率 0"只是还没攒够前缀，而不是缓存压根没开
        cache_write = _usage_field(usage, "prompt_tokens_details", "cache_write_tokens")
        reasoning = _usage_field(usage, "completion_tokens_details", "reasoning_tokens")

        self.usage["requests"] += 1
        self.usage["prompt"] += prompt
        self.usage["completion"] += completion
        self.usage["cached"] += cached
        self.usage["cache_write"] += cache_write
        self.usage["reasoning"] += reasoning

        entry = {
            "seq": self.usage["requests"],
            "round": round_no,
            "prompt": prompt,
            "completion": completion,
            "cached": cached,
            "cache_write": cache_write,
            "reasoning": reasoning,
            # 记下当时历史有多长：这一列才是"上下文膨胀"的直接证据
            "messages": len(self.messages),
        }
        log = self.usage["log"]
        log.append(entry)
        if len(log) > USAGE_LOG_LIMIT:
            del log[: len(log) - USAGE_LOG_LIMIT]

        cache_note = f" 缓存命中 {cached}" if cached else ""
        write_note = f" 写缓存 {cache_write}" if cache_write else ""
        print(
            f"[usage] #{entry['seq']} 轮{round_no} "
            f"输入 {prompt}{cache_note}{write_note} 输出 {completion}"
            + (f" 思考 {reasoning}" if reasoning else "")
            + f" | 历史 {entry['messages']} 条"
            + f" | 会话累计 in={self.usage['prompt']} out={self.usage['completion']}"
        )
        self._emit_usage(round_no, prompt, completion, cached, reasoning)

    def _emit_usage(self, round_no: int, prompt: int, completion: int,
                    cached: int, reasoning: int) -> None:
        """把这一笔交给外部（目标系统的用量表）。

        失败**必须静默**：上报只是为了老板能看板，不该因为它挂了就让用户
        的对话报错。所以这里吞掉所有异常，本地账本（self.usage）仍然完整。
        """
        if USAGE_SINK is None or not self.identity.get("username"):
            return
        payload = {
            "username": self.identity.get("username"),
            "employee_id": self.identity.get("employee_id"),
            "session_key": self.identity.get("session_key") or "",
            "model": self.model,
            "round_no": round_no,
            "prompt_tokens": prompt,
            "completion_tokens": completion,
            "cached_tokens": cached,
            "reasoning_tokens": reasoning,
        }
        try:
            USAGE_SINK(payload)
        except Exception:  # noqa: BLE001  上报失败不影响对话
            pass

    def usage_summary(self) -> dict:
        """本会话的用量结论。给接口/前端读取，也方便人工看一眼。

        【返回的三个派生指标，是"成本是否失控"的判断题】
            cache_hit_rate  缓存命中率：固定开销（工具说明书 + 系统提示词）
                            每轮都重发，命中缓存的部分按折扣价计费。命中率长期
                            为 0，说明前缀在变（时间戳、登录人信息插在前面等），
                            白白全价重发。
            input_growth    最后一次 ÷ 第一次的输入 token。>1 就是历史在膨胀；
                            20 轮后这个数很可能是 10 倍以上 —— 那才是真正的账单。
            avg_prompt      平均每次请求的输入。乘上请求数就是总输入，可以直接
                            对照字符数估算验证。
        """
        log = self.usage["log"]
        prompt_total = self.usage["prompt"]
        summary = {
            "请求次数": self.usage["requests"],
            "输入token": prompt_total,
            "输出token": self.usage["completion"],
            "总token": prompt_total + self.usage["completion"],
            "缓存命中token": self.usage["cached"],
            "缓存写入token": self.usage["cache_write"],
            "思考token": self.usage["reasoning"],
            "当前历史条数": len(self.messages),
        }
        if log:
            first, last = log[0]["prompt"], log[-1]["prompt"]
            summary["平均输入"] = round(prompt_total / len(log), 1)
            summary["输入增长倍数"] = round(last / first, 2) if first else 0
            summary["缓存命中率"] = f"{(self.usage['cached'] / prompt_total * 100):.1f}%" if prompt_total else "0.0%"
        return summary

    # ---------- 主入口 ----------

    def send(self, user_text: str | None = None) -> list[dict]:
        """处理一轮对话（可带用户输入），返回事件列表。

        user_text=None 的场景：confirm() 之后继续跑循环用 ——
        用户确认/拒绝本身不是新的用户消息，只是"补发"工具结果。
        """
        events: list[dict] = []
        if user_text:
            self.messages.append({"role": "user", "content": user_text})

        rounds = 0
        while True:
            rounds += 1
            if rounds > MAX_ROUNDS:  # 保险丝熔断：不再给工具，逼模型收口
                return self._force_answer(events)

            # 第 1 步：带着全部历史 + 工具说明书请求模型
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                tools=TOOLS,          # 工具说明书随请求带上，模型每次都"看得到"
                tool_choice="auto",   # 自动：模型自己决定调不调工具
                **self._model_kwargs(),  # 厂商特有参数（目前=关掉智谱深度思考）
            )
            msg = resp.choices[0].message
            self._record_usage(resp, rounds)

            # 第 2 步：没有工具调用 = 模型认为任务完成，循环退出
            if not msg.tool_calls:
                answer = msg.content or "（无回复）"
                events.append({"type": "answer", "content": answer})
                self.messages.append({"role": "assistant", "content": answer})
                return events

            # 第 3 步：先补"提议"这一次，再逐个回灌结果
            # 一条 assistant 消息可能带多个 tool_calls，而 OpenAI 协议要求
            # 「一条提议 : N 条结果」配对，所以提议只能在循环外追加一次。
            # 放在循环里追加 2 个调用就写 2 条 assistant，严格校验的厂商会 400。
            self.messages.append(_assistant_msg_dict(msg))

            # 第 4 步：逐个处理模型提议的工具调用
            for index, call in enumerate(msg.tool_calls):
                name = call.function.name
                try:
                    # 模型返回的参数是 JSON 字符串，需要解析
                    args = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    args = {}  # 参数解析失败也回灌错误，让模型自己纠错重试

                events.append({"type": "tool_call", "name": name, "args": args})

                # 第 5 步：危险操作 → 挂起，把控制权交回前端
                if name in CONFIRM_REQUIRED:
                    # 排在后面的调用这一轮不执行，但它们的 id 必须补"结果"，
                    # 否则会出现"声明了 3 个调用、只回了 1 条结果"的协议缺口。
                    self.pending_action = {
                        "call_id": call.id,
                        "name": name,
                        "args": args,
                        "skipped_ids": [c.id for c in msg.tool_calls[index + 1:]],
                    }
                    events.append({
                        "type": "confirm",
                        "name": name,
                        "args": args,
                        # 预检摘要：用真实数据说清"这一下会发生什么"，
                        # 由代码算，不让模型描述后果（它会编客户名/金额）
                        "summary": self._preview(name, args),
                    })
                    return events  # 循环在这里暂停 —— 这就是"人留在决策环里"

                # 第 6 步：普通工具 → 立即执行，结果回灌
                result = self._execute(name, args)
                events.append({"type": "tool_result", "name": name, "result": result})
                self.messages.append(
                    {"role": "tool", "tool_call_id": call.id, "content": json.dumps(result, ensure_ascii=False)}
                )

    @staticmethod
    def _execute(name: str, args: dict) -> dict:
        """执行一个工具，任何失败都转换成"工具结果"而不是抛异常。

        模型编造工具名（不在注册表里）是常见现象，直接 TOOL_DISPATCH[name]
        会抛 KeyError，把整轮对话打断；返回结构化错误则能让它自己改正。
        """
        tool = TOOL_DISPATCH.get(name)
        if tool is None:
            return {
                "ok": False,
                "原因": f"没有名为 {name} 的工具，请从工具说明书里选择已注册的工具后重试",
            }
        return tool(**(args or {}))

    @staticmethod
    def _preview(name: str, args: dict) -> dict | None:
        """确认框里的"人话摘要"：执行前用真实数据查一遍，说清会发生什么。

        失败一律返回 None —— 摘要只是锦上添花，不能因为查详情失败
        就把用户卡在"点不了确认"的状态里。
        """
        fn = CONFIRM_PREVIEW.get(name)
        if fn is None:
            return None
        try:
            return fn(**(args or {}))
        except Exception:  # noqa: BLE001  摘要算不出来就退化成只显示参数
            return None

    def _force_answer(self, events: list[dict]) -> list[dict]:
        """熔断收口：不带 tools 再请求一次，模型没有工具可调，只能给结论。

        提示语用局部副本发送，不写回 self.messages ——
        否则每熔断一次就在历史里留一条系统提示，下一轮接着误导模型。
        """
        hint = {
            "role": "user",
            "content": "（系统提示：工具调用已达轮数上限，请基于已获取的信息直接回答用户，不要再调用工具）",
        }
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[*self.messages, hint],
                **self._model_kwargs(),
            )
            answer = resp.choices[0].message.content or "（已达工具调用轮数上限，未能得出结论）"
            # 熔断收口也是一次真实计费的请求（虽然不带工具说明书），照样记账
            self._record_usage(resp, MAX_ROUNDS + 1)
        except Exception as exc:  # noqa: BLE001  收口本身失败也不能让接口 500
            answer = f"（已达工具调用轮数上限，收口时请求模型失败：{exc}）"
        events.append({"type": "answer", "content": answer})
        self.messages.append({"role": "assistant", "content": answer})
        return events

    # ---------- 危险操作确认 ----------

    def confirm(self, yes: bool) -> list[dict]:
        """用户对挂起操作表态后，把结果回灌给模型并继续循环。

        整个流程：send 挂起 → 前端弹按钮 → 用户点击 → confirm 补发
        tool 结果 → 继续 send 直到最终回答。这对应 LangGraph 的
        interrupt / human-in-the-loop 机制，只不过这里循环在我们
        手里，想停就停，不需要框架支持。
        """
        pa = self.pending_action
        if pa is None:
            return []
        self.pending_action = None

        # 注意：带 tool_calls 的 assistant 消息在 send() 挂起之前就已经追加过了，
        # 这里不能再补一次 —— 补两次就是"一条提议、两条提议"，协议不合法。
        if yes:
            result = self._execute(pa["name"], pa["args"])
        else:
            # 拒绝也是一种"工具结果"——模型读到后会改口告知用户，而不是卡死
            result = {"ok": False, "reason": "用户拒绝了本次操作"}
        content = json.dumps(result, ensure_ascii=False)
        events = [{"type": "tool_result", "name": pa["name"], "result": result}]
        self.messages.append({"role": "tool", "tool_call_id": pa["call_id"], "content": content})

        # 同一轮里被跳过的其他调用也要有结果，保证每个 tool_call_id 都有配对
        for skipped_id in pa.get("skipped_ids") or []:
            self.messages.append({
                "role": "tool",
                "tool_call_id": skipped_id,
                "content": json.dumps(
                    {"ok": False, "reason": "本轮未执行：同一轮里的多个操作需逐个确认，请重新发起这一项"},
                    ensure_ascii=False,
                ),
            })

        events.extend(self.send(None))  # 继续循环，直到最终回答
        return events
