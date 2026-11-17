"""工具注册表：循环唯一的外部依赖，也是"换一套工具 = 换一个场景"的插槽。

【为什么单独抽这一个文件】
    core.py 的循环本身不认识任何业务工具，它只要求四样东西存在：
        TOOLS            给模型看的工具说明书（JSON Schema 列表）
        TOOL_DISPATCH    名字 → 真实执行函数的映射
        CONFIRM_REQUIRED 哪些工具属于"危险操作"，执行前要人工确认
        CONFIRM_PREVIEW  确认前给用户看的"人话摘要"（用真实数据算，见下）

    这四样默认都是空的（这个文件），启动时由 bridge.py 注入 CRM 的真实工具：

        import agent.core as core
        core.TOOLS            = crm.tools.TOOLS
        core.TOOL_DISPATCH    = crm.tools.TOOL_DISPATCH
        core.CONFIRM_REQUIRED = crm.tools.CONFIRM_REQUIRED
        core.CONFIRM_PREVIEW  = crm.tools.CONFIRM_PREVIEW

    所以"同一套循环、换一套工具、换一个业务系统"不需要改 core.py 一行。

【CONFIRM_PREVIEW 为什么必须由代码算】
    确认框要写"即将在客户「李纯风」名下新增一条跟踪记录，方式：微信"这种话。
    这句话不能交给模型生成 —— 模型会记错客户名、编错金额。
    它必须是执行前用真实数据查出来的，模型只负责提议参数，不负责描述后果。

【想接自己的系统】
    照 crm/tools.py 的四段式写一份（schema / dispatch / confirm / preview），
    在启动处替换上面四个变量即可。循环、确认、轮数熔断都不用管。
"""

TOOLS: list[dict] = []
TOOL_DISPATCH: dict = {}
CONFIRM_REQUIRED: set[str] = set()
# name → fn(**args) → {"标题": str, "字段": [[名, 值], ...], "提示": str, "警告": str}
# 允许抛异常：循环那边会退化处理（只显示参数），不会挡住确认流程
CONFIRM_PREVIEW: dict = {}
