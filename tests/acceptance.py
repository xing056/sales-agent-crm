"""业务验收：权限、金额精度、中文编码、关联完整性。

和 smoke.py 的区别：smoke 只看"接口通不通"，这个看"行为对不对"。
每一条都是断言，失败会让进程退出码变成 1 —— 可以挂进 CI 或一键启动脚本。

    python tests/acceptance.py

判据全部来自真实接口返回，不读数据库、不看代码，黑盒验收。
"""

import re
import sys
from decimal import Decimal
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import _util as u  # noqa: E402

# 金额必须是"字符串 + 两位小数"。只要出现一段 float，精度链路就已经破了。
MONEY_RE = re.compile(r"^\d+\.\d{2}$")


def section_permission():
    """① 行级隔离：普通销售只能看自己的客户，无权限账号直接 403。"""
    u.section("① 行级数据隔离")

    admin = u.login("admin")
    user001 = u.login("user001")
    zhengping = u.login("zhengping")
    if not (admin and user001 and zhengping):
        u.check(False, "三个演示账号都能登录")
        return {}

    st_a, d_a = u.call("/api/customer/", token=admin)
    st_u, d_u = u.call("/api/customer/", token=user001)
    st_z, d_z = u.call("/api/customer/", token=zhengping)

    u.check(st_a == 200, "admin 可查全部客户", f"HTTP {st_a}")
    u.check(st_u == 403, "user001 查全部客户被拒（403）", f"实际 HTTP {st_u}")
    u.check(st_z == 403, "zhengping 查客户被拒（403）", f"实际 HTTP {st_z}")

    st_me, d_me = u.call("/api/customer/of_me/", token=user001)
    all_count = u.count_of(d_a) or 0
    my_count = u.count_of(d_me) or 0
    u.check(st_me == 200, "user001 可查自己的客户", f"HTTP {st_me}")
    u.check(
        0 < my_count < all_count,
        "「我的客户」是全部客户的真子集",
        f"我的 {my_count} / 全部 {all_count}",
    )
    return {"admin": admin, "user001": user001, "all": all_count, "mine": my_count}


def section_money(tokens):
    """② 金额精度：接口里不能出现 float，金额字段必须是两位小数字符串。"""
    u.section("② 金额精度（float 是这类系统的头号敌人）")
    token = tokens.get("admin") or u.login("admin")
    if not token:
        u.check(False, "拿到 admin 令牌")
        return

    targets = [
        "/api/customer/?page=1&size=100",
        "/api/customer/1/",
        "/api/sale_order/?page=1&size=100",
        "/api/sale_order/1/",
        "/api/stat/year_month_sale_amount/",
        "/api/stat/today_order_num_and_amount/",
        "/api/commission/",
    ]

    float_paths = []
    bad_shape = []
    for path in targets:
        status, payload = u.call(path, token=token)
        if status != 200:
            u.check(False, f"{path} 可访问", f"HTTP {status}")
            continue
        float_paths += u.find_floats(payload, path)

        # 递归检查所有 *_amount / amount 字段的形态
        def walk(obj):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    if isinstance(v, str) and ("amount" in k or k == "amount"):
                        if v and not MONEY_RE.match(v):
                            bad_shape.append(f"{path} · {k}={v!r}")
                    walk(v)
            elif isinstance(obj, list):
                for item in obj:
                    walk(item)

        walk(payload)

    u.check(not float_paths, "所有接口的金额都是字符串，没有一个 float",
            "、".join(float_paths[:3]) if float_paths else "扫描 %d 个接口" % len(targets))
    u.check(not bad_shape, "金额字段都是两位小数格式（如 13200.00）",
            "、".join(bad_shape[:3]) if bad_shape else "")


