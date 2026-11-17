<template>
  <el-card>
    <h3>订单详情</h3>
    <div class="actions">
      <el-button @click="$router.back()" plain type="primary">返回</el-button>
    </div>
    <el-divider></el-divider>
    <!-- {{ orderDetail }} -->
    <el-descriptions border direction="vertical">
      <el-descriptions-item label="订单编号">
        {{ orderDetail.order_no }}
      </el-descriptions-item>
      <el-descriptions-item label="订单金额">
        &yen;{{ orderDetail.amount }}
      </el-descriptions-item>
      <el-descriptions-item label="订单佣金">
        &yen;{{ orderDetail.commission }}
      </el-descriptions-item>
      <el-descriptions-item label="下单客户">
        {{ orderDetail.customer?.name }}-{{ orderDetail.customer?.phone }}
      </el-descriptions-item>
      <el-descriptions-item label="销售顾问">
        {{ orderDetail.user?.employee?.name }}-{{ orderDetail.user?.employee?.phone }}
      </el-descriptions-item>
      <el-descriptions-item label="订单状态">
        {{ orderDetail.status ? '正常' : '关闭' }}
      </el-descriptions-item>
      <el-descriptions-item label="下单时间">
        {{ orderDetail.create_time }}
      </el-descriptions-item>
    </el-descriptions>
    <el-divider>支付信息</el-divider>
    <el-descriptions border direction="vertical">
      <el-descriptions-item label="支付状态">
        {{ orderDetail.pay_status ? '已支付' : '未支付' }}
      </el-descriptions-item>
      <el-descriptions-item label="支付方式">
        {{ payWay[orderDetail.pay_way]?.label }}
      </el-descriptions-item>
      <el-descriptions-item label="支付时间">
        {{ orderDetail.pay_time || '暂无' }}
      </el-descriptions-item>
    </el-descriptions>
    <el-divider>快递信息</el-divider>
    <el-form ref="orderForm" :rules="rules" :model="orderDetail">
      <el-descriptions border direction="vertical">
        <el-descriptions-item label="收货人">
          <template v-if="isEdit">
            <el-form-item prop="consignee">
              <el-input placeholder="请输入收货人" v-model.trim="orderDetail.consignee"></el-input>
            </el-form-item>
          </template>
          <template v-else>
            {{ orderDetail.consignee }}
          </template>
        </el-descriptions-item>
        <el-descriptions-item label="联系电话">
          <template v-if="isEdit">
            <el-form-item prop="phone">
              <el-input placeholder="请输入联系电话" v-model.trim="orderDetail.phone"></el-input>
            </el-form-item>
          </template>
          <template v-else>{{ orderDetail.phone }}</template>
        </el-descriptions-item>
        <el-descriptions-item label="收货地址">
          <template v-if="isEdit">
            <el-form-item prop="region">
              <!-- 省市区级联选择器 -->
              <el-cascader @change="regionChange" :options="pcaTextArr" v-model="orderDetail.region">
              </el-cascader>
            </el-form-item>
            <el-form-item prop="adddress">
              <el-input placeholder="请输入详细地址" v-model.trim="orderDetail.address"></el-input>
            </el-form-item>
          </template>
          <template v-else>
            {{ orderDetail.province }}-{{ orderDetail.city }}-{{ orderDetail.county }}-{{ orderDetail.address }}
          </template>
        </el-descriptions-item>
        <el-descriptions-item label="快递状态">
          <template v-if="isEdit">
            <el-radio-group v-model="orderDetail.express_status">
              <el-radio :value="true" label="已发货"></el-radio>
              <el-radio :value="false" label="待发货"></el-radio>
            </el-radio-group>
          </template>
          <template v-else>
            {{ orderDetail.express_status ? '已发货' : '待发货' }}
          </template>
        </el-descriptions-item>
        <el-descriptions-item label="快递名称">
          <template v-if="isEdit">
            <el-form-item prop="express_name">
              <el-input placeholder="请输入快递名称" v-model.trim="orderDetail.express_name"></el-input>
            </el-form-item>
          </template>
          <template v-else>
            {{ orderDetail.express_name || '暂无' }}
          </template>
        </el-descriptions-item>
        <el-descriptions-item label="快递单号">
          <template v-if="isEdit">
            <el-form-item prop="express_no">
              <el-input placeholder="请输入快递单号" v-model.trim="orderDetail.express_no"></el-input>
            </el-form-item>
          </template>
          <template v-else>
            {{ orderDetail.express_no || '暂无' }}
          </template>
        </el-descriptions-item>
        <el-descriptions-item label="操作">
          <template v-if="isEdit">
            <el-button @click="submit" plain type="primary">确认提交</el-button>
            <el-button @click="isEdit = false" plain type="info">取消</el-button>
          </template>
          <el-button v-else @click="isEdit = true" plain type="primary">更新快递信息</el-button>

        </el-descriptions-item>
      </el-descriptions>
    </el-form>
    <el-divider>订单商品</el-divider>
    <el-table :data="orderProductList">
      <el-table-column prop="id" label="商品序号" min-width="80"></el-table-column>
      <el-table-column prop="cover" label="商品图片" min-width="100">
        <template v-slot="props">
          <el-image fit="cover" style="width: 100px;" :src="props.row.cover" v-if="props.row.cover"></el-image>
          <el-text v-else type="primary">暂无</el-text>
        </template>
      </el-table-column>
      <el-table-column prop="name" label="商品名称" min-width="100"></el-table-column>
      <el-table-column prop="price" label="商品价格" min-width="100"></el-table-column>
      <el-table-column prop="num" label="商品数量" min-width="100"></el-table-column>
      <el-table-column prop="commission_rate" label="商品佣金比例" min-width="100"></el-table-column>
    </el-table>
  </el-card>
