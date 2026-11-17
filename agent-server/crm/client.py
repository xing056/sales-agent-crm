"""dj-rbac 接口客户端。

设计要点：智能体**以真实登录用户的身份**调用后端接口（带 JWT），
而不是拿一个超级管理员令牌绕过去。这样做的好处是：

  · RBAC 权限校验天然生效 —— 模型调不动用户本人也没权限的接口
  · 行级隔离天然生效 —— of_me 返回什么，智能体就只能看到什么
  · 出错信息是后端真实返回，模型不会拿到"假数据"

换句话说：智能体没有特权，它只是一个手速很快的普通员工。
"""

import json
import urllib.error
import urllib.parse
import urllib.request


class ApiError(Exception):
    def __init__(self, status: int, payload):
        self.status = status
        self.payload = payload
        super().__init__(f"HTTP {status}: {payload}")


class CrmClient:
    def __init__(self, base_url: str, username: str = "", password: str = "",
                 token: str | None = None, profile: dict | None = None):
        self.base_url = base_url.rstrip("/")
        self.username = username
        self.password = password
        # 两种模式：
        #   1) 独立页面：给账号密码，自己登录拿令牌
        #   2) 嵌在后台管理里：前端把已登录的令牌直接传进来，不再重复登录
        #      —— 这样智能体的身份就是"当前坐在电脑前的那个人"，不需要选身份
        self._token = token
        self.profile = profile or {}

    # ---------- 底层 ----------

    def _raw(self, method, path, body=None, params=None, token=None):
        url = self.base_url + path
        if params:
            url += "?" + urllib.parse.urlencode(params)
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(url, data=data, method=method)
        req.add_header("Content-Type", "application/json")
        if token:
            req.add_header("Authorization", "Bearer " + token)
        try:
            with urllib.request.urlopen(req, timeout=20) as resp:
                raw = resp.read()
                return resp.status, (json.loads(raw) if raw else {})
        except urllib.error.HTTPError as exc:
            raw = exc.read()
            try:
                payload = json.loads(raw) if raw else {}
            except Exception:
                payload = {"detail": raw.decode("utf-8", "replace")[:200]}
            return exc.code, payload
        except Exception as exc:  # 连接失败等
            return -1, {"detail": f"无法连接后端 {self.base_url}：{exc}"}

    def login(self):
        status, payload = self._raw(
            "POST", "/api/user/login/",
            {"username": self.username, "password": self.password},
        )
        if status != 200 or not payload.get("access_token"):
            raise ApiError(status, payload.get("message") or payload)
        self._token = payload["access_token"]
        self.profile = payload.get("data") or {}
        return payload

    def call(self, method, path, body=None, params=None):
        if not self._token:
            self.login()
        status, payload = self._raw(method, path, body, params, self._token)
        if status == 401 and self.password:
            # 只有"自己登录"的模式才能重登；令牌是前端传进来的，重登不了，
            # 直接把 401 交给工具层，让模型告诉用户"登录状态已过期，请重新登录"
            self.login()
            status, payload = self._raw(method, path, body, params, self._token)
        return status, payload

    # ---------- 上层 ----------

    def list_all(self, path, params=None, max_rows=400):
        """取全量列表（后端单页最多 100 条，这里自动翻页）。

        返回 (status, meta, rows)。status != 200 时 rows 为空、meta 带错误信息，
        由工具层决定怎么向模型解释（例如 403 → 权限不足）。
        """
        rows, page = [], 1
        total = None
        while True:
            query = dict(params or {})
            query.update({"page": page, "size": 100})
            status, payload = self.call("GET", path, params=query)
            if status != 200:
                return status, payload if isinstance(payload, dict) else {"detail": str(payload)}, []
            if isinstance(payload, list):  # 非分页接口
                return 200, {"count": len(payload)}, payload
            total = payload.get("count", 0)
            batch = payload.get("results") or []
            rows.extend(batch)
            if not batch or len(rows) >= total or len(rows) >= max_rows:
                break
            page += 1
        return 200, {"count": total, "fetched": len(rows)}, rows

    def get_one(self, path, params=None):
        status, payload = self.call("GET", path, params=params)
        return status, payload