def section_chinese(tokens):
    """③ 中文编码：曾经被 GBK 误读过一次，这个断言就是防复发。"""
    u.section("③ 中文编码完整性")
    token = tokens.get("admin") or u.login("admin")
    status, payload = u.call("/api/customer/?page=1&size=20", token=token)
    if status != 200:
        u.check(False, "客户列表可访问", f"HTTP {status}")
        return

    rows = payload.get("results") or payload
    names = [r.get("name") or "" for r in rows]
    mojibake = [n for n in names if "\ufffd" in n or "?" in n]
    u.check(bool(names), "取到客户数据", f"{len(names)} 条")
    u.check(not mojibake, "客户姓名没有乱码（无 U+FFFD / ?）",
            "、".join(mojibake[:3]) if mojibake else f"抽检 {len(names)} 条")

    first = rows[0] if rows else {}
    st, detail = u.call(f"/api/customer/{first.get('id')}/", token=token)
    same = st == 200 and detail.get("name") == first.get("name")
    u.check(same, "列表与详情的姓名一致", f"{first.get('name')} vs {detail.get('name')}")


def section_integrity(tokens):
    """④ 关联完整性：订单/跟踪记录都要能指到存在的客户，不能有孤儿数据。"""
    u.section("④ 关联完整性（孤儿数据）")
    token = tokens.get("admin") or u.login("admin")

    st, orders = u.call("/api/sale_order/?page=1&size=100", token=token)
    if st == 200:
        rows = orders.get("results") or orders
        orphan = [o.get("order_no") for o in rows if not (o.get("customer") or {}).get("id")]
        u.check(bool(rows), "取到订单数据", f"{len(rows)} 条")
        u.check(not orphan, "每笔订单都能指到客户（无孤儿）",
                "、".join(map(str, orphan[:3])) if orphan else "")
    else:
        u.check(False, "订单列表可访问", f"HTTP {st}")

    st, tracks = u.call("/api/customer_tracking/?page=1&size=100", token=token)
    if st == 200:
        rows = tracks.get("results") or tracks
        orphan = [t.get("id") for t in rows if not (t.get("customer") or {}).get("id")]
        u.check(not orphan, "每条跟踪记录都能指到客户（无孤儿）",
                "、".join(map(str, orphan[:3])) if orphan else f"抽检 {len(rows)} 条")
    else:
        u.check(False, "跟踪记录可访问", f"HTTP {st}")

    # 订单金额必须等于明细行"数量 × 单价"之和。
    # 这是整个系统里最容易出精度问题的地方，所以用 Decimal 精确比较，不留容差。
    #
    # 注意：SaleOrderViewSet 目前没有配 filterset_fields，`?customer_id=` 之类的
    # 过滤参数会被忽略并返回全部数据。所以这里一律取回列表后自己比对，
    # 不要相信"传了参数就等于过滤了"。
    st, orders = u.call("/api/sale_order/?page=1&size=100", token=token)
    if st == 200:
        rows = orders.get("results") or orders
        checked = 0
        mismatched = []
        for row in rows:
            oid = row.get("id")
            sti, items = u.call(f"/api/sale_order_item/?order_id={oid}", token=token)
            if sti != 200:
                continue
            lines = items.get("results") if isinstance(items, dict) else items
            if not lines:
                continue  # 这笔订单没录入明细，跳过
            total = sum(
                (Decimal(str(li.get("num") or 0)) * Decimal(str(li.get("price") or 0))
                 for li in lines),
                Decimal("0.00"),
            )
            checked += 1
            if total != Decimal(str(row.get("amount"))):
                mismatched.append(f"订单{oid}: 明细合计 {total} ≠ 金额 {row.get('amount')}")
        u.check(checked > 0, "至少有一笔订单录入了明细可校验", f"校验 {checked} 笔")
        u.check(not mismatched, "订单金额 = 明细（数量×单价）之和，Decimal 精确相等",
                "；".join(mismatched[:3]) if mismatched else f"{checked} 笔全部相符")
    else:
        u.check(False, "订单列表可访问", f"HTTP {st}")


