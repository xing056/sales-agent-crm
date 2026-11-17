<template>
    <el-card>
        <h3>销售提成列表</h3>
        <el-divider></el-divider>
        <el-table :data="commisionList">
            <el-table-column prop="id" min-width="80" label="序号"></el-table-column>
            <el-table-column prop="user.employee.name" min-width="100" label="员工姓名"></el-table-column>
            <el-table-column prop="commission" min-width="100" label="提成金额"></el-table-column>
            <el-table-column prop="year_month" min-width="100" label="所属期"></el-table-column>
            <el-table-column prop="create_time" min-width="100" label="生成日期"></el-table-column>
            <el-table-column min-width="120" label="操作">
                <el-space>
                    <el-button type="primary" plain size="small">详情</el-button>
                </el-space>
            </el-table-column>
        </el-table>
        <br>
        <el-pagination background :total="commisionCount" layout="total,prev,pager,next,jumper" :page-size="size"
            @current-change="pageChange"></el-pagination>
    </el-card>
</template>

<script setup>
import useCommissionStore from '@/stores/commission'
import { storeToRefs } from 'pinia'
import { usePager } from '@/utils/hooks'
import { createCommission } from '@/utils/api'
import { withConfirm } from '@/utils/util'
const commissionStore = useCommissionStore()
const { commisionCount, commisionList } = storeToRefs(commissionStore)
const { getCommissionAction } = commissionStore
const { page, size } = usePager()
getCommissionAction({ page: page.value, size: size.value })
const pageChange = (num) => {
    page.value = num
    getCommissionAction({ page: page.value, size: size.value })
}
const createData = () => {
    withConfirm(async () => {
        return await createCommission()
    }, () => {
        getCommissionAction({ page: page.value, size: size.value })
    })
}
</script>

<style></style>