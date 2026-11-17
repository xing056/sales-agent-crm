<template>
    <div class="actions">
        <el-button v-if="hasPermission(['api:customer:create'])" @click="dialog.visible = true" type="primary"
            plain>新增客户</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="customerList" :row-class-name="rowClass">
        <!-- 姓名和手机号合成一列：扫一眼就知道是谁、怎么联系 -->
        <el-table-column label="客户" min-width="150">
            <template v-slot="props">
                <div class="cust-name">{{ props.row.name }}</div>
                <div class="cust-phone">{{ props.row.phone }}</div>
            </template>
        </el-table-column>

        <!-- 省份/城市/区县/地址 4 列合成 1 列，鼠标悬停看全址 -->
        <el-table-column label="地区" min-width="180" show-overflow-tooltip>
            <template v-slot="props">
                {{ fullAddress(props.row) }}
            </template>
        </el-table-column>

        <!-- 等级从数字变成人看得懂的话 -->
        <el-table-column label="等级" min-width="100">
            <template v-slot="props">
                <el-tag :type="levelInfo(props.row.level).type" effect="plain" size="small">
                    {{ levelInfo(props.row.level).text }}
                </el-tag>
            </template>
        </el-table-column>

        <el-table-column label="消费次数" min-width="95" align="right">
            <template v-slot="props">
                <span class="num">{{ props.row.order_count ?? 0 }}</span>
            </template>
        </el-table-column>

        <!-- 金额：右对齐 + 等宽数字 + 千分位，一列数字才能竖着比大小 -->
        <el-table-column label="消费金额" min-width="130" align="right">
            <template v-slot="props">
                <span class="num money">{{ money(props.row.order_amount) }}</span>
            </template>
        </el-table-column>

        <!-- 销售最关心的一列：这个客户是不是快凉了 -->
        <el-table-column label="最近跟进" min-width="115" align="right">
            <template v-slot="props">
                <template v-if="followDays(props.row.id) === null">
                    <span class="never">未跟进</span>
                </template>
                <template v-else>
                    <span :class="['num', followClass(followDays(props.row.id))]">
                        {{ followDays(props.row.id) }} 天前
                    </span>
                </template>
            </template>
        </el-table-column>

        <el-table-column align="center" label="销售专员" min-width="120">
            <template v-slot="props">
                <div>{{ props.row.user?.employee?.name || '—' }}</div>
                <el-link v-if="hasPermission(['api:employee:detail'])" underline="always" type="primary"
                    @click="$router.push({ name: 'empDetail', params: { id: props.row.user.employee.id } })">
                    {{ props.row.user?.employee?.work_no }}
                </el-link>
            </template>
        </el-table-column>

        <el-table-column label="来源" min-width="110">
            <template v-slot="props">{{ props.row.source?.name || '—' }}</template>
        </el-table-column>

        <el-table-column label="状态" min-width="80">
            <template v-slot="props">
                <el-tag :type="props.row.status ? 'primary' : 'danger'" effect="plain" size="small">
                    {{ props.row.status ? '正常' : '锁定' }}
                </el-tag>
            </template>
        </el-table-column>

        <el-table-column label="添加时间" min-width="160">
            <template v-slot="props">
                <span class="muted">{{ (props.row.create_time || '').slice(0, 10) }}</span>
            </template>
        </el-table-column>

        <el-table-column fixed="right" label="操作" min-width="190"
            v-if="hasPermission(['api:customer:update', 'api:customer:destroy'])">
            <template v-slot="props">
                <el-space wrap>
                    <el-button v-if="hasPermission(['api:customer_tracking:list'])"
                        @click="$router.push({ name: 'customerTracking', params: { id: props.row.id } })" type="info"
                        plain size="small">跟踪</el-button>
                    <el-button v-if="hasPermission(['api:customer:update'])"
                        @click="$router.push({ name: 'customerDetail', params: { id: props.row.id } })" type="primary"
                        plain size="small">详情</el-button>
                    <el-button v-if="hasPermission(['api:customer:destroy'])" @click="del(props.row.id)" type="danger"
                        plain size="small">删除</el-button>
                </el-space>
            </template>
        </el-table-column>
    </el-table>
    <br>
    <el-pagination @current-change="pageChange" background :total="customerCount" layout="total,prev,pager,next,jumper"
        :page-size="size"></el-pagination>
    <CustomerDialog ref="dialog" @updateCustomer="updateCustomer" />
