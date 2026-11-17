<template>
    <div class="dash">
        <div class="dash-head">
            <div>
                <h2 class="hi">{{ greeting }}</h2>
                <p class="sub">{{ todayText }} · 数据来自系统实时查询</p>
            </div>
        </div>

        <!-- 四个数字：进去先看这四个，别的不看也能干活 -->
        <div class="cards">
            <div class="card" v-for="item in cards" :key="item.label">
                <p class="card-label">{{ item.label }}</p>
                <p class="card-value" :class="item.tone">{{ item.value }}</p>
                <p class="card-hint">{{ item.hint }}</p>
            </div>
        </div>

        <div class="panels">
            <section class="panel">
                <header class="panel-head">
                    <span>本月业绩 top5</span>
                    <span class="panel-sub">按已支付订单金额</span>
                </header>
                <div v-if="!canOrder" class="empty">没有查看订单的权限</div>
                <div v-else-if="!ranking.length" class="empty">本月还没有已支付订单</div>
                <ul v-else class="rank">
                    <li v-for="(r, i) in ranking" :key="r.name">
                        <span class="rank-no">{{ i + 1 }}</span>
                        <span class="rank-name">{{ r.name }}</span>
                        <span class="rank-bar">
                            <i :style="{ width: r.percent + '%' }"></i>
                        </span>
                        <span class="rank-amount">{{ r.amount }}</span>
                    </li>
                </ul>
            </section>

            <section class="panel">
                <header class="panel-head">
                    <span>需要处理</span>
                    <span class="panel-sub">点进去看明细</span>
                </header>
                <ul class="todo">
                    <li v-for="t in todos" :key="t.label" @click="go(t.to)">
                        <span class="todo-dot" :class="t.tone"></span>
                        <span class="todo-label">{{ t.label }}</span>
                        <span class="todo-num" :class="t.tone">{{ t.value }}</span>
                        <span class="todo-arrow">›</span>
                    </li>
                </ul>
            </section>
        </div>
    </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user'
import http from '@/utils/http'
import { hasPermission } from '@/utils/util'
import { formatCents, sumCents, toCents } from '@/utils/money'

const router = useRouter()
const userStore = useUserStore()
const { loginInfo } = storeToRefs(userStore)

const orders = ref([])
const customers = ref([])
const trackings = ref([])
const loaded = ref({ order: false, customer: false, tracking: false })

const canOrder = hasPermission(['api:sale_order:list'])
const canCustomer = hasPermission(['api:customer:list'])
const canTracking = hasPermission(['api:customer_tracking:list'])

const now = new Date()
const pad = (n) => String(n).padStart(2, '0')
const ym = `${now.getFullYear()}-${pad(now.getMonth() + 1)}`
const today = `${ym}-${pad(now.getDate())}`

const greeting = computed(() => {
    const name = loginInfo.value?.employee?.name || loginInfo.value?.username || '你好'
    return `${name}，今天先看这四件事`
})
const todayText = `${now.getFullYear()} 年 ${now.getMonth() + 1} 月 ${now.getDate()} 日`

/* 分页取全量：后端单页上限 100 */
async function fetchAll(path) {
    const rows = []
    for (let page = 1; page <= 20; page++) {
        const res = await http.get(path, { params: { page, size: 100 } })
        if (!res || !res.data) return null
        const data = res.data
        const batch = data.results || []
        rows.push(...batch)
        if (!batch.length || rows.length >= (data.count ?? rows.length)) break
    }
    return rows
}

onMounted(async () => {
    if (canOrder) {
        const rows = await fetchAll('/sale_order/')
        if (rows) {
            orders.value = rows
            loaded.value.order = true
        }
    }
    if (canCustomer) {
        const rows = await fetchAll('/customer/')
        if (rows) {
            customers.value = rows
            loaded.value.customer = true
        }
    }
    if (canTracking) {
        const rows = await fetchAll('/customer_tracking/')
        if (rows) {
            trackings.value = rows
            loaded.value.tracking = true
        }
    }
})

/* ---------- 指标 ---------- */
const paidThisMonth = computed(() =>
    orders.value.filter((o) => o.pay_status && (o.create_time || '').slice(0, 7) === ym)
)

const monthAmount = computed(() => formatCents(sumCents(paidThisMonth.value.map((o) => o.amount))))
const todayOrders = computed(() =>
    orders.value.filter((o) => (o.create_time || '').slice(0, 10) === today)
)

const cards = computed(() => [
    {
        label: '本月成交额',
        value: loaded.value.order ? monthAmount.value : '—',
        hint: `${paidThisMonth.value.length} 笔已支付`,
        tone: 'money',
    },
    {
        label: '本月订单',
        value: loaded.value.order ? `${paidThisMonth.value.length}` : '—',
        hint: '笔',
        tone: '',
    },
    {
        label: '今日订单',
        value: loaded.value.order ? `${todayOrders.value.length}` : '—',
        hint: todayOrders.value.length ? '笔' : '今天还没有新单',
        tone: '',
    },
    {
        label: '客户总数',
        value: loaded.value.customer ? `${customers.value.length}` : '—',
        hint: loaded.value.customer ? '位' : '无权限',
        tone: '',
    },
])

/* ---------- 排行 ---------- */
const ranking = computed(() => {
    const map = new Map()
    paidThisMonth.value.forEach((o) => {
        const name = o.user?.employee?.name || o.user?.username || '未知'
        const row = map.get(name) || { name, cents: 0n, count: 0 }
        row.cents += toCents(o.amount)
        row.count += 1
        map.set(name, row)
    })
    const list = [...map.values()].sort((a, b) => (a.cents === b.cents ? b.count - a.count : a.cents > b.cents ? -1 : 1))
    const max = list.length ? list[0].cents : 0n
    return list.slice(0, 5).map((r) => ({
        name: r.name,
        amount: formatCents(r.cents),
        percent: max > 0n ? Number((r.cents * 100n) / max) : 0,
    }))
})

