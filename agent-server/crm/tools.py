"""CRM 工具层：模型能"看到"什么工具、真实执行如何路由。

三件套结构（agent/registry.py 里预留的三个插槽）：
    TOOLS           → 给模型看的工具说明书（JSON Schema）
    CONFIRM_REQUIRED→ 写操作名单，调用前必须用户确认
    TOOL_DISPATCH   → 名字 → 真实函数（模型只能提议，执行权在代码）

执行函数不做任何本地查询，而是通过 HTTP 调 dj-rbac 的真实接口，
带着当前登录用户的 JWT。所以权限校验、行级隔离全是后端说了算，
智能体本身没有特权。

【为什么用线程本地变量存 client】
工具分发表是模块级的（模型看到的是同一套说明），但"用谁的身份执行"
是每个请求各自的。server 是多线程的，用 threading.local 把
"当前请求的 client" 绑到线程上，避免并发时串号。
"""

import threading
from decimal import Decimal, ROUND_HALF_UP

from .client import CrmClient

# ---------- 当前请求上下文 ----------

_ctx = threading.local()


def bind(client: CrmClient):
    _ctx.client = client


def _c() -> CrmClient:
    client = getattr(_ctx, "client", None)
    if client is None:
        raise RuntimeError("工具上下文未绑定：请先调用 bind(client)")
    return client


# ---------- 字段翻译与瘦身 ----------

LEVELS = {0: "未分级", 1: "一般客户", 2: "重点客户"}

# ---------- 金额一律走 Decimal ----------
# 铁律：钱不能用 float。0.1 + 0.2 在二进制浮点里等于 0.30000000000000004，
# 单笔看不出来（落库只留两位），一旦累加、对账、算佣金就会差几分钱。
# 这里统一：
#   入参 str/int → Decimal；出参转成两位小数的字符串。
# 为什么出参用字符串而不是数字：JSON 的数字类型没有精度概念，
# 前端 JS 解析 "437.00" 成 number 又是 float，等于白做。
CENTS = Decimal("0.01")


def _dec(value) -> Decimal:
    if value is None or value == "":
        return Decimal("0.00")
    return Decimal(str(value))


def _money(value) -> str:
    """金额 → '437.00' 这样的两位小数字符串（四舍五入用银行家舍入之外的标准 HALF_UP）。"""
    return str(_dec(value).quantize(CENTS, rounding=ROUND_HALF_UP))


def _employee_name(user):
    """从嵌套的 user 对象里取出「员工姓名」，取不到就退回账号名。

    注意：dj-rbac 的 user 序列化非常深（user.employee.department...），
    整个塞给模型既浪费 token 又容易干扰判断，所以这里只提炼需要的字段。
    """
    if not isinstance(user, dict):
        return None
    employee = user.get("employee") or {}
    return employee.get("name") or user.get("username")


def _region(obj):
    parts = [obj.get("province"), obj.get("city"), obj.get("county")]
    return " ".join([p for p in parts if p]) or None


def _slim_customer(c):
    return {
        "客户ID": c.get("id"),
        "姓名": c.get("name"),
        "手机": c.get("phone"),
        "等级": LEVELS.get(c.get("level"), c.get("level")),
        "消费次数": c.get("order_count"),
        "消费金额": _money(c.get("order_amount")),
        "地区": _region(c),
        "销售员": _employee_name(c.get("user")),
        "来源": (c.get("source") or {}).get("name"),
        "状态": "正常" if c.get("status") else "锁定",
    }


def _full_address(o):
    """拼完整地址。address 字段里有些数据已经带了区县，重复拼会变成
    "龙岗区学园一巷115号 龙岗区学园一巷115号"，所以先判重。"""
    head = [o.get("province"), o.get("city")]
    head = [p for p in head if p]
    county = o.get("county") or ""
    address = o.get("address") or ""
    if county and county in address:
        county = ""
    parts = head + [p for p in (county, address) if p]
    # "深圳 深圳" 这种省市同名的情况去个重
    if len(parts) >= 2 and parts[0] == parts[1]:
        parts = parts[1:]
    return " ".join(parts) or None


