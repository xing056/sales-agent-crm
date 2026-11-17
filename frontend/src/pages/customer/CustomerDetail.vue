<template>
    <el-card>
        <div class="actions">
            <el-button type="primary" plain @click="$router.back()">返回</el-button>
        </div>
        <el-divider></el-divider>
        <el-form ref="customerForm" :rules="rules" :model="customer">
            <el-descriptions direction="vertical" border title="客户详情">
                <el-descriptions-item label="姓名">
                    <el-form-item v-if="isEidt" prop="name">
                        <el-input v-model.trim="customer.name" placeholder="请输入客户姓名"></el-input>
                    </el-form-item>
                    <template v-else>
                        {{ customer.name }}
                    </template>
                </el-descriptions-item>
                <el-descriptions-item label="联系方式">
                    <el-form-item v-if="isEidt" prop="phone">
                        <el-input v-model.trim="customer.phone" placeholder="请输入联系方式"></el-input>
                    </el-form-item>
                    <template v-else>
                        {{ customer.phone }}
                    </template>
                </el-descriptions-item>
                <el-descriptions-item label="客户等级">
                    {{ customer.level }}
                </el-descriptions-item>
                <el-descriptions-item label="消费次数">
                    {{ customer.order_count }}
                </el-descriptions-item>
                <el-descriptions-item label="消费金额">
                    &yen; {{ customer.order_amount }}
                </el-descriptions-item>
                <el-descriptions-item label="地区">
                    <el-form-item v-if="isEidt" prop="region">
                        <el-cascader v-model.trim="customer.region" @change="regionChange" :options="pcaTextArr">
                        </el-cascader>
                    </el-form-item>
                    <template v-else>
                        {{ customer.province }}-{{ customer.city }}-{{ customer.county }}-{{ customer.address }}
                    </template>
                </el-descriptions-item>
                <el-descriptions-item v-if="isEidt" label="详细地址">
                    <el-form-item prop="address">
                        <el-input v-model="customer.address" placeholder="请输入详细地址"></el-input>
                    </el-form-item>
                </el-descriptions-item>
                <el-descriptions-item label="客户来源">
                    {{ customer.source?.name }}
                </el-descriptions-item>
                <el-descriptions-item label="推荐者">
                    {{ customer.user?.employee?.name }}
                </el-descriptions-item>
                <el-descriptions-item label="客户状态">
                    <el-form-item v-if="isEidt" prop="status">
                        <el-radio-group v-model="customer.status">
                            <el-radio :value="true" label="正常"></el-radio>
                            <el-radio :value="false" label="异常"></el-radio>
                        </el-radio-group>
                    </el-form-item>
                    <template v-else>
                        {{ customer.status ? '正常' : '异常' }}
                    </template>
                </el-descriptions-item>
                <el-descriptions-item label="客户备注">
                    <el-form-item v-if="isEidt" prop="remark">
                        <el-input v-model="customer.remark" placeholder="请输入客户备注"></el-input>
                    </el-form-item>
                    <template v-else>
                        {{ customer.remark ? customer.remark : '暂无' }}
                    </template>
                </el-descriptions-item>
                <el-descriptions-item label="客户资料更新时间">
                    {{ customer.update_time }}
                </el-descriptions-item>
                <el-descriptions-item label="客户添加时间">
                    {{ customer.create_time }}
                </el-descriptions-item>
                <el-descriptions-item label="操作">
                    <template v-if="isEidt">
                        <el-button @click="submit" type="primary" plain>确认提交</el-button>
                        <el-button @click="isEidt = false" type="info" plain>取消</el-button>
                    </template>
                    <el-button @click="isEidt = true" v-else type="primary" plain>编辑</el-button>
                </el-descriptions-item>
            </el-descriptions>
        </el-form>
    </el-card>
</template>

<script setup>
import { pcaTextArr } from 'element-china-area-data'
import { onMounted, ref, useTemplateRef } from 'vue'
import { getCustomer, updateCustomer } from '@/utils/api'
import { useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
const customerForm = useTemplateRef("customerForm")
const isEidt = ref(false)
const route = useRoute()
// 获取路径参数
const customerId = route.params.id
// 根据客户id请求客户详情数据
const customer = ref({})
onMounted(async () => {
    const result = await getCustomer(customerId)
    if (result.status === 200) {
        customer.value = result.data
        const { province, city, county } = result.data
        customer.value.region = [province, city, county]
    }
})
const rules = {
    name: [{ required: true, message: '请输入客户姓名' }],
    phone: [{ pattern: /^1[3456789]\d{9}$/, requried: true, message: '请输入合法的手机号码' }],
    status: [{ required: true, message: '请选择客户状态' }],
    region: [{ required: true, message: '请选择地区' }],
    address: [{ required: true, message: '请输入详细地址' }],
}
const regionChange = (region) => {
    const [province, city, county] = region
    formData.value.province = province
    formData.value.city = city
    formData.value.county = county
}
const submit = () => {
    customerForm.value.validate(async valid => {
        if (valid) {
            const { name, phone, address, region, remark, status } = customer.value
            const [province, city, county] = region
            const result = await updateCustomer(customer.value.id, { name, phone, address, province, city, county, remark, status })
            if (result.status === 200) {
                ElMessage.success('操作成功')
                customer.value = result.data
                const { province, city, county } = result.data
                customer.value.region = [province, city, county]
                isEidt.value = false
            }
        }
    })
}
</script>

<style></style>