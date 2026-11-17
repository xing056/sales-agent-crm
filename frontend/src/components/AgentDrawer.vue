<template>
  <div>
    <!-- 悬浮入口 -->
    <div class="agent-fab" :class="{ open: visible }" @click="toggle" :title="visible ? '收起助手' : '打开 AI 助手'">
      <el-icon v-if="!visible" :size="22"><ChatDotRound /></el-icon>
      <el-icon v-else :size="20"><Close /></el-icon>
      <span v-if="!visible" class="fab-text">AI 助手</span>
    </div>

    <!-- 对话抽屉 -->
    <el-drawer v-model="visible" :with-header="false" size="440px" :append-to-body="true" class="agent-drawer">
      <div class="pane">
        <div class="pane-head">
          <div>
            <div class="pane-title">CRM 助手</div>
            <div class="pane-sub">
              以 {{ loginInfo.username || '当前账号' }} 的身份操作 · {{ currentPage }}
            </div>
          </div>
          <el-button link size="small" @click="clearChat">清空</el-button>
        </div>

        <div ref="scrollBox" class="pane-body">
          <div v-if="!blocks.length" class="empty">
            <div class="empty-tip">
              我可以查客户、查订单、看跟踪记录和销售统计，<br />
              也能帮你补一条跟踪记录。所有数据都从系统实时查询。
            </div>
            <div class="chips">
              <span v-for="q in examples" :key="q" class="chip" @click="ask(q)">{{ q }}</span>
            </div>
          </div>

          <template v-for="(b, i) in blocks" :key="i">
            <div v-if="b.role === 'user'" class="row right">
              <div class="bubble user">{{ b.text }}</div>
            </div>

            <div v-else-if="b.type === 'answer'" class="row">
              <div class="avatar">AI</div>
              <div class="bubble bot">{{ b.text }}</div>
            </div>

            <div v-else-if="b.type === 'tool'" class="tool" :class="{ pending: b.running }">
              <div class="tool-head" @click="b.open = !b.open">
                <span class="tag">{{ b.running ? '调用中' : '工具调用' }}</span>
                <span class="tool-name">{{ b.name }}</span>
                <span class="arrow">{{ b.open ? '收起 ▴' : '展开 ▾' }}</span>
              </div>
              <pre v-show="b.open">{{ toolText(b) }}</pre>
            </div>

            <div v-else-if="b.type === 'confirm'" class="confirm">
              <div class="confirm-q">
                <template v-if="b.summary && b.summary.标题">{{ b.summary.标题 }}</template>
                <template v-else>即将执行写操作 <b>{{ b.name }}</b>，是否确认？</template>
              </div>

              <!-- 摘要由后端用真实数据算出来，不是模型编的 -->
              <div v-if="b.summary && b.summary.字段" class="cf-list">
                <div v-for="row in b.summary.字段" :key="row[0]" class="cf-row">
                  <span class="cf-k">{{ row[0] }}</span>
                  <span class="cf-v">{{ row[1] }}</span>
                </div>
              </div>
              <div v-if="b.summary && b.summary.提示" class="cf-tip">{{ b.summary.提示 }}</div>
              <div v-if="b.summary && b.summary.警告" class="cf-warn">{{ b.summary.警告 }}</div>

              <!-- 没有摘要时（或想看细节时）退回原始参数 -->
              <details v-if="!b.summary" class="cf-raw">
                <summary>原始参数</summary>
                <pre>{{ JSON.stringify(b.args, null, 2) }}</pre>
              </details>

              <div v-if="!b.resolved" class="acts">
                <el-button type="warning" size="small" @click="doConfirm(b, true)">确认执行</el-button>
                <el-button size="small" @click="doConfirm(b, false)">取消</el-button>
              </div>
              <div v-else class="resolved">{{ b.resolvedText }}</div>
            </div>

            <div v-else-if="b.type === 'error'" class="row">
              <div class="avatar err">!</div>
              <div class="bubble err">{{ b.text }}</div>
            </div>
          </template>

          <div v-if="loading" class="row">
            <div class="avatar">AI</div>
            <div class="bubble bot thinking">
              正在处理<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span>
            </div>
          </div>
        </div>

        <div class="pane-foot">
          <el-input
            v-model="draft"
            type="textarea"
            :rows="2"
            resize="none"
            placeholder="例如：这个客户有哪些订单？"
            @keydown.enter.exact.prevent="send"
          />
          <el-button type="primary" :disabled="loading || !draft.trim()" @click="send">发送</el-button>
        </div>
      </div>
    </el-drawer>
  </div>
