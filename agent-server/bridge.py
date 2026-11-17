"""桥接层：把通用智能体循环接到 dj-rbac 的 CRM 工具上。

【关键决定：不重写循环，只换工具】
    agent/core.py 里的 AgentSession 是这套智能体的循环本体（两百来行），
    这里一行逻辑都没有重写，而是 import 进来用，然后替换掉三个模块级变量：

        core.TOOLS            → CRM 工具说明书
        core.TOOL_DISPATCH    → CRM 工具的真实执行函数
        core.CONFIRM_REQUIRED → 哪些写操作要人工确认

    这样"同一套循环、换一套工具、换一个业务系统"就成立了 ——
    这正是工具可插拔的意义，也是这个项目想验证的事：
    智能体的能力边界不在循环里，在工具层。

【为什么循环和工具分开放】
    agent/ 只放与业务无关的通用能力（循环、注册表），crm/ 只放 CRM 工具。
    agent/registry.py 默认是空注册表，由这个文件在启动时注入 ——
    所以 core.py 里找不到"客户""订单"这类字眼，它不认识任何业务。
"""

import hashlib
import json
import time
import urllib.error
import urllib.request
from datetime import date

import agent.core as core  # noqa: E402  手写智能体循环

from config import (  # noqa: E402
    ALLOW_USER_LOGIN,
    DEMO_PASSWORD,
    DJRBAC_BASE,
    INTERNAL_API_KEY,
    LLM_DAILY_BUDGET_TOKENS,
    LLMConfig,
    MAX_SESSIONS,
    REPORT_TIMEOUT,
    SESSION_TTL,
)
from crm.client import CrmClient  # noqa: E402
from crm.tools import CONFIRM_PREVIEW, CONFIRM_REQUIRED, TOOL_DISPATCH, TOOLS  # noqa: E402


class BudgetExceeded(Exception):
    """当日 token 预算用尽。故意用独立异常类型：

    如果混在通用异常里，上层只能一律回 500，用户看到的是"服务器出错"，
    实际却是"你今天额度用完了" —— 这两种情况该给完全不同的提示。
    """


# 预算状态的本地缓存有效期。真值以目标系统的用量表为准，
# 这里只是避免"每次对话都查一次库"，60 秒的偏差可以接受。
BUDGET_CACHE_TTL = 60


def _guard(fn):
    """给每个工具套一层兜底：工具抛异常不能让整个循环崩掉。

    模型经常会传错参数（少字段、类型不对）。如果让异常直接冒出去，
    整轮对话就中断了。这里把异常转成正常的工具结果回灌给模型，
    让它自己纠错重试 —— 这是"让智能体自愈"最便宜的一种做法。
    """

    def runner(**kwargs):
        try:
            return fn(**(kwargs or {}))
        except TypeError as exc:
            return {"ok": False, "原因": f"参数不匹配：{exc}，请检查字段名和类型后重试"}
        except Exception as exc:  # noqa: BLE001
            return {"ok": False, "原因": f"工具执行异常：{exc}"}

    runner.__name__ = getattr(fn, "__name__", "tool")
    return runner


# ---------- 注入：把 agent.core 的全局表换成 CRM 的 ----------
core.TOOLS = TOOLS
core.TOOL_DISPATCH = {name: _guard(fn) for name, fn in TOOL_DISPATCH.items()}
core.CONFIRM_REQUIRED = CONFIRM_REQUIRED
core.CONFIRM_PREVIEW = CONFIRM_PREVIEW

