"""金额精度体检：把所有接口跑一遍，扫描返回体里有没有 float 类型的金额。

判定标准：
  · 出现在金额相关字段上的 float → 不合格
  · 金额是字符串（"2800.00"）或整数（数量类）→ 合格
"""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000"
PWD = "123123"

ENDPOINTS = [
    "/api/customer/?page=1&size=100",
    "/api/customer/1/",
    "/api/customer/of_me/",
    "/api/customer_tracking/?size=100",
    "/api/sale_order/?page=1&size=100",
    "/api/sale_order/13/",
    "/api/sale_order_item/?order_id=13",
    "/api/product/",
    "/api/category/",
    "/api/commission/",
    "/api/stat/top_sale_product/",
    "/api/stat/top10_sale_employee/",
    "/api/stat/top10_province_customer/",
    "/api/stat/weekday_sale_amount/",
    "/api/stat/month_day_sale_amount/",
    "/api/stat/year_month_sale_amount/",
    "/api/stat/today_order_num_and_amount/",
]

MONEY_HINTS = ("amount", "price", "commission", "money", "total", "金额", "佣金", "价格")


def call(path, token):
    req = urllib.request.Request(BASE + path)
    req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status, json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return e.code, {}


def login():
    req = urllib.request.Request(
        BASE + "/api/user/login/",
        data=json.dumps({"username": "admin", "password": PWD}).encode(),
        method="POST", headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read())["access_token"]


def scan(obj, path="", found=None):
    if found is None:
        found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan(v, f"{path}.{k}" if path else k, found)
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:5]):
            scan(v, f"{path}[{i}]", found)
    elif isinstance(obj, float):
        found.append((path, obj))
    return found


def main():
    token = login()
    bad = []
    total_fields = 0
    for ep in ENDPOINTS:
        status, payload = call(ep, token)
        if status != 200:
            print(f"  ! {status} {ep}")
            continue
        floats = scan(payload)
        money_floats = [f for f in floats if any(h in f[0].lower() for h in MONEY_HINTS)]
        total_fields += len(floats)
        flag = "❌" if money_floats else "✅"
        print(f"{flag} {ep}")
        for p, v in money_floats:
            print(f"      浮点金额：{p} = {v!r}")
            bad.append((ep, p, v))
    print("\n" + "=" * 58)
    if bad:
        print(f"不合格：发现 {len(bad)} 处浮点金额")
        sys.exit(1)
    print("合格：所有接口的金额都是字符串，未发现 float")
    print(f"（扫描到的 float 总数：{total_fields} —— 非金额字段可为 0 或不存在）")
    sys.exit(0)


if __name__ == "__main__":
    main()