def _slim_order(o):
    return {
        "订单ID": o.get("id"),
        "订单号": o.get("order_no"),
        "客户ID": (o.get("customer") or {}).get("id"),
        "客户": (o.get("customer") or {}).get("name"),
        "销售员": _employee_name(o.get("user")),
        "金额": _money(o.get("amount")),
        "佣金": _money(o.get("commission")),
        "订单状态": "正常" if o.get("status") else "已取消",
        "支付状态": "已支付" if o.get("pay_status") else "未支付",
        "支付方式": o.get("pay_way"),
        "收货人": o.get("consignee"),
        "收货电话": o.get("phone"),
        "收货地址": _full_address(o),
        "下单时间": o.get("create_time"),
    }


def _slim_tracking(t):
    return {
        "跟踪ID": t.get("id"),
        "客户ID": (t.get("customer") or {}).get("id"),
        "客户": (t.get("customer") or {}).get("name"),
        "销售员": _employee_name(t.get("user")),
        "跟踪方式": t.get("tracking_way"),
        "跟踪结果": t.get("description"),
        "跟踪时间": t.get("tracking_time"),
    }


def _forbidden_hint(status, payload, fallback_tool):
    """把后端的 403 翻译成模型能照着办的话，而不是一句干巴巴的报错。"""
    message = (payload or {}).get("message") or (payload or {}).get("detail") or "请求被拒绝"
    if status == 403:
        return {
            "ok": False,
            "原因": f"当前账号没有该数据权限（后端返回：{message}）",
            "建议": f"如实告知用户权限不足，不要猜测数据；可以改用 {fallback_tool} 查他自己的数据",
        }
    return {"ok": False, "原因": f"接口调用失败（HTTP {status}）：{message}"}


# ---------- 工具实现 ----------

def whoami() -> dict:
    """当前登录人：账号、员工、部门、岗位、角色。"""
    profile = _c().profile or {}
    employee = profile.get("employee") or {}
    return {
        "账号": profile.get("username"),
        "员工": employee.get("name"),
        "部门": (employee.get("department") or {}).get("name"),
        "岗位": (employee.get("position") or {}).get("name"),
        "角色": [r.get("name") for r in (profile.get("role") or [])],
        "是否超级管理员": bool(profile.get("is_superuser")),
    }


def list_customers(keyword: str = "", sales: str = "", level: str = "", limit: int = 20) -> dict:
    """查客户。keyword 模糊匹配姓名/手机/地区；sales 按销售员姓名过滤；level 按等级过滤。"""
    status, meta, rows = _c().list_all("/api/customer/")
    if status != 200:
        return _forbidden_hint(status, meta, "my_customers")

    def match(c):
        if keyword:
            text = " ".join(str(x) for x in [
                c.get("name"), c.get("phone"), c.get("province"), c.get("city"),
                c.get("county"), c.get("address"),
            ] if x)
            if keyword not in text:
                return False
        if sales and sales not in (_employee_name(c.get("user")) or ""):
            return False
        if level:
            target = {"未分级": 0, "一般客户": 1, "重点客户": 2}.get(level, None)
            if target is not None and c.get("level") != target:
                return False
        return True

    hit = [c for c in rows if match(c)]
    slim = [_slim_customer(c) for c in hit[:max(1, min(limit, 50))]]
    result = {
        "ok": True,
        "全库客户数": meta.get("count"),
        "命中数": len(hit),
        "返回": slim,
    }
    if len(hit) > len(slim):
        result["提示"] = f"共命中 {len(hit)} 条，只返回前 {len(slim)} 条，可加条件缩小范围"
    if not hit:
        result["提示"] = "没有符合条件的客户"
    return result


