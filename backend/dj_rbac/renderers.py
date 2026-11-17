"""让 DRF 在 JSON 里把 Decimal 原样输出成字符串，而不是转成 float。

【为什么需要这个文件】
    DRF 的默认编码器（rest_framework.utils.encoders.JSONEncoder）里有一行：
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
    也就是说：只要视图直接 return Response(queryset/聚合结果)，
    哪怕模型字段是 DecimalField、数据库是 decimal(10,2)，
    到了 JSON 这一层也会被转成二进制浮点。

    「模型用 Decimal」不等于「接口不丢精度」—— 精度是在最后一米丢的。

    序列化器（Serializer）路径不受影响：DecimalField 默认输出字符串
    （COERCE_DECIMAL_TO_STRING=True）。出问题的是统计这类
    "直接返回聚合结果"的接口，恰好又是报表最常看的地方。

【改完之后】
    Decimal('2800.00')  →  "2800.00"（字符串，前端展示不需要再算）
"""

from decimal import Decimal

from rest_framework.renderers import JSONRenderer
from rest_framework.utils.encoders import JSONEncoder


class MoneySafeJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            # format(..., 'f') 不用科学计数法，也不会丢掉末尾的 0
            return format(obj, "f")
        return super().default(obj)


class MoneySafeJSONRenderer(JSONRenderer):
    encoder_class = MoneySafeJSONEncoder
