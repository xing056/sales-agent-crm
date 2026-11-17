"""配置：LLM 参数与目标系统地址，全部来自本仓库内的 .env。

【为什么是"就近读取"】
    不写死任何绝对路径：先找 agent-server/.env，再找仓库根的 .env，
    都没有就用下面的默认值 —— 把整个文件夹复制走即可独立运行。

【优先级】
    进程环境变量  >  .env 文件  >  代码里的默认值
    临时换模型/换 Key 不用改文件，直接设环境变量即可。
"""

import os
from pathlib import Path

# agent-server/  和  仓库根（backend/ frontend/ agent-server/ 的上一层）
BASE_DIR = Path(__file__).resolve().parent
ROOT_DIR = BASE_DIR.parent
ENV_CANDIDATES = (BASE_DIR / ".env", ROOT_DIR / ".env")


def _parse_env(path: Path) -> dict:
    """极简 .env 解析：跳过注释行，只取第一处 '='，去掉成对引号。

    不装 python-dotenv 是因为只有这么点需求，少一个依赖少一处坑。
    """
    data = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
            value = value[1:-1]
        data[key.strip()] = value
    return data


def _load_env() -> dict:
    for path in ENV_CANDIDATES:
        data = _parse_env(path)
        if data:
            return data
    return {}


ENV = _load_env()
ENV_FILE = next((p for p in ENV_CANDIDATES if p.exists()), None)


def get(key: str, default: str = "") -> str:
    """环境变量优先，其次 .env，最后默认值。"""
    if key in os.environ:
        return os.environ[key]
    return ENV.get(key, default)


# ---------- 被智能体操作的目标系统（Django 后端） ----------
DJRBAC_BASE = get("DJRBAC_BASE", "http://127.0.0.1:8000").rstrip("/")
# 独立页面（agent-server/web/index.html）切账号演示时用的统一密码
# 只有在 AGENT_ALLOW_USER_LOGIN=true 时才会被用到
DEMO_PASSWORD = get("DJRBAC_PASSWORD", "")

# ---------- 身份校验 ----------
# 默认 false：一律要求前端传登录令牌（token），不接受"只报账号名"。
# 为什么必须这样：如果只凭账号名就能建会话，智能体会用自己的服务端密码
# 去登录目标系统 —— 等于把"以任意账号读取全库"的能力开在了一个 HTTP 端口上，
# 任何能访问到 8200 的人（包括恶意网页里的跨源请求）都能用。
# 只有在纯本机演示、且不想从后台管理系统里打开时，才临时设成 true。
ALLOW_USER_LOGIN = get("AGENT_ALLOW_USER_LOGIN", "false").lower() in ("1", "true", "yes", "on")

# 会话回收：空闲超过该秒数即丢弃；同时限制内存里最多保留多少个会话
SESSION_TTL = int(get("AGENT_SESSION_TTL", "1800"))
MAX_SESSIONS = int(get("AGENT_MAX_SESSIONS", "100"))

# ---------- 用量上报 ----------
# 与 backend/.env 保持同一个值。留空 = 不上报（接口那边也会拒绝），
# 这样"没配"和"配错"表现得一样明显，不会静默地什么都不记。
INTERNAL_API_KEY = get("INTERNAL_API_KEY", "")

# 单账号每日 token 预算。0 = 不限制（默认）。
# 为什么默认关：这是演示环境，配一个小数字会让演示中途被自己拦下来。
# 真要用，在 .env 里写 LLM_DAILY_BUDGET_TOKENS=200000 之类。
LLM_DAILY_BUDGET_TOKENS = int(get("LLM_DAILY_BUDGET_TOKENS", "0") or 0)

# 上报接口超时（秒）。调小是故意的：看板晚几秒没关系，对话卡住不行。
REPORT_TIMEOUT = float(get("AGENT_REPORT_TIMEOUT", "3"))

# 独立页面顶栏可切换的身份：用来直观演示 RBAC 权限与行级隔离
DEMO_USERS = [
    {"username": "admin", "label": "admin（超级管理员）"},
    {"username": "user001", "label": "user001（普通销售）"},
    {"username": "zhengping", "label": "zhengping（无客户权限）"},
]

# ---------- 智能体服务自身 ----------
SERVER_HOST = get("AGENT_HOST", "127.0.0.1")
SERVER_PORT = int(get("AGENT_PORT", "8200"))
# 允许跨域访问的前端地址（开发服务器/预览服务器）
ALLOWED_ORIGINS = [
    o.strip() for o in get(
        "AGENT_ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,"
        "http://localhost:5180,http://127.0.0.1:5180,"
        "http://localhost:4173,http://127.0.0.1:4173",
    ).split(",") if o.strip()
]


class LLMConfig:
    """模型接入参数。任何 OpenAI 协议端点都能用（百炼 / DeepSeek / 智谱 / 本地 vLLM）。"""

    def __init__(self):
        # 环境变量优先，方便临时换模型/换 Key 而不改文件
        self.api_key = get("LLM_API_KEY", "")
        self.base_url = get("LLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4")
        self.model = get("LLM_MODEL", "glm-4.7")
        # core.py 里读的是进程环境变量，这里同步过去
        thinking = get("LLM_DISABLE_THINKING", "")
        if thinking and "LLM_DISABLE_THINKING" not in os.environ:
            os.environ["LLM_DISABLE_THINKING"] = thinking

    @property
    def ready(self) -> bool:
        return bool(self.api_key and self.base_url and self.model)