def my_customers(limit: int = 20) -> dict:
    """查"我的客户"——后端按当前登录人做了行级隔离，只会返回自己跟的客户。"""
    status, meta, rows = _c().list_all("/api/customer/of_me/")
    if status != 200:
        return _forbidden_hint(status, meta, "whoami")
    slim = [_slim_customer(c) for c in rows[:max(1, min(limit, 50))]]
    return {
        "ok": True,
        "我的客户数": meta.get("count"),
        "返回": slim,
        "说明": "这是后端行级隔离后的结果，仅当前账号负责的客户",
    }


def get_customer(customer_id: int) -> dict:
    """按客户ID查详情（含推荐人、备注）。"""
    status, payload = _c().get_one(f"/api/customer/{customer_id}/")
    if status != 200:
        if status == 404:
            return {"ok": False, "原因": f"客户ID {customer_id} 不存在"}
        return _forbidden_hint(status, payload, "my_customers")
    detail = _slim_customer(payload)
    detail["备注"] = payload.get("remark")
    parent = payload.get("parent")
    detail["推荐人"] = (parent or {}).get("name") if isinstance(parent, dict) else None
    return {"ok": True, "客户": detail}


def list_trackings(customer_id: int = 0, keyword: str = "", limit: int = 20) -> dict:
    """查客户跟踪记录。可按客户ID精确查，或按客户姓名模糊查。"""
    params = {"customer_id": customer_id} if customer_id else None
    status, meta, rows = _c().list_all("/api/customer_tracking/", params=params)
    if status != 200:
        return _forbidden_hint(status, meta, "my_customers")
    if keyword:
        rows = [t for t in rows if keyword in ((t.get("customer") or {}).get("name") or "")]
    slim = [_slim_tracking(t) for t in rows[:max(1, min(limit, 50))]]
    result = {"ok": True, "命中数": len(rows), "返回": slim}
    if not rows:
        result["提示"] = "没有查到跟踪记录"
    return result


def list_orders(keyword: str = "", customer_id: int = 0, pay_status: str = "", limit: int = 20) -> dict:
    """查销售订单。keyword 匹配客户姓名/订单号/收货人；pay_status 取 已支付/未支付。"""
    status, meta, rows = _c().list_all("/api/sale_order/")
    if status != 200:
        return _forbidden_hint(status, meta, "my_customers")

    def match(o):
        if customer_id and (o.get("customer") or {}).get("id") != customer_id:
            return False
        if keyword:
            text = " ".join(str(x) for x in [
                (o.get("customer") or {}).get("name"), o.get("order_no"),
                o.get("consignee"), o.get("phone"),
            ] if x)
            if keyword not in text:
                return False
        if pay_status:
            want = pay_status == "已支付"
            if bool(o.get("pay_status")) != want:
                return False
        return True

    hit = [o for o in rows if match(o)]
    slim = [_slim_order(o) for o in hit[:max(1, min(limit, 50))]]
    # 合计用 Decimal 累加，再统一格式化；不能用 sum() 直接把字符串加起来
    total_amount = sum((_dec(x["金额"]) for x in slim), Decimal("0.00"))
    result = {
        "ok": True,
        "全库订单数": meta.get("count"),
        "命中数": len(hit),
        "本次返回金额合计": _money(total_amount),
        "返回": slim,
    }
    if len(hit) > len(slim):
        result["提示"] = f"共命中 {len(hit)} 条，只返回前 {len(slim)} 条"
    if not hit:
        result["提示"] = "没有符合条件的订单"
    return result


def get_order(order_id: int) -> dict:
    """按订单ID查详情（含商品明细）。"""
    status, payload = _c().get_one(f"/api/sale_order/{order_id}/")
    if status != 200:
        if status == 404:
            return {"ok": False, "原因": f"订单ID {order_id} 不存在"}
        return _forbidden_hint(status, payload, "my_customers")
    order = _slim_order(payload)
    st, items = _c().get_one("/api/sale_order_item/", params={"order_id": order_id})
    if st == 200:
        rows = items if isinstance(items, list) else (items.get("results") or [])
        order["商品明细"] = [
            {
                "商品": i.get("name"),
                "数量": i.get("num"),
                "单价": _money(i.get("price")),
                "佣金比例": _money(i.get("commission_rate")),
            }
            for i in rows
        ]
    return {"ok": True, "订单": order}


