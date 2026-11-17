<template>
    <el-card>
        <h3>创建订单</h3>
        <div class="actions">
            <el-button @click="$router.back()" type="primary" plain>返回</el-button>
        </div>
        <el-divider></el-divider>
        <el-form ref="orderForm" :rules="rules" :model="formData" label-width="80px" label-position="right">
            <el-form-item prop="customer_id" label="下单客户">
                <el-select @change="customerChange" v-model="formData.customer_id" remote :remote-method="queryCustomer"
                    :loading="loading" filterable clearable>
                    <el-option v-for="item in customerList" :key="item.id" :value="item.id"
                        :label="item.name + '-' + item.phone"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="consignee" label="收货人">
                <el-input v-model.trim="formData.consignee" placeholder="请输入收货人"></el-input>
            </el-form-item>
            <el-form-item prop="phone" label="联系电话">
                <el-input v-model.trim="formData.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
            <el-form-item prop="region" label="收货地区">
                <el-cascader v-model.trim="formData.region" :options="pcaTextArr">
                </el-cascader>
            </el-form-item>
            <el-form-item prop="address" label="详细地址">
                <el-input v-model.trim="formData.address" placeholder="请输入详细地址"></el-input>
            </el-form-item>
            <el-form-item prop="pay_way" label="支付方式">
                <el-select v-model="formData.pay_way">
                    <el-option v-for="item in payWay" :key="item.value" :value="item.value"
                        :label="item.label"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item label="订单商品">
                <el-table :data="cartList">
                    <el-table-column prop="id" label="序号" min-width="60"></el-table-column>
                    <el-table-column prop="cover" label="商品封面" min-width="100">
                        <template v-slot="props">
                            <el-image v-if="props.row.cover" :src="props.row.cover" style="width: 100px;"></el-image>
                            <el-text v-else type="danger">暂无图片</el-text>
                        </template>
                    </el-table-column>
                    <el-table-column prop="name" label="商品名称" min-width="60"></el-table-column>
                    <el-table-column prop="price" label="商品价格" min-width="60"></el-table-column>
                    <el-table-column prop="num" label="商品数量" min-width="120">
                        <template v-slot="props">
                            <el-input-number v-model="props.row.num" :min="1" />
                        </template>
                    </el-table-column>
                    <el-table-column prop="commission_rate" label="商品佣金比例" min-width="60"></el-table-column>
                    <el-table-column label="操作" min-width="60">
                        <template v-slot="props">
                            <el-button plain size="small" type="danger" @click="del(props.$index)">删除</el-button>
                        </template>
                    </el-table-column>

                </el-table>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submit" plain>确认提交</el-button>
            </el-form-item>
        </el-form>
    </el-card>
</template>

<script setup>
import { payWay } from '@/utils/config'
import { pcaTextArr } from 'element-china-area-data'
import useCartStore from '@/stores/cart'
import { storeToRefs } from 'pinia'
import { createSaleOrder, getCustomerListOfMe } from '@/utils/api'
import { ref } from 'vue'
import { ElNotification } from 'element-plus'
import { useRouter } from 'vue-router'
import { withConfirm } from '@/utils/util'
const router = useRouter()
const orderForm = ref('orderForm')
const formData = ref({
    customer_id: '',
    pay_way: '',
    consignee: '',
    // 和省市区级联选择器进行绑定
    region: [],
    phone: '',
    province: '',
    city: '',
    county: '',
    address: ''
})
const rules = {
    consignee: [{ required: true, message: '请输入收货人' }],
    phone: [{ required: true, message: '请输入收货人联系方式' }],
    region: [{ required: true, message: '请选择省市区' }],
    address: [{ required: true, message: '请输入详细地址' }],
    customer_id: [{ required: true, message: '请选择客户' }]
}
const cartStore = useCartStore()
const { cartList } = storeToRefs(cartStore)
const { resetCartProduct, removeCartProduct } = cartStore
const customerList = ref([])
const loading = ref(true)
// 根据用户输入关键词, 搜索客户
const queryCustomer = async (value) => {
    if (value) {
        const result = await getCustomerListOfMe({ name: value })
        if (result.status === 200) {
            customerList.value = result.data.results
            loading.value = false
        }
    }
}
// 监听客户选择下拉框
const customerChange = (value) => {
    const customer = customerList.value.find(item => item.id === value)
    const { name, phone, province, city, county, address } = customer
    formData.value.region = [province, city, county]
    formData.value.consignee = name
    formData.value.phone = phone
    formData.value.address = address
    formData.value.province = province
    formData.value.city = city
    formData.value.county = county
}
const submit = () => {
    orderForm.value.validate(async valid => {
        if (valid) {
            // 添加订单商品
            formData.value.order_items = cartList.value
            // 提交订单
            const result = await createSaleOrder(formData.value)
            if (result.status === 201) {
                ElNotification.success('订单提交成功')
                // 清空购物车中的商品数据
                resetCartProduct()
                // 跳转到订单支付页面: 根据支付方式跳转到不同的地址
                router.push({ name: 'saleOrderDetail', params: { id: result.data.id } })
            }
        }
    })
}

const del = (index) => {
    withConfirm(() => {
        removeCartProduct(index)
    })
}
</script>

<style></style>