SYSTEM_PROMPT_TEMPLATE = """你是「CRM 销售助手」，接在一套 RBAC 客户管理系统（Django + DRF）前面，
能查客户、查订单、查跟踪记录、看销售统计，也能帮用户补一条跟踪记录。

当前登录人：{who}
今天是：{today}

行为准则：
1. 涉及客户、订单、统计、跟踪记录的问题，必须先调用工具取真实数据，绝不编造数字。
2. 不知道客户ID/订单ID时，先用 list_customers 或 list_orders 查出 ID，再用 get_customer / get_order 看详情。
3. 用户问「我的客户」用 my_customers；问「全部客户」或按条件筛用 list_customers。
4. 工具返回权限不足（403）时，如实说明当前账号没有这个权限，并建议改用 my_customers 查本人数据；
   绝对不要猜数据、也不要换个说法把没查到的数据说成查到了。
5. 工具返回「没有查到」就直说没有，不要推测。
6. 金额用 ¥ 表示并保留两位小数。结果超过 5 条时先给一句汇总，再列出关键几条。
7. 用户要求「记录一下 / 写一条跟踪 / 备注」时，调用 add_tracking（系统会弹确认框，等用户点）。
8. 不要凭常识回答公司业务规则（提成比例、退货政策等）。数据里没有的，就说系统里没有这项信息。
9. 查不到人、查不到单时（例如用户问「查一下马云」），明确回答「系统里没有找到相关记录」，
   并建议他核对姓名/手机号拼写，或到左侧对应页面手动搜索一次；
   不要用名字相近的客户顶替，也不要给「大概是」这类模糊答案。
10. 用户说「这个客户」「当前订单」，但上下文里没有具体记录（比如他停在列表页）时，
    先反问是哪一个，不要猜。
"""


def build_prompt(profile: dict) -> str:
    employee = profile.get("employee") or {}
    parts = [profile.get("username") or "未知"]
    if employee.get("name"):
        parts.append(f"员工 {employee['name']}")
    if (employee.get("department") or {}).get("name"):
        parts.append(f"部门 {employee['department']['name']}")
    roles = [r.get("name") for r in (profile.get("role") or []) if r.get("name")]
    if roles:
        parts.append("角色 " + "/".join(roles))
    if profile.get("is_superuser"):
        parts.append("超级管理员")
    return SYSTEM_PROMPT_TEMPLATE.format(who="｜".join(parts), today=date.today().isoformat())