/* ---------- 待办 ---------- */
const lastFollowAt = computed(() => {
    const map = {}
    trackings.value.forEach((t) => {
        const cid = t.customer?.id
        if (!cid) return
        const ts = new Date(t.tracking_time || t.create_time).getTime()
        if (!map[cid] || ts > map[cid]) map[cid] = ts
    })
    return map
})

const overdueCount = computed(() => {
    if (!loaded.value.customer || !loaded.value.tracking) return null
    return customers.value.filter((c) => {
        const ts = lastFollowAt.value[c.id]
        if (!ts) return true
        return (Date.now() - ts) / 86400000 > 30
    }).length
})

const lockedCount = computed(() =>
    loaded.value.customer ? customers.value.filter((c) => c.status === false).length : null
)
const unpaidCount = computed(() =>
    loaded.value.order ? orders.value.filter((o) => !o.pay_status).length : null
)

const todos = computed(() => [
    {
        label: '超 30 天没跟进的客户',
        value: overdueCount.value === null ? '—' : `${overdueCount.value} 位`,
        tone: 'warn',
        to: { name: 'customer' },
    },
    {
        label: '状态被锁定的客户',
        value: lockedCount.value === null ? '—' : `${lockedCount.value} 位`,
        tone: 'muted',
        to: { name: 'customer' },
    },
    {
        label: '未支付的订单',
        value: unpaidCount.value === null ? '—' : `${unpaidCount.value} 单`,
        tone: 'muted',
        to: { name: 'saleOrder' },
    },
])

const go = (to) => router.push(to)
</script>

<style scoped>
.dash {
    padding: 4px 2px;
}

.dash-head {
    margin-bottom: 18px;
}

.hi {
    font-size: 20px;
    font-weight: 500;
    color: var(--el-text-color-primary);
    margin: 0 0 4px;
}

.sub {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    margin: 0;
}

.cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 14px;
    margin-bottom: 16px;
}

.card {
    background: var(--el-bg-color);
    border: 1px solid var(--el-border-color-lighter);
    border-radius: 10px;
    padding: 16px 18px;
}

.card-label {
    font-size: 12px;
    color: var(--el-text-color-secondary);
    margin: 0 0 8px;
}

.card-value {
    font-size: 26px;
    font-weight: 500;
    line-height: 1.2;
    margin: 0 0 6px;
    color: var(--el-text-color-primary);
    font-variant-numeric: tabular-nums;
    font-feature-settings: 'tnum';
}

.card-value.money {
    color: #b88230;
}

.card-hint {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
    margin: 0;
}

.panels {
    display: grid;
    grid-template-columns: minmax(0, 1.35fr) minmax(0, 1fr);
    gap: 14px;
}

@media (max-width: 900px) {
    .panels {
        grid-template-columns: minmax(0, 1fr);
    }
}

.panel {
    background: var(--el-bg-color);
    border: 1px solid var(--el-border-color-lighter);
    border-radius: 10px;
    padding: 16px 18px;
}

.panel-head {
    display: flex;
    align-items: baseline;
    justify-content: space-between;
    margin-bottom: 14px;
    font-size: 14px;
    font-weight: 500;
    color: var(--el-text-color-primary);
}

.panel-sub {
    font-size: 12px;
    font-weight: 400;
    color: var(--el-text-color-placeholder);
}

.empty {
    font-size: 13px;
    color: var(--el-text-color-placeholder);
    padding: 18px 0;
    text-align: center;
}

.rank {
    list-style: none;
    margin: 0;
    padding: 0;
}

.rank li {
    display: grid;
    grid-template-columns: 20px 68px minmax(0, 1fr) 96px;
    align-items: center;
    gap: 10px;
    padding: 7px 0;
}

.rank-no {
    font-size: 12px;
    color: var(--el-text-color-placeholder);
    font-variant-numeric: tabular-nums;
}

.rank-name {
    font-size: 13px;
    color: var(--el-text-color-regular);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
}

.rank-bar {
    height: 8px;
    background: var(--el-fill-color-light);
    border-radius: 4px;
    overflow: hidden;
}

.rank-bar i {
    display: block;
    height: 100%;
    background: #c9a227;
    border-radius: 4px;
}

.rank-amount {
    text-align: right;
    font-size: 13px;
    color: var(--el-text-color-primary);
    font-variant-numeric: tabular-nums;
    font-feature-settings: 'tnum';
}

.todo {
    list-style: none;
    margin: 0;
    padding: 0;
}

.todo li {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 0;
    border-bottom: 1px solid var(--el-border-color-lighter);
    cursor: pointer;
}

.todo li:last-child {
    border-bottom: none;
}

.todo li:hover .todo-label {
    color: var(--el-color-primary);
}

.todo-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--el-text-color-placeholder);
    flex: 0 0 6px;
}

.todo-dot.warn {
    background: #e6a23c;
}

.todo-label {
    font-size: 13px;
    color: var(--el-text-color-regular);
}

.todo-num {
    margin-left: auto;
    font-size: 14px;
    color: var(--el-text-color-primary);
    font-variant-numeric: tabular-nums;
}

.todo-num.warn {
    color: #e6a23c;
    font-weight: 500;
}

.todo-arrow {
    color: var(--el-text-color-placeholder);
    font-size: 16px;
    line-height: 1;
}
</style>