</template>

<script setup>
import { pcaTextArr } from 'element-china-area-data'
import { payWay } from '@/utils/config'
import { onMounted, ref, useTemplateRef } from 'vue'
import { getSaleOrder, getSaleOrderProductList, updateSaleOrder } from '@/utils/api'
import { useRoute } from 'vue-router'
import { ElNotification } from 'element-plus'
const orderForm = useTemplateRef('orderForm')
const isEdit = ref(false)
const route = useRoute()
const saleOrderId = route.params.id
// 获取订单详情
const orderDetail = ref({})
// 订单商品列表
const orderProductList = ref([])
onMounted(async () => {
  const result = await getSaleOrder(saleOrderId)
  if (result.status === 200) {
    orderDetail.value = result.data
    const { province, city, county } = orderDetail.value
    orderDetail.value.region = [province, city, county]
  }
  const res = await getSaleOrderProductList(saleOrderId)
  if (res.status === 200) {
    orderProductList.value = res.data
  }
})
const rules = {
  consignee: [{ required: true, message: '请输入收货人姓名' }],
  phone: [{ pattern: /^1[3456789]\d{9}$/, required: true, message: '请输入收货人联系电话' }],
  region: [{ required: true, message: '请选择省市区' }],
  addess: [{ required: true, message: '请输入详细收货地址' }],
  express_name: [{ required: true, message: '请输入快递名称' }],
  express_status: [{ required: true, message: '请选择快递状态' }],
  express_no: [{ required: true, message: '请输入快递单号' }],
}
const regionChange = (region) => {
  const [province, city, county] = region
  orderDetail.value.province = province
  orderDetail.value.city = city
  orderDetail.value.county = county
}
const submit = () => {
  orderForm.value.validate(async valid => {
    if (valid) {
      const { consignee, phone, addess, express_name, express_status, express_no, province, city, county } = orderDetail.value
      const body = { consignee, phone, addess, express_name, express_status, express_no, province, city, county }
      const result = await updateSaleOrder(saleOrderId, body)
      if (result.status === 200) {
        ElNotification.success('更新订单信息成功')
        isEdit.value = false
      }
    }
  })
}
</script>

<style></style>