</template>

<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { storeToRefs } from 'pinia'
import { ChatDotRound, Close } from '@element-plus/icons-vue'
import useUserStore from '@/stores/user'

const userStore = useUserStore()
const { loginInfo, accessToken } = storeToRefs(userStore)
const route = useRoute()

// 智能体服务地址：默认"跟当前页面同主机、8200 端口"，
// 部署到别的机器/端口时用环境变量 VITE_AGENT_BASE 覆盖，不用改代码。
const AGENT_BASE =
  import.meta.env.VITE_AGENT_BASE || `${location.protocol}//${location.hostname}:8200`

const visible = ref(false)
const loading = ref(false)
const draft = ref('')
const blocks = ref([])
const scrollBox = ref(null)

/* ---------- 页面上下文 ----------
   这是嵌进后台管理才拿得到的东西：用户现在在哪个模块、
   在不在某个详情页。独立页面拿不到，只能靠用户自己说。 */
const PAGE_NAMES = {
  perm: '权限管理', role: '角色管理', menu: '菜单管理', user: '用户管理',
  department: '部门管理', departmentEmp: '部门员工', position: '岗位管理',
  employee: '员工管理', empDetail: '员工详情', profile: '个人资料',
  customerSource: '客户来源', customer: '客户管理', customerDetail: '客户详情',
  customerTracking: '客户跟踪', customerOfMe: '我的客户',
  allCustomerTracking: '客户跟踪记录', category: '商品分类', product: '商品管理',
  saleOrder: '销售订单', saleOrderDetail: '订单详情', orderCreate: '新建订单',
  stat: '数据统计', commission: '员工销售提成', myCommission: '我的销售提成',
}
const currentPage = computed(() => PAGE_NAMES[route.name] || route.name || '后台管理')

// 详情页把"当前这条记录"带给智能体
const focus = computed(() => {
  const id = Number(route.params?.id)
  if (!id) return null
  if (route.name === 'customerDetail' || route.name === 'customerTracking') {
    return { type: '客户', id }
  }
  if (route.name === 'saleOrderDetail') return { type: '订单', id }
  if (route.name === 'empDetail') return { type: '员工', id }
  return null
})

const examples = computed(() => {
  const f = focus.value
  if (f && f.type === '客户') {
    return ['这个客户是谁在跟？', '这个客户有哪些订单？', '这个客户最近跟进到哪一步了？']
  }
  if (f && f.type === '订单') {
    return ['这笔订单的明细是什么？', '这个客户还有别的订单吗？']
  }
  return ['我负责的客户有几个？', '客户总数是多少？', '本月每日销售额怎么样？', '查一下韩楚风的订单']
})

/* ---------- 渲染工具 ---------- */
function toolText(b) {
  const args = JSON.stringify(b.args ?? {}, null, 2)
  const res = b.result === undefined ? '（执行中…）' : JSON.stringify(b.result, null, 2)
  return `参数：\n${args}\n\n返回：\n${res}`
}

function scrollBottom() {
  nextTick(() => {
    if (scrollBox.value) scrollBox.value.scrollTop = scrollBox.value.scrollHeight
  })
}
watch(blocks, scrollBottom, { deep: true })

function toggle() {
  visible.value = !visible.value
}

function clearChat() {
  blocks.value = []
  post('/api/reset', {}).catch(() => {})
}

