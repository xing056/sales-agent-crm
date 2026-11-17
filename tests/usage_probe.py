"""Token 用量探针：量一次问答到底花多少 token、缓存命中多少。

【为什么单独一个脚本，而且不进 CI】
    smoke / acceptance / agent_contract 都是"对错题"，能挂 CI。
    这个是"测量"，跑一次要真花几厘钱，而且结果依赖模型厂商当天的行为
    （缓存粒度、是否命中），不适合当断言 —— 今天命中 1024、明天可能 0，
    那不是回归，是厂商侧的正常波动。

    【它不需要 Django 跑起来】
        工具执行用了可控的假数据，但**工具说明书是真的**（直接读
        crm/tools.py 的 TOOLS），系统提示词、历史累积、缓存前缀全都真实。
        所以量出来的输入 token 和线上一致，只有工具返回体的内容不同。

    用法：
        cd agent-server 同级目录
        ./backend/.venv/Scripts/python.exe tests/usage_probe.py
     或在 agent-server 下：
        ./.venv/Scripts/python.exe ../tests/usage_probe.py

    注意：要用 **agent-server 的环境**（它装了 openai），backend 的 venv 跑不了。

    想对比"少返回几条能省多少"：
        ./.venv/Scripts/python.exe ../tests/usage_probe.py --rows 20
        ./.venv/Scripts/python.exe ../tests/usage_probe.py --rows 5

【它回答什么问题】
    1. 一次"查列表"的问答要发几次请求？各多少 token？
    2. 固定开销（系统提示词 + 工具说明书）占输入多少？
    3. 上下文缓存到底有没有命中？命中多少？
    4. 第 2 次请求比第 1 次贵几倍（这就是"历史膨胀"的直接证据）。
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
AGENT_DIR = HERE.parent / "agent-server"
sys.path.insert(0, str(AGENT_DIR))

# core.py 里读环境变量控制思考开关，探针跟着 .env 走（由 config 负责同步）
import agent.core as core  # noqa: E402
import crm.tools as tools  # noqa: E402
from config import LLMConfig  # noqa: E402

SYSTEM_PROMPT = "你是 CRM 助手。查数据必须调用工具，不要编造。"
QUESTION = "帮我查一下全部客户，列出前几个"


def _fake_rows(n: int = 20) -> list[dict]:
    """造 n 条客户，字段与真实 _slim_customer 完全一致，保证体量可比。"""
    return [
        tools._slim_customer({
            "id": i,
            "name": f"客户{i}",
            "phone": f"138000000{i:02d}",
            "level": 1,
            "order_count": 2,
            "order_amount": "1200.00",
            "province": "广东省",
            "city": "深圳市",
            "county": "南山区",
            "address": "x",
            "user": {"name": "张三"},
            "source": {"name": "门店"},
            "status": 1,
        })
        for i in range(1, n + 1)
    ]


def _install_fake_tools(n_rows: int) -> None:
    """装上真实说明书 + 假执行结果。改的是模块级插槽，不动 crm/tools.py 本身。"""
    rows = _fake_rows(n_rows)
    core.TOOLS = tools.TOOLS
    core.CONFIRM_REQUIRED = tools.CONFIRM_REQUIRED
    core.CONFIRM_PREVIEW = tools.CONFIRM_PREVIEW
    core.TOOL_DISPATCH = {
        "list_customers": lambda **kw: {
            "ok": True,
            "全库客户数": 136,
            "命中数": 136,
            "返回": rows,
            "提示": f"共命中 136 条，只返回前 {len(rows)} 条，可加条件缩小范围",
        },
        "my_customers": lambda **kw: {"ok": True, "命中数": len(rows), "返回": rows[:5]},
    }


def run_once(cfg, label: str) -> dict:
    """跑一段完整对话，返回用量汇总。"""
    session = core.AgentSession(api_key=cfg.api_key, base_url=cfg.base_url, model=cfg.model)
    session.messages[0]["content"] = SYSTEM_PROMPT
    print(f"\n--- {label} ---")
    session.send(QUESTION)
    s = session.usage_summary()
    print(f"  该段汇总：请求 {s['请求次数']} 次 / 输入 {s['输入token']} / 输出 {s['输出token']}"
          f" / 缓存命中 {s['缓存命中token']}（{s.get('缓存命中率', '0%')}）")
    return s


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser(description="量一次问答的 token 消耗")
    parser.add_argument("--rows", type=int, default=20,
                        help="列表工具返回多少条（默认 20，与线上 limit 一致；传 5 可对比'收窄返回'省多少）")
    args = parser.parse_args()

    cfg = LLMConfig()
    if not cfg.ready:
        print("模型未配置：请先按 README 复制 agent-server/.env.example 为 .env 并填 LLM_API_KEY")
        return 2

    print("=" * 62)
    print("Token 用量探针")
    print(f"  模型：{cfg.model} @ {cfg.base_url}")
    print(f"  工具：{len(tools.TOOLS)} 个，说明书 {len(__import__('json').dumps(tools.TOOLS, ensure_ascii=False))} 字符")
    print(f"  列表返回：{args.rows} 条")
    print("=" * 62)

    _install_fake_tools(args.rows)

    first = run_once(cfg, "第 1 段对话（前缀冷启动）")
    second = run_once(cfg, "第 2 段对话（同前缀，看缓存是否复用）")

    print("\n" + "-" * 62)
    print("结论")
    print(f"  单段问答输入 token：{first['输入token']}")
    print(f"  输入增长倍数：{first.get('输入增长倍数', 0)}x（第 2 次请求 ÷ 第 1 次）")
    print(f"  缓存命中：{first['缓存命中token']} / {first['输入token']}")
    print(f"  缓存写入：{first['缓存写入token']}")
    if not second["缓存命中token"]:
        print("  → 两段对话的命中情况不一致：缓存是「段内生效、跨段不保证」")
    return 0


if __name__ == "__main__":
    sys.exit(main())
