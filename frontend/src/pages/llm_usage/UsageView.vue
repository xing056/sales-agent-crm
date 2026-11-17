<template>
    <el-card>
        <div class="head">
            <div>
                <h3>Tokens 用量</h3>
                <p class="sub">
                    每一次模型请求都会上报一条流水，按账号归集。数据来自后端
                    <code>llm_usage</code> 明细表，不是估算值。
                </p>
            </div>
            <el-radio-group v-model="range" @change="load">
                <el-radio-button value="today">今天</el-radio-button>
                <el-radio-button value="week">本周</el-radio-button>
                <el-radio-button value="month">本月</el-radio-button>
            </el-radio-group>
        </div>

        <el-divider></el-divider>

        <div class="stats">
            <div class="stat">
                <span class="k">总消耗</span>
                <span class="v">{{ fmt(total.total_tokens) }}</span>
                <span class="u">token</span>
            </div>
            <div class="stat">
                <span class="k">请求次数</span>
                <span class="v">{{ total.requests || 0 }}</span>
                <span class="u">次</span>
            </div>
            <div class="stat">
                <span class="k">输入 / 输出</span>
                <span class="v">{{ fmt(total.prompt_tokens) }} / {{ fmt(total.completion_tokens) }}</span>
            </div>
            <div class="stat">
                <span class="k">缓存命中</span>
                <span class="v">{{ pct(total.cache_hit_rate) }}</span>
                <span class="u">（命中部分按折扣价计费）</span>
            </div>
            <div class="stat">
                <span class="k">较上期</span>
                <span v-if="change === null" class="v muted">—</span>
                <span v-else class="v" :class="change >= 0 ? 'up' : 'down'">
                    {{ change >= 0 ? '↑' : '↓' }} {{ Math.abs(change * 100).toFixed(1) }}%
                </span>
            </div>
        </div>

        <el-table v-loading="loading" :data="items" empty-text="这个区间还没有用量记录">
            <el-table-column prop="username" label="账号" min-width="120">
                <template #default="{ row }">
                    <span class="mono">{{ row.username }}</span>
                </template>
            </el-table-column>
            <el-table-column prop="requests" label="请求" width="80" align="right"></el-table-column>
            <el-table-column label="输入" min-width="110" align="right">
                <template #default="{ row }">{{ fmt(row.prompt_tokens) }}</template>
            </el-table-column>
            <el-table-column label="输出" min-width="110" align="right">
                <template #default="{ row }">{{ fmt(row.completion_tokens) }}</template>
            </el-table-column>
            <el-table-column label="合计" min-width="110" align="right">
                <template #default="{ row }">
                    <strong>{{ fmt(row.total_tokens) }}</strong>
                </template>
            </el-table-column>
            <el-table-column label="缓存命中率" width="120" align="right">
                <template #default="{ row }">{{ pct(row.cache_hit_rate) }}</template>
            </el-table-column>
            <el-table-column label="占总量" min-width="160">
                <template #default="{ row }">
                    <div class="bar">
                        <div class="bar-in" :style="{ width: share(row) + '%' }"></div>
                        <span class="bar-t">{{ share(row).toFixed(1) }}%</span>
                    </div>
                </template>
            </el-table-column>
        </el-table>

        <p class="foot">
            区间：{{ start }} ~ {{ endLabel }}
            <template v-if="previousTotal > 0">
                ｜上期总消耗 {{ fmt(previousTotal) }} token
            </template>
            ｜数字涨=成本涨，与股票红绿习惯相反，别读错
        </p>
    </el-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import http from '@/utils/http'

const range = ref('month')
const loading = ref(false)
const items = ref([])
const total = ref({})
const change = ref(null)
const previousTotal = ref(0)
const start = ref('')
const end = ref('')

const endLabel = computed(() => {
    if (!end.value) return ''
    // 后端给的是"不含"的右边界（下一期 00:00），显示时退一天更像人话
    const d = new Date(end.value)
    d.setDate(d.getDate() - 1)
    const p = (n) => String(n).padStart(2, '0')
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`
})

const fmt = (n) => (n === null || n === undefined ? '0' : Number(n).toLocaleString('zh-CN'))
const pct = (v) => `${((v || 0) * 100).toFixed(1)}%`

// 占比按"该账号 / 区间总量"，用来一眼看出谁是大头
function share(row) {
    const sum = total.value.total_tokens || 0
    return sum ? (row.total_tokens / sum) * 100 : 0
}

async function load() {
    loading.value = true
    try {
        const res = await http.get('/llm_usage/summary/', { params: { range: range.value } })
        if (!res || !res.data) return
        const data = res.data
        items.value = data.items || []
        total.value = data.total || {}
        change.value = data.change_rate === undefined ? null : data.change_rate
        previousTotal.value = (data.previous && data.previous.total_tokens) || 0
        start.value = (data.start || '').slice(0, 10)
        end.value = data.end || ''
    } finally {
        loading.value = false
    }
}

onMounted(load)
</script>

<style scoped>
.head {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
}

.head h3 {
    margin: 0 0 6px;
}

.sub {
    margin: 0;
    color: var(--app-text-secondary, #888);
    font-size: 13px;
    line-height: 1.6;
}

.sub code {
    background: var(--app-bg-muted, #f2f3f5);
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 12px;
}

.stats {
    display: flex;
    flex-wrap: wrap;
    gap: 28px;
    margin-bottom: 18px;
}

.stat {
    display: flex;
    flex-direction: column;
    gap: 4px;
}

.stat .k {
    font-size: 12px;
    color: var(--app-text-secondary, #888);
}

.stat .v {
    font-size: 22px;
    font-weight: 600;
    font-variant-numeric: tabular-nums;
}

.stat .v.muted {
    color: var(--app-text-secondary, #888);
}

.stat .u {
    font-size: 12px;
    color: var(--app-text-secondary, #888);
}

/* 涨=成本上升，用警示色；降=省钱，用安全色。故意和股票红绿相反 */
.up {
    color: #d03050;
}

.down {
    color: #18a058;
}

.mono {
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
}

.bar {
    display: flex;
    align-items: center;
    gap: 8px;
}

.bar-in {
    height: 6px;
    border-radius: 3px;
    background: linear-gradient(90deg, #2080f0, #36ad6a);
    min-width: 2px;
}

.bar-t {
    font-size: 12px;
    color: var(--app-text-secondary, #888);
    font-variant-numeric: tabular-nums;
}

.foot {
    margin: 14px 0 0;
    font-size: 12px;
    color: var(--app-text-secondary, #888);
}
</style>