/* ---------- 请求 ---------- */
async function post(path, body) {
  const resp = await fetch(AGENT_BASE + path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      token: accessToken.value,
      user: loginInfo.value?.username,
      profile: loginInfo.value,
      page_name: currentPage.value,
      focus: focus.value,
      ...body,
    }),
  })
  const data = await resp.json()
  if (data.error) throw new Error(data.error)
  return data
}

function applyEvents(events) {
  let lastTool = null
  for (const ev of events || []) {
    if (ev.type === 'tool_call') {
      const block = { type: 'tool', name: ev.name, args: ev.args, running: true, open: false }
      blocks.value.push(block)
      lastTool = block
    } else if (ev.type === 'tool_result') {
      const target = lastTool || { type: 'tool', name: ev.name, args: {}, open: false }
      target.result = ev.result
      target.running = false
      if (!lastTool) blocks.value.push(target)
    } else if (ev.type === 'confirm') {
      blocks.value.push({
        type: 'confirm', name: ev.name, args: ev.args,
        summary: ev.summary || null, resolved: false,
      })
    } else if (ev.type === 'answer') {
      blocks.value.push({ type: 'answer', text: ev.content })
    }
  }
}

async function send() {
  const text = draft.value.trim()
  if (!text || loading.value) return
  draft.value = ''
  blocks.value.push({ role: 'user', text })
  loading.value = true
  try {
    const data = await post('/api/chat', { text })
    applyEvents(data.events)
  } catch (err) {
    blocks.value.push({ type: 'error', text: `调用失败：${err.message}。请确认智能体服务已启动（${AGENT_BASE}）` })
  } finally {
    loading.value = false
  }
}

function ask(q) {
  draft.value = q
  send()
}

