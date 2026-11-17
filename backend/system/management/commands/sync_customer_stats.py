"""按订单表重算客户消费统计。

    python manage.py sync_customer_stats            # 修正数据
    python manage.py sync_customer_stats --dry-run   # 只体检，不写库

命令是幂等的：跑一次和跑十次结果一样。日常不需要手动跑（下单/改单/删单
已经自动同步），它的用途是：
    · 首次接入历史数据后做一次性回填
    · 有人绕过接口直接改库之后，把数据修回来
    · CI 或演示前体检：--dry-run 能告诉你有没有对不上的客户
"""

from django.core.management.base import BaseCommand

from system.utils.customer_stats import sync_all_customer_stats


class Command(BaseCommand):
    help = "按订单表重算客户的消费次数/消费总额（幂等）"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="只检查不写库，用于体检",
        )

    def handle(self, *args, **options):
        dry = options["dry_run"]
        total, changed_count, details = sync_all_customer_stats(dry_run=dry)

        if not changed_count:
            self.stdout.write(self.style.SUCCESS(
                f"体检完成：{total} 个客户的消费统计全部正确，无需修正"
            ))
            return

        mode = "需要修正（未写库）" if dry else "已修正"
        self.stdout.write(self.style.WARNING(
            f"{mode}：{changed_count} / {total} 个客户"
        ))
        for item in details[:20]:
            before_n, before_amt = item["before"]
            after_n, after_amt = item["after"]
            self.stdout.write(
                f"  客户 {item['id']:>4} {item['name'] or '':<8}"
                f" 次数 {before_n} → {after_n}   金额 {before_amt} → {after_amt}"
            )
        if len(details) > 20:
            self.stdout.write(f"  …… 其余 {len(details) - 20} 个略")

        if dry:
            self.stdout.write("（--dry-run 模式，未写入数据库）")
        else:
            self.stdout.write(self.style.SUCCESS("修正完成"))
