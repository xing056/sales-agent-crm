<template>
  <el-card>
    <h3>销售订单管理</h3>
    <div class="actions">
      <el-button type="primary" plain @click="$router.push({ name: 'product' })">创建订单</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="saleOrderList">
      <el-table-column prop="id" label="序号" min-width="80"></el-table-column>
      <el-table-column prop="order_no" label="订单编号" min-width="100"></el-table-column>
      <el-table-column prop="customer.name" label="下单客户" min-width="100"></el-table-column>
      <el-table-column prop="user.employee.name" label="销售顾问" min-width="100"></el-table-column>
      <el-table-column prop="amount" label="订单金额" min-width="100"></el-table-column>
      <el-table-column prop="commission" label="销售佣金" min-width="100"></el-table-column>
      <el-table-column prop="status" label="订单状态" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.status ? 'primary' : 'danger'">{{ props.row.status ? '正常' : '关闭' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" label="下单时间" min-width="100"></el-table-column>
      <el-table-column prop="pay_way" label="支付方式" min-width="100">
        <template v-slot="props">
          <el-tag>{{ payWay[props.row.pay_way].label }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="pay_status" label="支付状态" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.pay_status ? 'primary' : 'danger'">{{ props.row.pay_status ? '已支付' : '未支付'
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="pay_time" label="支付时间" min-width="100"></el-table-column>
      <el-table-column fixed="right" label="操作" min-width="120">
        <template v-slot="props">
          <el-space>
            <el-button @click="$router.push({ name: 'saleOrderDetail', params: { id: props.row.id } })" type="primary"
              size="small" plain>详情</el-button>
            <el-button @click="del(props.row.id)" type="danger" size="small" plain>删除</el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>

    <br>
    <el-pagination :total="saleOrderCount" layout="total,prev,pager,next,jumper" :page-size="size" background
      @current-change="pageChange"></el-pagination>

  </el-card>
</template>

<script setup>
import { payWay } from '@/utils/config'
import useSaleOrderStore from '@/stores/sale_order'
import { usePager } from '@/utils/hooks'
import { storeToRefs } from 'pinia'
import { withConfirm } from '@/utils/util'
import { removeSaleOrder } from '@/utils/api'
const saleOrderStore = useSaleOrderStore()
const { saleOrderCount, saleOrderList } = storeToRefs(saleOrderStore)
const { getSaleOrderListAction } = saleOrderStore
const { page, size } = usePager()
getSaleOrderListAction({ page: page.value, size: size.value })
const pageChange = (num) => {
  page.value = num
  getSaleOrderListAction({ page: page.value, size: size.value })
}
const del = (id) => {
  withConfirm(async () => {
    return await removeSaleOrder(id)
  }, () => {
    getSaleOrderListAction({ page: page.value, size: size.value })
  })
}
</script>

<style></style>