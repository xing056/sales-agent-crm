"""命令行试跑：直接对智能体提问，打印工具调用链路。"""
import json
import sys
import urllib.request

BASE = "http://127.0.0.1:8200"


def post(path, body):
    req = urllib.request.Request(
        BASE + path, data=json.dumps(body).encode(), method="POST",
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def run(user, text, auto_confirm=None):
    print(f"\n{'='*66}\n[{user}] 用户：{text}")
    data = post("/api/chat", {"user": user, "text": text})
    if data.get("error"):
        print("错误：", data["error"])
        return
    for ev in data["events"]:
        if ev["type"] == "tool_call":
            print(f"  → 调用工具 {ev['name']}  参数={json.dumps(ev['args'], ensure_ascii=False)}")
        elif ev["type"] == "tool_result":
            brief = json.dumps(ev["result"], ensure_ascii=False)
            print(f"    ← 返回 {brief[:220]}{'...' if len(brief) > 220 else ''}")
        elif ev["type"] == "confirm":
            print(f"  ⏸ 待确认：{ev['name']} {json.dumps(ev['args'], ensure_ascii=False)}")
            if auto_confirm is not None:
                d2 = post("/api/confirm", {"user": user, "yes": auto_confirm})
                for e2 in d2.get("events", []):
                    if e2["type"] == "tool_result":
                        print(f"    ← 确认后返回 {json.dumps(e2['result'], ensure_ascii=False)[:200]}")
                    elif e2["type"] == "answer":
                        print(f"  回答：{e2['content']}")
        elif ev["type"] == "answer":
            print(f"  回答：{ev['content']}")


if __name__ == "__main__":
    user = sys.argv[1] if len(sys.argv) > 1 else "admin"
    question = sys.argv[2] if len(sys.argv) > 2 else "我是谁？我负责的客户有几个？"
    run(user, question)