</template>

<script setup>
import CustomerDialog from '@/pages/customer/CustomerDialog.vue'
import { ref, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import useCustomerStore from '@/stores/customer'
import { hasPermission, withConfirm } from '@/utils/util'
import { removeCustomer, getCustomerTrackingList } from '@/utils/api'
import { formatMoney } from '@/utils/money'

const { userId } = defineProps({
    userId: {
        type: Number,
        default: null
    }
})
const customerStore = useCustomerStore()
const dialog = useTemplateRef('dialog')
const { customerList, customerCount } = storeToRefs(customerStore)
const { getCustomerAction } = customerStore
const page = ref(1)
const size = ref(10)
const params = { page: page.value, size: size.value }
if (userId) {
    params.userId = userId
}
getCustomerAction(params)

/* 金额格式化统一走 utils/money.js：整数分计算，不经过浮点 */
const money = (value) => formatMoney(value)

/* ---------- 等级语义化 ---------- */
const LEVELS = {
    0: { text: '未分级', type: 'info' },
    1: { text: '一般客户', type: 'primary' },
    2: { text: '重点客户', type: 'warning' },
}
const levelInfo = (level) => LEVELS[level] ?? { text: `等级${level}`, type: 'info' }

const fullAddress = (row) => {
    const parts = [row.province, row.city, row.county, row.address].filter(Boolean)
    const joined = parts.join(' ')
    return joined || '—'
}

/* ---------- 最近跟进天数 ----------
   数据来自 customer_tracking。当前数据量小，一次取回后本地按客户归并；
   量大了应该让后端 annotate(Max('tracking_time')) 直接带在客户列表里，
   避免前端做联表。这里保持改动最小。 */
const lastTrackingAt = ref({})

const loadTracking = async () => {
    if (!hasPermission(['api:customer_tracking:list'])) return
    const res = await getCustomerTrackingList({ page: 1, size: 100 })
    if (!res || !res.data) return
    const rows = res.data.results || res.data || []
    const map = {}
    rows.forEach((item) => {
        const cid = item.customer?.id
        if (!cid) return
        const ts = new Date(item.tracking_time || item.create_time).getTime()
        if (!map[cid] || ts > map[cid]) map[cid] = ts
    })
    lastTrackingAt.value = map
}
loadTracking()

const followDays = (customerId) => {
    const ts = lastTrackingAt.value[customerId]
    if (!ts) return null
    return Math.max(0, Math.floor((Date.now() - ts) / 86400000))
}

const followClass = (days) => {
    if (days === null) return 'muted'
    if (days > 30) return 'overdue'
    if (days > 7) return 'warm'
    return 'fresh'
}

/* 逾期客户整行淡淡标记一下，方便一眼扫到 */
const rowClass = ({ row }) => {
    const days = followDays(row.id)
    return days !== null && days > 30 ? 'row-overdue' : ''
}

const pageChange = (num) => {
    params.page = page.value = num
    getCustomerAction(params)
}
const updateCustomer = () => {
    getCustomerAction(params)
}
const del = (id) => {
    withConfirm(async () => {
        return await removeCustomer(id)
    }, () => {
        getCustomerAction(params)
    })
}
</script>

<style scoped>
.actions {
    display: flex;
    justify-content: flex-end;
}

.cust-name {
    color: #1f2329;
    font-weight: 500;
}

.cust-phone {
    font-size: 12px;
    color: #909399;
    font-variant-numeric: tabular-nums;
}

/* 等宽数字：让同一列的数字位数对齐，扫读时不会跳 */
.num {
    font-variant-numeric: tabular-nums;
    font-feature-settings: 'tnum';
}

.money {
    color: #1f2329;
}

.muted {
    color: #c0c4cc;
}

/* 从未跟进：给橙色而不是红色。103/107 都是这个状态，
   全标红会变成报警疲劳，反而没人看。 */
.never {
    color: #e6a23c;
}

.fresh {
    color: #67c23a;
}

.warm {
    color: #e6a23c;
}

.overdue {
    color: var(--el-color-danger);
    font-weight: 500;
}

:deep(.row-overdue) td {
    background-color: var(--app-danger-row) !important;
}
</style>
