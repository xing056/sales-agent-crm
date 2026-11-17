"""Tokens 用量：内部上报 + 超管看板查询。

【两个接口，两套完全不同的信任模型】
    report   —— 只有智能体服务能调，用共享密钥（X-Internal-Key），不走用户令牌。
                原因：普通员工如果能调这个接口，就能给任何人伪造用量，
                看板立刻变成假的。共享密钥没配时必须**拒绝所有请求**，
                不能"没配就放行"——那等于默认开放。
    summary  —— 走正常登录鉴权 + RBAC 权限码。超管看全部，
                普通员工只能看自己（防止互相看到彼此的消耗）。

【为什么存明细、聚合在查询时算】
    见 models/ai_usage.py 的说明。这里只强调一点：
    口径（今天/本周/本月、环比区间）全部在查询时决定，
    所以以后改口径不需要动历史数据。
"""

from datetime import datetime, time, timedelta

from django.conf import settings
from django.db.models import Count, Sum
from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from system.models import LlmUsage

# 单次上报的字段上限：防脏数据把统计带偏。
# 真实一次请求的输入 token 不可能到 200 万（那已经是百万级上下文）。
MAX_TOKENS_PER_REQUEST = 2_000_000

RANGE_LABELS = {"today": "今天", "week": "本周", "month": "本月"}


def _day_start(moment):
    """取某个时刻所在自然日的 00:00（带时区）。"""
    return timezone.make_aware(datetime.combine(timezone.localtime(moment).date(), time.min))


def _range_bounds(range_key: str):
    """返回 (本期开始, 本期结束, 上期开始, 上期结束)。

    「本周」按周一起算（国内习惯），「本月」按自然月。
    上期 = 紧邻的同样长度区间，用来算环比。
    """
    now = timezone.now()
    today = _day_start(now)

    if range_key == "today":
        start = today
        end = start + timedelta(days=1)
    elif range_key == "week":
        start = today - timedelta(days=today.weekday())  # weekday(): 周一=0
        end = start + timedelta(days=7)
    else:  # month（默认）
        start = _day_start(now.replace(day=1))
        # 下月 1 日：先跳到本月最后一天再加 1 天，避免 2 月/31 日的边界坑
        end = _day_start((start + timedelta(days=32)).replace(day=1))

    span = end - start
    return start, end, start - span, start


