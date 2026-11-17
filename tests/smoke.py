"""接口冒烟测试：28 个接口全部应返回 200。

用途：改完代码、换完数据库，先跑这个确认没有哪条链路被改断。
它只回答"通不通"，不判断数据对不对 —— 数据正确性在 acceptance.py。

    python tests/smoke.py
    DJRBAC_BASE=http://127.0.0.1:8001 python tests/smoke.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _util as u  # noqa: E402

# (路径, 说明)。路径里的中文已做 URL 编码，避免控制台编码差异。
ENDPOINTS = [
    ("/api/user/", "用户列表"),
    ("/api/role/", "角色列表"),
    ("/api/permission/", "权限列表"),
    ("/api/menu/", "菜单列表"),
    ("/api/department/", "部门列表"),
    ("/api/position/", "岗位列表"),
    ("/api/employee/", "员工列表"),
    ("/api/customer_source/", "客户来源"),
    ("/api/customer/", "客户列表"),
    ("/api/customer/1/", "客户详情"),
    ("/api/customer/of_me/", "我的客户（行级隔离）"),
    ("/api/customer/?name=%E5%BC%A0", "客户-姓名模糊"),
    ("/api/customer_tracking/", "跟踪记录列表"),
    ("/api/customer_tracking/?customer_id=1", "跟踪-按客户过滤"),
    ("/api/category/", "商品分类"),
    ("/api/product/", "商品列表"),
    ("/api/sale_order/", "销售订单"),
    ("/api/sale_order/1/", "订单详情"),
    ("/api/sale_order_item/?order_id=1", "订单明细"),
    ("/api/commission/", "佣金"),
    ("/api/stat/top_sale_product/", "统计-商品排行"),
    ("/api/stat/top10_sale_employee/", "统计-员工业绩"),
    ("/api/stat/top10_province_customer/", "统计-省份客户"),
    ("/api/stat/weekday_sale_amount/", "统计-本周销售"),
    ("/api/stat/month_day_sale_amount/", "统计-月内每日"),
    ("/api/stat/year_month_sale_amount/", "统计-年度月度"),
    ("/api/stat/today_order_num_and_amount/", "统计-今日单量"),
    ("/api/common/get_spell/?words=%E5%BC%A0%E4%B8%89", "公共-拼音转换"),
]


def main() -> int:
    print(f"目标：{u.BASE}")
    if not u.PASSWORD:
        print("! 找不到登录密码：请设置环境变量 DJRBAC_PASSWORD，或在 agent-server/.env 里配置")
        return 2

    token = u.login("admin")
    if not token:
        print("! admin 登录失败，后端未就绪或账号密码不匹配")
        return 2

    u.section("接口冒烟（共 %d 个）" % len(ENDPOINTS))
    print(f"  {'#':<4}{'接口':<34}{'状态':<8}{'说明'}")
    print("  " + "-" * 62)
    for i, (path, label) in enumerate(ENDPOINTS, 1):
        status, _ = u.call(path, token=token)
        ok = status == 200
        print(f"  {i:<4}{path[:33]:<34}{status:<8}{label}")
        if not ok:
            u._failures.append(f"{label} → HTTP {status}")

    return u.summary("冒烟测试")


if __name__ == "__main__":
    sys.exit(main())