def section_aggregates(tokens):
    """⑤ 客户消费统计必须等于订单实际。

    这两个字段（order_count / order_amount）是反范式冗余：订单表才是事实来源。
    后端在增删改订单时会重算，这里的断言就是防止它哪天又被改回"增量 +1/-1"——
    那套写法只要漏一次（删单不走模型、改单换了客户、直接改库）就会永久偏掉，
    而且不报错，只能靠对账发现。
    """
    u.section("⑤ 客户消费统计一致性")
    token = tokens.get("admin") or u.login("admin")

    status, payload = u.call("/api/sale_order/?page=1&size=100", token=token)
    if status != 200:
        u.check(False, "订单列表可访问", f"HTTP {status}")
        return

    orders = payload.get("results") or payload
    expected = {}
    for o in orders:
        cid = (o.get("customer") or {}).get("id")
        if not cid:
            continue
        n, amount = expected.get(cid, (0, Decimal("0.00")))
        expected[cid] = (n + 1, amount + Decimal(str(o.get("amount") or "0")))

    u.check(bool(expected), "有客户带订单可校验", f"{len(expected)} 个客户 / {len(orders)} 笔订单")

    mismatched = []
    for cid, (n, amount) in expected.items():
        st, cust = u.call(f"/api/customer/{cid}/", token=token)
        if st != 200:
            mismatched.append(f"客户{cid} 详情 HTTP {st}")
            continue
        got_n = cust.get("order_count")
        got_amount = Decimal(str(cust.get("order_amount") or "0"))
        if got_n != n or got_amount != amount:
            mismatched.append(f"客户{cid}: 记录 {got_n}次/{got_amount} ≠ 实际 {n}次/{amount}")

    u.check(not mismatched, "每个客户的消费次数与金额都等于其订单实际",
            "；".join(mismatched[:3]) if mismatched else f"{len(expected)} 个客户全部相符")


def section_validation(tokens):
    """⑥ 非法输入要在入库前被拦住。

    sale_order.pay_way 在库里是 enum，模型曾经只写了 CharField —— 于是任意字符串
    都能通过序列化层，一路走到 MySQL 才炸成 500 Data truncated。
    这条断言盯着"返回 400 而不是 500"。
    """
    u.section("⑥ 非法输入拦截")
    token = tokens.get("admin") or u.login("admin")

    payload = {
        "customer_id": 1,
        "consignee": "测试",
        "phone": "18710950666",
        "pay_way": "微信",  # 枚举里没有，库里也存不下
        "order_items": [{"id": 8, "num": 1, "price": "100.00", "commission_rate": "0.10"}],
    }
    status, data = u.call("/api/sale_order/", "POST", payload, token=token)
    u.check(status == 400, "非法支付方式返回 400（不是 500 DataError）", f"HTTP {status}")

    # 万一下次它又允许写入了，别把脏数据留在库里
    if status in (200, 201):
        oid = (data or {}).get("id")
        if oid:
            u.call(f"/api/sale_order/{oid}/", "DELETE", token=token)
            u.check(False, "非法订单已被写入（已回滚删除，但校验漏了）", f"订单 {oid}")


def main() -> int:
    print(f"目标：{u.BASE}")
    if not u.PASSWORD:
        print("! 找不到登录密码：请设置 DJRBAC_PASSWORD，或在 agent-server/.env 里配置")
        return 2

    # 先探活，避免后端没起来时打一堆看不懂的失败
    status, _ = u.call("/api/schema/")
    if status == -1:
        print(f"! 连不上后端 {u.BASE}，请先启动 Django（见 README「快速开始」）")
        return 2

    tokens = section_permission()
    section_money(tokens)
    section_chinese(tokens)
    section_integrity(tokens)
    section_aggregates(tokens)
    section_validation(tokens)
    return u.summary("业务验收")


if __name__ == "__main__":
    sys.exit(main())
