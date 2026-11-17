"""客户消费统计（消费次数 / 消费总额）的同步逻辑。

【为什么不做增量维护】

    最直觉的写法是下单时 `customer.order_count += 1`，删单时 `-= 1`。
    这是错的，而且错得很隐蔽：

      · 删单走的是 queryset.delete()（不触发模型的 delete）→ 少减一次
      · 改单把客户从 A 改成 B → A 没减、B 没加
      · 有人直接改库、脚本导入数据 → 完全绕过
      · 一次失败的回滚可能只回滚了一半

    任何一次漏掉，误差就永久留在数据里，而且**没有任何报错**，只能靠对账发现。

【这里的做法】

    一律「按订单表重算」：把该客户的订单数、金额合计重新算一遍写回去。
    幂等、可重复执行、不需要知道之前发生过什么 —— 即使数据已经漂了，
    调一次就修正回来。下单 / 改单 / 删单之后调用同一个函数即可。

    重算用的是订单表，所以客户的统计**永远等于**订单实际，不会出现
    "客户说有 3 单、订单表有 5 单"这种对不上的情况。
"""

from decimal import Decimal

from django.db.models import Count, Sum

from ..models import Customer, SaleOrder

ZERO = Decimal("0.00")


def sync_customer_stats(customer_id):
    """重算并写回单个客户的消费统计。返回写入后的值（客户已不存在则返回 None）。

    用 .update() 而不是 save()：不触发信号、不覆盖其他字段，也不会因为
    模型层的 default 把金额写成 int。
    """
    if not customer_id:
        return None

    agg = SaleOrder.objects.filter(customer_id=customer_id).aggregate(
        total_count=Count("id"),
        total_amount=Sum("amount"),
    )
    order_count = agg["total_count"] or 0
    order_amount = agg["total_amount"] or ZERO

    updated = Customer.objects.filter(pk=customer_id).update(
        order_count=order_count,
        order_amount=order_amount,
    )
    if not updated:
        return None
    return {
        "customer_id": customer_id,
        "order_count": order_count,
        "order_amount": str(order_amount),
    }


def sync_all_customer_stats(dry_run=False):
    """全量重算所有客户，返回 (客户总数, 需要修正的数量, 明细列表)。

    用两条查询算出全部统计，再和现有值逐个比对：
    只有真的不一致才写库，避免无谓的 UPDATE。
    """
    rows = (
        SaleOrder.objects.exclude(customer_id__isnull=True)
        .values("customer_id")
        .annotate(total_count=Count("id"), total_amount=Sum("amount"))
    )
    stats = {
        r["customer_id"]: (r["total_count"], r["total_amount"] or ZERO)
        for r in rows
    }

    total = 0
    changed = []
    for cust in Customer.objects.all().only("id", "name", "order_count", "order_amount"):
        total += 1
        real_count, real_amount = stats.get(cust.id, (0, ZERO))
        stored_amount = cust.order_amount or ZERO
        if cust.order_count != real_count or stored_amount != real_amount:
            changed.append(
                {
                    "id": cust.id,
                    "name": cust.name,
                    "before": (cust.order_count, str(stored_amount)),
                    "after": (real_count, str(real_amount)),
                }
            )
            if not dry_run:
                Customer.objects.filter(pk=cust.id).update(
                    order_count=real_count, order_amount=real_amount
                )

    return total, len(changed), changed
