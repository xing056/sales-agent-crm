from django.db import models


class LlmUsage(models.Model):
    """一次模型请求的用量流水。

    【为什么是"每次请求一行"，不是"每人每天一行"】
        只在聚合表里存天/周/月的合计，等于把口径焊死在表结构里 —— 哪天
        "周"的定义改了、或者要看"某个会话第几轮最贵"，历史数据就废了。
        存明细，任何粒度都是查询时算出来的，随时能换口径重算。

    【为什么不存 access_token】
        session_key 是令牌的 sha1 前 16 位，只能用来区分会话，反推不出令牌。
        流水表一旦存了原始令牌，就等于给"能读这张表的人"发了一把万能钥匙。

    【username 为什么必须单独存】
        智能体的会话是按令牌哈希分桶的（换浏览器 = 新会话），
        所以"按人聚合"不能靠 session_key，只能靠这里冗余的 username。
    """

    username = models.CharField(max_length=50, verbose_name="账号")
    # 员工id 只做归属参考，取不到就留空（密码登录模式拿不到员工资料）
    employee_id = models.IntegerField(null=True, blank=True, verbose_name="员工id")
    session_key = models.CharField(max_length=64, verbose_name="会话标识(令牌哈希)")
    model = models.CharField(max_length=50, null=True, blank=True, verbose_name="模型")
    round_no = models.SmallIntegerField(default=0, verbose_name="循环轮次")
    prompt_tokens = models.PositiveIntegerField(default=0, verbose_name="输入token")
    completion_tokens = models.PositiveIntegerField(default=0, verbose_name="输出token")
    cached_tokens = models.PositiveIntegerField(default=0, verbose_name="缓存命中token")
    reasoning_tokens = models.PositiveIntegerField(default=0, verbose_name="思考token")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发生时间")

    class Meta:
        db_table = "llm_usage"
        ordering = ["-id"]
        indexes = [
            # 看板的主查询是"某个时间范围内按账号分组"，这条索引正对着它
            models.Index(fields=["username", "created_at"], name="idx_usage_user_time"),
            # 单看时间范围的汇总（不分组）走这条
            models.Index(fields=["created_at"], name="idx_usage_time"),
        ]

    def __str__(self):
        return f"{self.username} {self.prompt_tokens}+{self.completion_tokens}"
