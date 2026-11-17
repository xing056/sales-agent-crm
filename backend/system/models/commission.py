from django.db import models
from .index import User


# 员工提成表模型类
class Commission(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="员工用户对象"
    )
    commission = models.DecimalField(
        null=True, blank=True, max_digits=10, decimal_places=2, verbose_name="提成金额"
    )
    year_month = models.IntegerField(null=True, blank=True, verbose_name="所属期")
    status = models.BooleanField(default=True, verbose_name="状态")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = "commission"
        ordering = ["-id"]