class AgentRuntime:
    """管理"每个登录用户一个会话"。

    一个会话 = 一个人 + 一段对话历史 + 他自己的 JWT。
    换人就是换会话，工具上下文跟着换，权限自然跟着换。
    """

    def __init__(self):
        self.llm = LLMConfig()
        self.sessions: dict[str, core.AgentSession] = {}
        # 账号 → (今日已用 token, 记录时刻)。只做预算判断，不是账本本身。
        self._budget: dict[str, tuple[int, float]] = {}
        self._report_failures = 0
        # 把用量出口接到这个实例上。核心循环只管把账交出来，
        # 存到哪、失败怎么办，都由这里决定。
        core.USAGE_SINK = self._report_usage

    def ready(self) -> bool:
        return self.llm.ready

    # ---------- 会话管理 ----------

    @staticmethod
    def _key(username: str | None, token: str | None) -> str:
        # 令牌模式下一个令牌就是一个身份；账号模式下一人一会话
        if token:
            return "tk:" + hashlib.sha1(token.encode("utf-8")).hexdigest()[:16]
        return "pw:" + (username or "")

    def _evict(self, now: float) -> None:
        """回收会话，两条规则：

        1. 空闲超过 SESSION_TTL 秒的直接丢弃；
        2. 还超上限时，按最久未使用淘汰到 MAX_SESSIONS 以内。

        为什么必须有：key 是令牌的 sha1，重新登录就是一个新令牌 = 新 key，
        旧会话永远不会再被访问到，不回收就是纯内存泄漏；长时间运行时
        每个会话还攥着一整段对话历史 + 一个 HTTP 客户端。
        """
        for key, session in list(self.sessions.items()):
            if now - getattr(session, "last_active", now) > SESSION_TTL:
                self.sessions.pop(key, None)
        overflow = len(self.sessions) - MAX_SESSIONS
        if overflow > 0:
            ordered = sorted(
                self.sessions.items(), key=lambda kv: getattr(kv[1], "last_active", 0.0)
            )
            for key, _ in ordered[:overflow]:
                self.sessions.pop(key, None)

    # ---------- 用量上报与预算 ----------

    def _report_usage(self, payload: dict) -> None:
        """把一次请求的用量 POST 给目标系统。

        为什么不重要到可以随便失败：对话是主线，看板是旁路。
        上报挂了最多是老板看不到数字，不能让用户连问题都问不了。
        但也不能一声不吭 —— 前几次失败会打日志，否则"看板空了"
        会被误当成"今天没人用"。
        """
        if not INTERNAL_API_KEY:
            return
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            DJRBAC_BASE + "/api/llm_usage/report/", data=body, method="POST"
        )
        req.add_header("Content-Type", "application/json")
        req.add_header("X-Internal-Key", INTERNAL_API_KEY)
        try:
            with urllib.request.urlopen(req, timeout=REPORT_TIMEOUT) as resp:
                data = json.loads(resp.read() or b"{}")
        except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
            self._report_failures += 1
            # 只在第 1/10/100 次提示，避免日志被网络问题刷爆
            if self._report_failures in (1, 10, 100):
                print(f"[usage] 上报失败（累计 {self._report_failures} 次）：{exc}")
            return

        self._report_failures = 0
        # 上报接口顺带回了该账号今日累计，直接拿来更新预算状态，
        # 省掉一次单独的查询 —— 记账和取数一次往返完成。
        used = int(data.get("today_prompt", 0)) + int(data.get("today_completion", 0))
        self._budget[payload["username"]] = (used, time.time())

    def _check_budget(self, username: str) -> None:
        """对话开始前看一眼今天还剩多少。

        注意这是"事后拦"：第一次请求时本地还没有数据，所以会放过去，
        要等上报回来才知道超了。真正的硬闸门应该在上报接口里拒绝写入，
        这里只是让用户在下一轮就知道停 —— demo 够用，生产要两边一起做。
        """
        if LLM_DAILY_BUDGET_TOKENS <= 0 or not username:
            return
        used, at = self._budget.get(username, (0, 0.0))
        if time.time() - at > BUDGET_CACHE_TTL:
            return  # 缓存过期就当不知道，别拿旧数据拦人
        if used >= LLM_DAILY_BUDGET_TOKENS:
            raise BudgetExceeded(
                f"今日 token 额度已用完（已用 {used} / 上限 {LLM_DAILY_BUDGET_TOKENS}），"
                "明天再试，或让管理员调高 LLM_DAILY_BUDGET_TOKENS"
            )

    def _whoami(self, token: str) -> dict | None:
        """凭令牌问后端"我是谁"。失败返回 None，绝不抛异常。

        为什么必须问而不是从请求体里读用户名：用量是要记到人头上的账。
        如果用户名由前端自报，员工 A 就能把自己的消耗记到 B 头上，
        看板立刻变成一份谁都不信的数据。
        """
        req = urllib.request.Request(DJRBAC_BASE + "/api/user/whoami/")
        req.add_header("Authorization", "Bearer " + token)
        try:
            with urllib.request.urlopen(req, timeout=REPORT_TIMEOUT) as resp:
                return json.loads(resp.read() or b"{}")
        except (urllib.error.URLError, TimeoutError, OSError, ValueError):
            return None

    def _client_for(self, username, token, profile):
        if token:
            name = username or (profile or {}).get("username")
            if not name:
                me = self._whoami(token) or {}
                name = me.get("username")
                # 顺手把 profile 补全：系统提示词里的"员工/部门"要靠它，
                # 而登录接口返回的 employee 没有 department 字段。
                if me and not profile:
                    profile = {
                        "username": name,
                        "employee": me.get("employee"),
                        "is_superuser": me.get("is_superuser"),
                    }
            name = name or "unknown"
            # 前端已经把登录令牌送过来了，这里不再重新登录：
            # 智能体的身份 = 当前坐在电脑前的那个人
            return CrmClient(DJRBAC_BASE, name, "", token=token, profile=profile or {})
        if not ALLOW_USER_LOGIN:
            # 兜底：正常请求在 server 层就被拦掉了，走到这里说明有人绕过了校验。
            # 绝不能用服务端的公共密码替对方登录 —— 那等于匿名获得任意账号的读取权。
            raise PermissionError("缺少登录令牌：请在后台管理系统中使用，或配置 AGENT_ALLOW_USER_LOGIN=true 后使用独立页面")
        client = CrmClient(DJRBAC_BASE, username or "", DEMO_PASSWORD)
        client.login()  # 失败会抛 ApiError，由 server 层转成友好提示
        return client

    def _get_session(self, username=None, token=None, profile=None) -> core.AgentSession:
        now = time.time()
        self._evict(now)
        key = self._key(username, token)
        session = self.sessions.get(key)
        if session is not None:
            session.last_active = now
            return session

        client = self._client_for(username, token, profile)
        session = core.AgentSession(
            api_key=self.llm.api_key,
            base_url=self.llm.base_url,
            model=self.llm.model,
        )
        base_prompt = build_prompt(client.profile or {"username": client.username})
        session.messages[0]["content"] = base_prompt
        session.base_prompt = base_prompt
        session.crm_client = client
        # 上报归属写死在会话上：核心循环不认识"用户"，只有这里知道
        employee = (client.profile or {}).get("employee") or {}
        session.identity = {
            "username": client.username,
            "session_key": key,
            "employee_id": employee.get("id") if isinstance(employee, dict) else None,
        }
        session.last_active = now
        self.sessions[key] = session
        return session

    @staticmethod
    def _apply_page_context(session, page_name: str | None, focus: dict | None = None):
        """把"用户现在在哪个模块、在看哪条记录"写进系统提示。

        这是嵌进后台管理才有的好处：智能体知道你在看客户页还是订单页，
        甚至知道你正打开着哪个客户的详情。独立页面拿不到这个上下文，
        只能靠用户自己把 ID 说出来。
        """
        base = getattr(session, "base_prompt", session.messages[0]["content"])
        if not page_name and not focus:
            session.messages[0]["content"] = base
            return

        lines = [base, ""]
        if page_name:
            lines.append(f"当前界面上下文：用户正停留在「{page_name}」页面。")
        if focus and focus.get("id"):
            kind = focus.get("type") or "记录"
            fid = focus.get("id")
            lines.append(
                f"用户当前打开的是{kind} ID={fid} 的详情页。"
                f"用户说「这个{kind}」「当前{kind}」时，指的就是 ID={fid}；"
                f"可直接用 get_customer / get_order 等工具按这个 ID 查询，不必再反问。"
            )
        lines.append(
            "如果用户用「这个/当前」指代某条数据，优先理解为当前页面对应的业务对象。"
        )
        session.messages[0]["content"] = "\n".join(lines)

    def reset(self, username=None, token=None):
        session = self.sessions.get(self._key(username, token))
        if session is not None:
            # 清空对话前先把这段对话的账单打出来 —— 否则"这一轮聊了多少钱"
            # 就随 reset 一起消失了，而这正是最该被看见的数字。
            if session.usage.get("requests"):
                s = session.usage_summary()
                print(
                    f"[usage] 会话重置，本段共 {s['请求次数']} 次请求 "
                    f"in={s['输入token']} out={s['输出token']} "
                    f"缓存={s['缓存命中token']} 输入增长={s.get('输入增长倍数', 0)}x"
                )
                session.usage = core.new_usage()
            session.messages = session.messages[:1]
            session.pending_action = None
            session.last_active = time.time()

    def usage(self, username=None, token=None) -> dict:
        """查当前会话的用量。只读，不新建会话（新建会去打目标系统接口）。"""
        session = self.sessions.get(self._key(username, token))
        if session is None:
            return {"会话": "不存在或已过期（没有任何对话记录）"}
        return session.usage_summary()

    # ---------- 入口 ----------

    def chat(self, text: str, *, username=None, token=None, profile=None,
             page_name=None, focus=None) -> list[dict]:
        from crm.tools import bind

        session = self._get_session(username, token, profile)
        self._apply_page_context(session, page_name, focus)
        self._check_budget(session.identity.get("username") or "")
        bind(session.crm_client)  # 把"用谁的身份执行"绑到当前线程
        return session.send(text)

    def confirm(self, yes: bool, *, username=None, token=None, profile=None,
                page_name=None, focus=None) -> list[dict]:
        from crm.tools import bind

        session = self._get_session(username, token, profile)
        self._apply_page_context(session, page_name, focus)
        # confirm() 不查预算：用户已经点过"确认"，这时候拦住等于让一次
        # 已获批的写操作烂在半路，比多花一次请求更糟。
        bind(session.crm_client)
        return session.confirm(yes)
