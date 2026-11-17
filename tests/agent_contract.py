"""智能体工具层契约检查：不调模型，只验代码保证的部分。

为什么单独一个文件：
  smoke.py / acceptance.py 打的是 Django 接口，验的是"系统本身对不对"。
  这里验的是"智能体的护栏对不对"——手机模型不稳定，但这些必须有确定结论：

    1. 确认前的摘要用真实数据（客户名、等级、归属销售不能是模型编的）
    2. 客户不存在时，摘要要给出警告而不是照抄参数
    3. 查不到人时，工具要明确返回"命中数 0"，让模型有素材说"没找到"

  这三条都不经过 LLM，所以能进 CI；提示词层面的"不许编造"只能人工抽查。
"""

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parent / "agent-server"))

import _util as u  # noqa: E402

from crm.client import CrmClient  # noqa: E402
import crm.tools as tools  # noqa: E402


def main() -> int:
    token = u.login("admin")
    if not token:
        print("登录失败：请确认后端已启动、密码正确")
        return 2

    # 把"用谁的身份执行"绑给工具层（对应 server 里 runtime 做的事）
    client = CrmClient(u.BASE, "admin", "", token=token, profile={})
    tools.bind(client)

    u.section("① 确认摘要必须来自真实数据")
    summary = tools.describe_add_tracking(customer_id=1, tracking_way="电话", description="联调测试")
    fields = dict(summary.get("字段") or [])
    u.check(bool(summary.get("标题")), "摘要带标题", summary.get("标题", ""))
    u.check("客户" in fields and "ID=1" in str(fields.get("客户")), "客户字段带 ID", str(fields.get("客户")))
    # 客户 1 在种子数据里是「韩楚风」，摘要里的名字必须和接口返回一致
    status, payload = client.get_one("/api/customer/1/")
    same = status == 200 and payload.get("name") in str(fields.get("客户"))
    u.check(same, "客户名与接口一致（不是模型编的）",
            f"摘要={fields.get('客户')} / 接口={payload.get('name') if status == 200 else status}")
    u.check(bool(fields.get("归属销售")), "带归属销售", str(fields.get("归属销售")))
    u.check(bool(summary.get("提示")), "带后果说明")

    u.section("② 客户不存在时给警告，而不是照抄参数")
    missing = tools.describe_add_tracking(customer_id=99999999, tracking_way="电话", description="x")
    u.check(bool(missing.get("警告")), "缺失客户 → 有警告", str(missing.get("警告"))[:50])
    u.check("99999999" in str(missing.get("字段")), "仍然回显传入的 ID，便于人工核对")

    u.section("③ 查不到人时，工具明确返回命中 0")
    result = tools.list_customers(keyword="马云不存在的名字")
    u.check(result.get("ok") is True, "工具本身不报错")
    u.check(result.get("命中数") == 0, "命中数为 0", str(result.get("命中数")))
    u.check(bool(result.get("提示")), "带提示语（供模型转述）", str(result.get("提示")))

    return u.summary("智能体护栏契约（确认摘要 / 缺失客户 / 查无此人）")


if __name__ == "__main__":
    sys.exit(main())