STAT_KINDS = {
    "商品销售排行": "top_sale_product",
    "销售员业绩排行": "top10_sale_employee",
    "省份客户排行": "top10_province_customer",
    "本周每日销售额": "weekday_sale_amount",
    "本月每日销售额": "month_day_sale_amount",
    "年度各月销售额": "year_month_sale_amount",
    "今日单量与金额": "today_order_num_and_amount",
}


def sales_stats(kind: str) -> dict:
    """取销售统计。kind 必须是 STAT_KINDS 里的中文名之一。"""
    path = STAT_KINDS.get(kind)
    if not path:
        return {"ok": False, "原因": f"不支持的统计类型：{kind}", "可选": list(STAT_KINDS)}
    status, payload = _c().get_one(f"/api/stat/{path}/")
    if status != 200:
        return {"ok": False, "原因": f"统计接口返回 HTTP {status}"}
    if isinstance(payload, list):
        payload = payload[:12]
    return {"ok": True, "统计类型": kind, "数据": payload}


def add_tracking(customer_id: int, tracking_way: str, description: str) -> dict:
    """给客户新增一条跟踪记录（写操作，需用户确认后执行）。"""
    status, payload = _c().call(
        "POST", "/api/customer_tracking/",
        {"customer_id": customer_id, "tracking_way": tracking_way, "description": description},
    )
    if status in (200, 201):
        return {"ok": True, "已写入": _slim_tracking(payload), "说明": "跟踪记录已保存到数据库"}
    message = payload.get("message") or payload.get("detail") or payload
    if status == 400 and isinstance(payload, dict):
        message = payload
    return {"ok": False, "原因": f"写入失败（HTTP {status}）：{message}"}


def describe_add_tracking(customer_id: int, tracking_way: str, description: str) -> dict:
    """确认框摘要：把参数翻成"要动谁、动什么"，并用真实数据核对一遍。

    这个函数在用户点「确认」**之前**跑，只读不写。
    客户名、等级、归属销售全部取自接口真值 —— 不用模型给的参数、
    更不让模型自己描述后果（它会记错客户名、编错数字）。
    """
    status, payload = _c().get_one(f"/api/customer/{customer_id}/")
    if status != 200 or not isinstance(payload, dict):
        return {
            "标题": f"给客户 ID={customer_id} 新增一条跟踪记录",
            "字段": [
                ["客户", f"ID={customer_id}"],
                ["跟踪方式", tracking_way],
                ["内容", description],
            ],
            "警告": f"客户详情读取失败（HTTP {status}），请先核对这个客户 ID 是否真实存在",
        }
    return {
        "标题": "将新增一条客户跟踪记录",
        "字段": [
            ["客户", f"{payload.get('name')}（ID={customer_id}）"],
            ["客户等级", LEVELS.get(payload.get("level"), payload.get("level") or "-")],
            ["归属销售", _employee_name(payload.get("user"))],
            ["跟踪方式", tracking_way],
            ["内容", description],
        ],
        "提示": "确认后立即写入数据库，并计入该客户的跟进记录",
    }


