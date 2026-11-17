"""零依赖 HTTP 服务：聊天页 + 三个接口。

为什么不用 FastAPI：这个环境只是演示入口，用标准库就够，
少一层依赖就少一处启动失败的可能。要换成 FastAPI 也只是换壳，
bridge.py 和 crm/ 都不用动。
"""

import json
import threading
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from bridge import AgentRuntime, BudgetExceeded
from config import (
    ALLOWED_ORIGINS,
    ALLOW_USER_LOGIN,
    DEMO_USERS,
    DJRBAC_BASE,
    ENV_FILE,
    LLMConfig,
    SERVER_HOST,
    SERVER_PORT,
)
from crm.client import ApiError

WEB_DIR = Path(__file__).parent / "web"
runtime = AgentRuntime()
_chat_lock = threading.Lock()  # 演示用：串行处理，避免同一会话被并发写乱


class Handler(BaseHTTPRequestHandler):
    server_version = "sales-agent-crm/1.0"

    # ---------- 工具方法 ----------

    def _cors_origin(self) -> str | None:
        """只对白名单来源回显 Origin；不在白名单里的不给这个头。

        为什么不再"其余放行为 *"：带 * 的响应意味着任何网页都能跨源读到
        本服务的返回内容 —— 而本服务能用令牌读全库。回显具体来源才能既
        支持前端跨端口调用，又不把响应暴露给陌生站点。
        """
        origin = self.headers.get("Origin") or ""
        return origin if origin in ALLOWED_ORIGINS else None

    def _cors_headers(self):
        origin = self._cors_origin()
        if origin:
            self.send_header("Access-Control-Allow-Origin", origin)
            self.send_header("Vary", "Origin")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")

    def _json(self, payload, status=200):
        body = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        # 嵌在后台管理里时是跨端口调用，需要放行 CORS
        self._cors_headers()
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_response(204)
        self._cors_headers()
        self.send_header("Content-Length", "0")
        self.end_headers()

    def _read_json(self):
        length = int(self.headers.get("Content-Length") or 0)
        if not length:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def log_message(self, fmt, *args):  # 只打一行，别刷屏
        print(f"[web] {self.address_string()} {fmt % args}")

    # ---------- 路由 ----------

    def do_GET(self):
        path = self.path.split("?")[0]
        if path in ("/", "/index.html"):
            html = (WEB_DIR / "index.html").read_text(encoding="utf-8")
            data = html.encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
            return
        if path == "/api/info":
            self._json({
                # 演示账号列表只在开启"账号名登录"时才下发，否则没有用处
                "users": DEMO_USERS if ALLOW_USER_LOGIN else [],
                "target": DJRBAC_BASE,
                "llm": {
                    "model": runtime.llm.model,
                    "base_url": runtime.llm.base_url,
                    "ready": runtime.ready(),
                },
            })
            return
        self._json({"error": "not found"}, 404)

    def do_POST(self):
        path = self.path.split("?")[0]
        try:
            body = self._read_json()
        except Exception as exc:  # noqa: BLE001
            self._json({"error": f"请求体解析失败：{exc}"}, 400)
            return

        if not runtime.ready():
            self._json({"error": "LLM 未配置：请把 agent-server/.env.example 复制为 .env 并填 LLM_API_KEY"}, 500)
            return

        try:
            if path == "/api/chat":
                self._handle_chat(body)
            elif path == "/api/confirm":
                self._handle_confirm(body)
            elif path == "/api/reset":
                ident = self._require_identity(body)
                if ident is None:
                    return
                runtime.reset(username=ident["username"], token=ident["token"])
                self._json({"ok": True})
            elif path == "/api/usage":
                # 为什么是 POST 而不是 GET：复用同一套身份校验（令牌在请求体里），
                # 不为了"语义正确"再开一条读 query string 的鉴权路径 ——
                # 那才是漏洞的常见来源。
                ident = self._require_identity(body)
                if ident is None:
                    return
                self._json(runtime.usage(username=ident["username"], token=ident["token"]))
            else:
                self._json({"error": "not found"}, 404)
        except PermissionError as exc:
            # 身份校验的兜底：bridge 层拒绝时按 401 回，不暴露服务端细节
            self._json({"error": str(exc)}, 401)
        except BudgetExceeded as exc:
            # 429 而不是 500：这不是故障，是"额度用完了"，
            # 前端要能据此给出"明天再来"而不是"系统出错"。
            self._json({"error": str(exc), "code": "budget_exceeded"}, 429)
        except ApiError as exc:
            self._json({"error": f"登录 dj-rbac 失败：{exc.payload}"}, 502)
        except Exception:  # noqa: BLE001
            # 完整堆栈只进控制台。异常原文里可能带着内部地址、文件路径、
            # 甚至上游响应体 —— 那些不该跟着 HTTP 响应跑到浏览器里。
            traceback.print_exc()
            self._json({"error": "服务端异常，请查看 agent-server 控制台日志"}, 500)

    # ---------- 业务 ----------

    def _identity(self, body):
        """两种身份来源：嵌在后台管理里传 token；独立页面传 user。

        注意：user 这条路径默认是关的（见 config.ALLOW_USER_LOGIN）——
        它会让服务端拿公共密码替对方登录，等于匿名获得任意账号的读取权。
        """
        return {
            "username": body.get("user"),
            "token": body.get("token"),
            "profile": body.get("profile"),
            "page_name": body.get("page_name"),
            "focus": body.get("focus"),
        }

    def _require_identity(self, body):
        """校验身份来源，不通过就直接回 401 并返回 None。

        令牌由前端从登录态里带过来，后端每次工具调用都以它为准 ——
        所以"能不能看到数据"取决于这个令牌在 dj-rbac 里有什么权限，
        而不是取决于请求体里自称是谁。
        """
        if body.get("token"):
            return self._identity(body)
        if ALLOW_USER_LOGIN and body.get("user"):
            return self._identity(body)
        self._json(
            {
                "error": "缺少登录令牌：请从后台管理系统内打开智能体（会自动带上登录凭证）；"
                "独立演示页面需要先在 agent-server/.env 里设置 AGENT_ALLOW_USER_LOGIN=true"
            },
            401,
        )
        return None

    def _handle_chat(self, body):
        text = (body.get("text") or "").strip()
        if not text:
            self._json({"error": "消息不能为空"}, 400)
            return
        ident = self._require_identity(body)
        if ident is None:
            return
        with _chat_lock:
            events = runtime.chat(text, **ident)
        self._json({"events": events})

    def _handle_confirm(self, body):
        ident = self._require_identity(body)
        if ident is None:
            return
        with _chat_lock:
            events = runtime.confirm(bool(body.get("yes")), **ident)
        self._json({"events": events})


def main():
    llm = LLMConfig()
    print("=" * 62)
    print("CRM 智能体（手写循环 + dj-rbac 工具）")
    print(f"  后端接口：{DJRBAC_BASE}")
    print(f"  对话模型：{llm.model} @ {llm.base_url}")
    print(f"  配置文件：{ENV_FILE or '未找到 .env（仅使用默认值）'}")
    print(f"  Key 就绪：{'是' if llm.ready else '否 —— 请复制 .env.example 为 .env 并填写 LLM_API_KEY'}")
    print(f"  打开页面：http://{SERVER_HOST}:{SERVER_PORT}/")
    print("=" * 62)
    ThreadingHTTPServer((SERVER_HOST, SERVER_PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
