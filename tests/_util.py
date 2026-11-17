"""验收脚本共用的 HTTP 与输出工具。只用标准库，不引入任何依赖。

设计原则：
  · 目标地址、账号密码全部可配置（环境变量优先），不写死
  · 断言失败要能体现在进程退出码上，方便 CI 或 .bat 调用
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Windows 控制台默认 GBK，打印中文/符号会炸，先切成 utf-8
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:  # noqa: BLE001  Python < 3.7 或不支持 reconfigure 的环境
    pass

BASE = os.getenv("DJRBAC_BASE", "http://127.0.0.1:8000").rstrip("/")


def _find_password() -> str:
    """密码来源优先级：环境变量 > agent-server/.env > backend/.env。

    仓库里不存密码，所以脚本要去读本地 .env（它就是照着 README 配的那份）。
    """
    if os.getenv("DJRBAC_PASSWORD"):
        return os.environ["DJRBAC_PASSWORD"]

    here = Path(__file__).resolve().parent
    for candidate in (
        here.parent / "agent-server" / ".env",
        here.parent / "backend" / ".env",
    ):
        if not candidate.exists():
            continue
        for line in candidate.read_text(encoding="utf-8", errors="replace").splitlines():
            line = line.strip()
            if line.startswith("DJRBAC_PASSWORD="):
                return line.split("=", 1)[1].strip().strip("\"'")
    return ""


PASSWORD = _find_password()


def call(path, method="GET", body=None, token=None, timeout=40):
    """发一个请求，返回 (状态码, 解析后的响应体)。不抛异常，由调用方断言。"""
    url = BASE + path
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", "Bearer " + token)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return resp.status, _parse(raw)
    except urllib.error.HTTPError as exc:
        return exc.code, _parse(exc.read())
    except Exception as exc:  # noqa: BLE001  连不上/超时
        return -1, {"_error": str(exc)}


def _parse(raw: bytes):
    try:
        return json.loads(raw or b"{}")
    except Exception:  # noqa: BLE001
        return {"_raw": raw.decode("utf-8", "replace")[:200]}


def login(username: str):
    """登录拿 access_token，失败返回 None 并把原因打出来。"""
    status, data = call("/api/user/login/", "POST", {"username": username, "password": PASSWORD})
    if status != 200:
        print(f"  ! 登录失败 {username}: HTTP {status} {data}")
        return None
    return data.get("access_token")


def count_of(payload):
    """列表接口的条数：DRF 分页返回 count，未分页返回数组长度。"""
    if isinstance(payload, dict):
        if "count" in payload:
            return payload["count"]
        if isinstance(payload.get("results"), list):
            return len(payload["results"])
    if isinstance(payload, list):
        return len(payload)
    return None


# ---------- 输出 ----------

_failures: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> bool:
    """一条断言。失败会记下来，最后统一影响退出码。"""
    mark = "PASS" if ok else "FAIL"
    print(f"  [{mark}] {label}" + (f"  —— {detail}" if detail else ""))
    if not ok:
        _failures.append(label)
    return ok


def section(title: str):
    print(f"\n{title}")


def summary(title: str) -> int:
    """打印结论并返回退出码（0 = 全过）。"""
    print("\n" + "-" * 62)
    if _failures:
        print(f"{title}：{len(_failures)} 项失败")
        for f in _failures:
            print(f"  · {f}")
        return 1
    print(f"{title}：全部通过")
    return 0


def find_floats(obj, path="root"):
    """递归找出所有浮点数。金额一旦是 float，说明精度链路被破坏了。"""
    found = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            found += find_floats(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            found += find_floats(v, f"{path}[{i}]")
    elif isinstance(obj, float):
        found.append(path)
    return found
