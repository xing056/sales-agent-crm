<template>
    <div class="actions">
        <el-button type="info" @click="$router.go(-1)">返回</el-button>
        <el-button v-if="hasPermission(['api:customer_tracking:create'])" @click="dialog.visible = true" type="primary" plain>新增记录</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="customerTrackingList">
        <el-table-column prop="id" label="序号" min-width="80"></el-table-column>
        <el-table-column prop="customer.name" label="客户姓名" min-width="100"></el-table-column>
        <el-table-column prop="user.employee.name" label="销售人员" min-width="100"></el-table-column>
        <el-table-column prop="tracking_way" label="跟踪方式" min-width="100">
            <template v-slot="props">
                {{ trackingWay[props.row.tracking_way].label }}
            </template>
        </el-table-column>
        <el-table-column prop="tracking_time" label="跟踪时间" min-width="100"></el-table-column>
        <el-table-column prop="status" label="跟踪状态" min-width="100">
            <template v-slot="props">
                <el-tag :type="props.row.status ? 'primary' : 'danger'">{{ props.row.status ? '成功' : '失败'
                    }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="description" label="跟踪描述" min-width="100"></el-table-column>
        <el-table-column prop="create_time" label="添加时间" min-width="100"></el-table-column>
        <el-table-column fixed="right" label="操作" min-width="120" v-if="hasPermission(['api:customer_tracking:update','api:customer_tracking:destroy'])">
            <template v-slot="props">
                <el-space wrap>
                    <el-button v-if="hasPermission(['api:customer_tracking:update'])" @click="edit(props.row)" type="primary" size="small">编辑</el-button>
                    <el-button v-if="hasPermission(['api:customer_tracking:destroy'])" @click="del(props.row.id)" type="danger" size="small">删除</el-button>
                </el-space>
            </template>
        </el-table-column>
    </el-table>
    <br>
    <el-pagination background @current-change="pageChange" :page-size="size" :total="customerTrackingCount"
        layout="total,prev,pager,next,jumper"></el-pagination>
    <TrackingDialog ref="dialog" @updateTracking="updateTracking" />
</template>
<script setup>
import TrackingDialog from '@/pages/customer_tracking/TrackingDialog.vue'
import { trackingWay } from '@/utils/config'
import { ref, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import useCustomerTrackingStore from '@/stores/customer_tracking'
import { hasPermission, withConfirm } from '@/utils/util'
import { removeCustomerTracking } from '@/utils/api'
// 接受父组件通过自定义属性传递的customerId
const { customerId } = defineProps({
    customerId: {
        type: Number,
        default: null
    }
})
const customerTrackingStore = useCustomerTrackingStore()
const dialog = useTemplateRef('dialog')
const { customerTrackingList, customerTrackingCount } = storeToRefs(customerTrackingStore)
const { getCustomerTrackingAction } = customerTrackingStore
const page = ref(1)
const size = ref(10)
const params = { page: page.value, size: size.value }
if (customerId) {
    params.customer_id = customerId
}
getCustomerTrackingAction(params)
const pageChange = (num) => {
    page.value = num
    getCustomerTrackingAction(params)
}
const del = (id) => {
    withConfirm(async () => {
        return await removeCustomerTracking(id)
    }, () => {
        getCustomerTrackingAction(params)
    })
}
// 自定义事件处理函数
const updateTracking = () => {
    getCustomerTrackingAction(params)
}
const edit = (row) => {
    dialog.value.openUpdateForm(row)
}
</script>

<style></style>