class LlmUsageReportView(APIView):
    """智能体服务内部上报一次请求的用量。

    刻意关掉认证和 RBAC 权限 —— 因为调用方不是"某个登录用户"，是另一个进程。
    安全性由共享密钥承担，且密钥缺失时一律拒绝。
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request):
        expected = getattr(settings, "INTERNAL_API_KEY", "") or ""
        if not expected:
            # 关键：没配置就不许用。否则等于给所有能访问 8000 的人开了写权限。
            return Response({"message": "服务端未配置 INTERNAL_API_KEY，内部上报已禁用"}, status=403)
        if request.headers.get("X-Internal-Key") != expected:
            return Response({"message": "内部上报密钥不正确"}, status=403)

        data = request.data or {}
        username = str(data.get("username") or "").strip()
        if not username:
            return Response({"message": "缺少 username"}, status=400)

        tokens = {}
        for field in ("prompt_tokens", "completion_tokens", "cached_tokens", "reasoning_tokens"):
            try:
                value = int(data.get(field) or 0)
            except (TypeError, ValueError):
                return Response({"message": f"{field} 必须是整数"}, status=400)
            if value < 0 or value > MAX_TOKENS_PER_REQUEST:
                return Response({"message": f"{field} 超出合理范围"}, status=400)
            tokens[field] = value

        try:
            employee_id = int(data["employee_id"]) if data.get("employee_id") else None
        except (TypeError, ValueError):
            employee_id = None

        row = LlmUsage.objects.create(
            username=username[:50],
            employee_id=employee_id,
            session_key=str(data.get("session_key") or "")[:64],
            model=(str(data.get("model") or "")[:50] or None),
            round_no=int(data.get("round_no") or 0),
            **tokens,
        )

        # 顺手把"该账号今日累计"返回去：智能体那边要用它做预算熔断，
        # 这样一次往返同时完成记账和取数，不用再单独查一次。
        today = _day_start(timezone.now())
        today_total = (
            LlmUsage.objects.filter(username=row.username, created_at__gte=today)
            .aggregate(p=Sum("prompt_tokens"), c=Sum("completion_tokens"))
        )
        return Response({
            "ok": True,
            "id": row.id,
            "today_prompt": today_total["p"] or 0,
            "today_completion": today_total["c"] or 0,
        })


class LlmUsageViewSet(GenericViewSet):
    """超管看板：按账号聚合 + 明细。"""

    queryset = LlmUsage.objects.all()
    rbac_permissions = {
        "summary": "api:llm_usage:summary",
        "list": "api:llm_usage:list",
    }

    def _scoped(self, request):
        """超管看全部，其他人只看自己。

        这条不是"顺手加的过滤"——没有它，任何一个员工都能看到同事的消耗，
        而这个数字直接对应公司花出去的钱。
        """
        qs = LlmUsage.objects.all()
        if request.user.is_superuser:
            return qs
        return qs.filter(username=request.user.username)

    @action(["get"], detail=False)
    def summary(self, request):
        range_key = request.query_params.get("range", "month")
        if range_key not in RANGE_LABELS:
            return Response({"message": "range 只能是 today / week / month"}, status=400)

        start, end, prev_start, prev_end = _range_bounds(range_key)
        base = self._scoped(request)

        current = base.filter(created_at__gte=start, created_at__lt=end)
        rows = (
            current.values("username")
            .annotate(
                # 每次请求一行，所以"请求次数"就是行数
                requests=Count("id"),
                prompt_tokens=Sum("prompt_tokens"),
                completion_tokens=Sum("completion_tokens"),
                cached_tokens=Sum("cached_tokens"),
                reasoning_tokens=Sum("reasoning_tokens"),
            )
            .order_by("-prompt_tokens")
        )

        items = []
        for row in rows:
            prompt = row["prompt_tokens"] or 0
            completion = row["completion_tokens"] or 0
            cached = row["cached_tokens"] or 0
            items.append({
                "username": row["username"],
                "requests": row["requests"],
                "prompt_tokens": prompt,
                "completion_tokens": completion,
                "cached_tokens": cached,
                "total_tokens": prompt + completion,
                # 缓存命中率只对输入有意义：命中的部分按折扣价计费
                "cache_hit_rate": round(cached / prompt, 4) if prompt else 0,
            })

        total_prompt = sum(i["prompt_tokens"] for i in items)
        total_completion = sum(i["completion_tokens"] for i in items)
        total_cached = sum(i["cached_tokens"] for i in items)
        total_requests = sum(i["requests"] for i in items)

        prev = base.filter(created_at__gte=prev_start, created_at__lt=prev_end).aggregate(
            p=Sum("prompt_tokens"), c=Sum("completion_tokens")
        )
        prev_total = (prev["p"] or 0) + (prev["c"] or 0)
        current_total = total_prompt + total_completion

        return Response({
            "range": range_key,
            "range_label": RANGE_LABELS[range_key],
            "start": start,
            "end": end,
            "total": {
                "requests": total_requests,
                "prompt_tokens": total_prompt,
                "completion_tokens": total_completion,
                "cached_tokens": total_cached,
                "total_tokens": current_total,
                "cache_hit_rate": round(total_cached / total_prompt, 4) if total_prompt else 0,
            },
            "previous": {"total_tokens": prev_total},
            # 上期为 0 时不返回百分比 —— 从 0 涨到任何数都是无限增长，没有意义
            "change_rate": (round((current_total - prev_total) / prev_total, 4) if prev_total else None),
            "items": items,
        })

    def list(self, request):
        """明细：最近的请求流水，用于核对聚合数字。"""
        qs = self._scoped(request)
        try:
            limit = min(int(request.query_params.get("limit", 50)), 200)
        except (TypeError, ValueError):
            limit = 50
        rows = qs.values(
            "id", "username", "session_key", "model", "round_no",
            "prompt_tokens", "completion_tokens", "cached_tokens", "reasoning_tokens",
            "created_at",
        )[:limit]
        return Response({"items": list(rows), "limit": limit})