async function doConfirm(block, yes) {
  block.resolved = true
  block.resolvedText = yes ? '已确认，正在执行…' : '已取消本次操作'
  loading.value = true
  try {
    const data = await post('/api/confirm', { yes })
    applyEvents(data.events)
  } catch (err) {
    blocks.value.push({ type: 'error', text: `执行失败：${err.message}` })
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.agent-fab {
  position: fixed; right: 26px; bottom: 26px; z-index: 2000;
  display: flex; align-items: center; gap: 6px;
  height: 48px; padding: 0 18px; border-radius: 24px;
  background: linear-gradient(135deg, var(--el-color-primary), var(--el-color-primary-dark-2));
  color: #fff; cursor: pointer; user-select: none;
  box-shadow: 0 6px 18px rgba(64, 158, 255, 0.42);
  transition: transform .15s ease;
}
.agent-fab:hover { transform: translateY(-2px); }
.agent-fab.open { padding: 0; width: 48px; justify-content: center; border-radius: 50%; }
.fab-text { font-size: 14px; font-weight: 500; }

.pane { display: flex; flex-direction: column; height: 100%; margin: -20px; }
.pane-head {
  display: flex; align-items: center; justify-content: space-between;
  padding: 14px 18px; border-bottom: 1px solid var(--app-border); background: var(--app-bg-card);
}
.pane-title { font-size: 15px; font-weight: 600; color: var(--app-text); }
.pane-sub { font-size: 12px; color: var(--app-text-sub); margin-top: 3px; }

.pane-body { flex: 1; overflow-y: auto; padding: 16px; background: var(--app-bg-page); }
.empty { padding: 26px 8px; }
.empty-tip { font-size: 13px; color: var(--el-text-color-regular); line-height: 1.9; text-align: center; }
.chips { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; margin-top: 16px; }
.chip {
  font-size: 12px; color: var(--el-color-primary); background: var(--el-color-primary-light-9); border: 1px solid var(--el-color-primary-light-8);
  border-radius: 14px; padding: 5px 12px; cursor: pointer;
}
.chip:hover { background: var(--el-color-primary-light-8); }

.row { display: flex; gap: 8px; margin-bottom: 12px; align-items: flex-start; }
.row.right { justify-content: flex-end; }
.avatar {
  width: 28px; height: 28px; flex: 0 0 28px; border-radius: 50%;
  background: #409eff; color: #fff; font-size: 11px; font-weight: 600;
  display: flex; align-items: center; justify-content: center;
}
.avatar.err { background: var(--el-color-danger); }
.bubble {
  padding: 9px 13px; border-radius: 10px; font-size: 13px; line-height: 1.75;
  white-space: pre-wrap; word-break: break-word; max-width: 330px;
}
.bubble.user { background: #409eff; color: #fff; border-bottom-right-radius: 3px; }
.bubble.bot { background: var(--app-bg-card); border: 1px solid var(--app-border); border-bottom-left-radius: 3px; color: var(--app-text); }
.bubble.err { background: var(--app-err-bg); border: 1px solid var(--app-err-border); color: var(--app-err-text); }
.thinking .dot { animation: blink 1.2s infinite; }
@keyframes blink { 0%,80%,100%{opacity:.2} 40%{opacity:1} }

.tool {
  background: var(--app-bg-card); border: 1px solid var(--app-border); border-left: 3px solid var(--el-color-success);
  border-radius: 8px; padding: 9px 11px; margin-bottom: 12px; font-size: 12px;
}
.tool.pending { border-left-color: var(--el-color-warning); }
.tool-head { display: flex; align-items: center; gap: 8px; cursor: pointer; }
.tag {
  font-size: 11px; padding: 1px 6px; border-radius: 4px;
  background: var(--app-ok-bg); color: var(--app-ok-text);
}
.tool.pending .tag { background: var(--app-warn-bg); color: var(--app-warn-text); }
.tool-name { font-family: ui-monospace, Consolas, monospace; color: var(--app-text); font-weight: 600; }
.arrow { margin-left: auto; color: var(--app-text-sub); font-size: 11px; }
.tool pre {
  margin: 8px 0 0; padding: 8px; background: var(--app-bg-muted); border-radius: 6px;
  font-size: 11px; line-height: 1.6; max-height: 220px; overflow: auto;
  white-space: pre-wrap; word-break: break-all; color: var(--app-text);
  font-family: ui-monospace, Consolas, monospace;
}

.confirm {
  background: var(--app-bg-card); border: 1px solid var(--app-warn-border); border-left: 3px solid var(--el-color-warning);
  border-radius: 8px; padding: 11px 13px; margin-bottom: 12px; font-size: 13px;
}
.confirm-q { margin-bottom: 8px; color: var(--app-text); }
.confirm pre {
  margin: 0 0 10px; padding: 8px; background: var(--app-bg-muted); border-radius: 6px;
  font-size: 11px; color: var(--app-text); white-space: pre-wrap;
  font-family: ui-monospace, Consolas, monospace;
}
.acts { display: flex; gap: 8px; }
.resolved { color: var(--app-text-sub); font-size: 12px; }

/* 确认摘要：键值对齐，读起来像一张对账单 */
.cf-list { display: flex; flex-direction: column; gap: 3px; margin: 4px 0 8px; }
.cf-row { display: flex; gap: 8px; font-size: 12px; line-height: 1.65; }
.cf-k { flex: 0 0 64px; color: var(--app-text-sub); }
.cf-v { flex: 1; color: var(--app-text); word-break: break-all; }
.cf-tip { font-size: 11px; color: var(--app-text-sub); margin-bottom: 8px; }
.cf-warn { font-size: 12px; color: var(--el-color-danger); margin-bottom: 8px; }
.cf-raw { margin: 0 0 10px; }
.cf-raw summary { cursor: pointer; font-size: 11px; color: var(--app-text-sub); }

.pane-foot {
  display: flex; gap: 8px; align-items: flex-end;
  padding: 12px 14px; background: var(--app-bg-card); border-top: 1px solid var(--app-border);
}
.pane-foot :deep(.el-textarea__inner) { font-size: 13px; }
</style>