# ---------- 工具说明书 ----------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "whoami",
            "description": "查询当前登录人是谁：账号、员工姓名、部门、岗位、角色、是否超管。涉及'我'的问题先调它",
            "parameters": {"type": "object", "properties": {}},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_customers",
            "description": (
                "查询客户列表（需要客户列表权限）。keyword 模糊匹配姓名/手机/地区；"
                "sales 按销售员姓名过滤；level 可选 未分级/一般客户/重点客户"
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "姓名、手机号或地区的关键词，可留空"},
                    "sales": {"type": "string", "description": "销售员姓名，可留空"},
                    "level": {"type": "string", "description": "客户等级：未分级 / 一般客户 / 重点客户"},
                    "limit": {"type": "integer", "description": "最多返回几条，默认 20"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "my_customers",
            "description": "查询'我的客户'——后端按登录人做了行级隔离，只返回当前账号负责跟进的客户。问'我的客户'时用它",
            "parameters": {
                "type": "object",
                "properties": {"limit": {"type": "integer", "description": "最多返回几条，默认 20"}},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_customer",
            "description": "按客户ID查客户详情（含等级、消费金额、销售员、来源、备注、推荐人）",
            "parameters": {
                "type": "object",
                "properties": {"customer_id": {"type": "integer", "description": "客户ID，数字"}},
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_trackings",
            "description": "查询客户跟踪记录（谁在什么时候用什么方式跟进了哪个客户、结果如何）",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer", "description": "客户ID，精确查某个客户时填"},
                    "keyword": {"type": "string", "description": "客户姓名关键词，模糊查时填"},
                    "limit": {"type": "integer", "description": "最多返回几条，默认 20"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_orders",
            "description": "查询销售订单。keyword 匹配客户姓名/订单号/收货人；也可按客户ID或支付状态过滤",
            "parameters": {
                "type": "object",
                "properties": {
                    "keyword": {"type": "string", "description": "客户姓名、订单号或收货人关键词"},
                    "customer_id": {"type": "integer", "description": "客户ID，精确查某客户的所有订单"},
                    "pay_status": {"type": "string", "description": "支付状态：已支付 / 未支付"},
                    "limit": {"type": "integer", "description": "最多返回几条，默认 20"},
                },
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order",
            "description": "按订单ID查订单详情，含商品明细（商品、数量、单价、佣金比例）",
            "parameters": {
                "type": "object",
                "properties": {"order_id": {"type": "integer", "description": "订单ID，数字"}},
                "required": ["order_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "sales_stats",
            "description": (
                "取销售统计报表。kind 只能取：商品销售排行 / 销售员业绩排行 / 省份客户排行 / "
                "本周每日销售额 / 本月每日销售额 / 年度各月销售额 / 今日单量与金额"
            ),
            "parameters": {
                "type": "object",
                "properties": {"kind": {"type": "string", "description": "上面列出的统计类型之一"}},
                "required": ["kind"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "add_tracking",
            "description": "给某个客户新增一条跟踪记录（写操作，系统会先让用户确认再执行）",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {"type": "integer", "description": "要跟进的客户ID"},
                    "tracking_way": {"type": "string", "description": "跟踪方式，例如：电话 / 微信 / 上门拜访"},
                    "description": {"type": "string", "description": "跟踪结果或沟通内容"},
                },
                "required": ["customer_id", "tracking_way", "description"],
            },
        },
    },
]

# 写操作必须人工确认 —— 判断标准：只读直接执行，写库必须点确认
CONFIRM_REQUIRED = {"add_tracking"}

# 确认前先给用户看一段"人话摘要"：由代码用真实数据算，不交给模型
CONFIRM_PREVIEW = {
    "add_tracking": describe_add_tracking,
}

TOOL_DISPATCH = {
    "whoami": whoami,
    "list_customers": list_customers,
    "my_customers": my_customers,
    "get_customer": get_customer,
    "list_trackings": list_trackings,
    "list_orders": list_orders,
    "get_order": get_order,
    "sales_stats": sales_stats,
    "add_tracking": add_tracking,
}


def execute_tool(name: str, args: dict) -> dict:
    """统一执行入口：白名单校验 + 统一兜底，方便加审计日志。"""
    if name not in TOOL_DISPATCH:
        return {"ok": False, "原因": f"未知工具：{name}"}
    try:
        return TOOL_DISPATCH[name](**(args or {}))
    except TypeError as exc:
        return {"ok": False, "原因": f"参数不匹配：{exc}"}
    except Exception as exc:
        return {"ok": False, "原因": f"工具执行异常：{exc}"}
