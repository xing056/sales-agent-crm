<template>
    <el-card>
        <h3>客户来源管理</h3>
        <div class="actions">
            <el-button v-if="hasPermission(['api:customer_source:create'])" @click="dialog.visible = true" type="primary" plain>新增客户来源</el-button>
        </div>
        <el-divider></el-divider>
        <el-table :data="customerSourceList">
            <el-table-column prop="id" label="序号" min-width="80"></el-table-column>
            <el-table-column prop="name" label="来源名称" min-width="100"></el-table-column>
            <el-table-column prop="status" label="来源状态" min-width="100">
                <template v-slot="props">
                    <el-tag :type="props.row.status ? 'primary' : 'danger'">{{ props.row.status ? '正常' : '禁用'
                    }}</el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="120" v-if="hasPermission(['api:customer_source:update','api:customer_source:destroy'])">
                <template v-slot="props">
                    <el-space>
                        <el-button v-if="hasPermission(['api:customer_source:update'])" @click="edit(props.row)" type="primary" size="small" plain>编辑</el-button>
                        <el-button v-if="hasPermission(['api:customer_source:destroy'])" @click="del(props.row.id)" type="danger" size="small" plain>删除</el-button>
                    </el-space>
                </template>
            </el-table-column>
        </el-table>
        <br>
        <el-pagination @current-change="pageChange" :page-size="size" :total="customerSourceCount"
            layout="total,prev,pager,next,jumper" background></el-pagination>
    </el-card>
    <SourceDialog ref="dialog" @updateSource="updateSource" />
</template>

<script setup>
import SourceDialog from './SourceDialog.vue'
import { removeCustomerSource } from '@/utils/api'
import { withConfirm,hasPermission } from '@/utils/util'
import { ref, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import useCustomerSourceStore from '@/stores/customer_source'
const dialog = useTemplateRef('dialog')
// 获取数据仓库对象
const customerSourceStore = useCustomerSourceStore()
const { customerSourceCount, customerSourceList } = storeToRefs(customerSourceStore)
const { getCustomerSource } = customerSourceStore
const page = ref(1)
const size = ref(10)
// 请求客户来源数据
getCustomerSource({ page: page.value, size: size.value })
const pageChange = (num) => {
    page.value = num
    getCustomerSource({ page: page.value, size: size.value })
}
const del = (id) => {
    withConfirm(async () => { return await removeCustomerSource(id) }, () => {
        getCustomerSource({ page: page.value, size: size.value })
    })
}
const edit = (row) => {
    dialog.value.openUpdateForm(row)
}
const updateSource = () => {
    // 请求最新的列表数据
    getCustomerSource({ page: page.value, size: size.value })
}
</script>

<style></style>