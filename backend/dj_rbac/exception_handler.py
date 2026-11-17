"""统一异常出口：让前端永远拿到同一份 JSON，而不是一坨 HTML。

在此之前，错误是两套语言：
  · 400 / 401 / 403  → {"message": "..."}，说得清原因
  · 没接住的异常      → 500 + Django 调试页整页 HTML（线上则是一句 Server Error）
                        —— 前端既不知道错在哪，也拿不到可以用来排查的线索

现在统一成：

    {"message": "...", "code": "...", "request_id": "..."}

三类来源分别处理：
  1. DRF 认识的异常（校验失败 / 权限 / 认证 / 404 / 405）：原样透出，
     只把 detail 改名为 message；字段级校验错误保持 {字段: [错误]} 的原形，
     前端本来就是按这个形状渲染的。
  2. 业务代码主动抛的 APIException：同上。
  3. 没人接的异常：服务端记完整 traceback + 编号，响应里只给编号。
     打开 DEBUG 时额外带上 detail（本机排查用）；关闭时不泄露内部信息。
"""

import logging
import uuid

from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler

logger = logging.getLogger("dj_rbac.api")


def custom_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)

    if response is None:
        # ---- 走到这里说明没人接这个异常 ----
        rid = uuid.uuid4().hex[:12]
        request = context.get("request")
        logger.exception(
            "未捕获异常 rid=%s %s %s",
            rid,
            getattr(request, "method", "-"),
            getattr(request, "path", "-"),
        )
        body = {
            "message": f"服务器内部错误，请把编号 {rid} 发给管理员",
            "code": "internal_error",
            "request_id": rid,
        }
        # 只在调试模式下把异常类型和原文带出去
        if settings.DEBUG:
            body["detail"] = f"{type(exc).__name__}: {exc}"
        return Response(body, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # ---- DRF 已知异常：统一字段名 ----
    data = response.data
    if isinstance(data, dict) and "message" not in data and "detail" in data:
        detail = data["detail"]
        normalized = {"message": detail if isinstance(detail, str) else str(detail)}
        # simplejwt 这类异常还会带 code / messages，一并保留
        for key in ("code", "messages"):
            if key in data:
                normalized[key] = data[key]
        response.data = normalized
    return response
