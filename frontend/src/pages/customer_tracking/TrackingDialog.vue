<template>
    <el-dialog @close="reset" :title="title" v-model="visible">
        <el-form label-width="80px" label-position="right" :rules="rules" :model="formData" ref="trackingForm">
            <el-form-item v-if="!pk" label="选择客户" prop="customer_id">
                <el-select v-model="formData.customer_id" filterable clearable remote :remote-method="queryCustomer"
                    :loading="loading">
                    <el-option v-for="item in customerList" :key="item.id" :value="item.id"
                        :label="item.name"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item v-else label="客户信息">
                {{ formData.customer.name }}-{{ formData.customer.phone }}
            </el-form-item>
            <el-form-item prop="tracking_way" label="跟踪方式">
                <el-select v-model="formData.tracking_way" placeholder="请选择跟踪方式">
                    <el-option v-for="item in trackingWay" :key="item.value" :value="item.value"
                        :label="item.label"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="tracking_time" label="跟踪时间">
                <el-date-picker v-model="formData.tracking_time" type="datetime" placeholder="请选择跟踪时间"
                    value-format="YYYY/MM/DD HH:mm:ss" />
            </el-form-item>
            <el-form-item prop="status" label="跟踪状态">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true" label="成功"></el-radio>
                    <el-radio :value="false" label="失败"></el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item prop="description" label="跟踪描述">
                <el-input v-model.trim="formData.description" type="textarea" :rows="3"
                    placeholder="请输入跟踪描述"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button @click="submit" type="primary">确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { inject, onMounted, ref } from 'vue'
import { trackingWay } from '@/utils/config'
import { useDialog } from '@/utils/hooks'
import { createCustomerTracking, getCustomerList, updateCustomerTracking, getCustomer } from '@/utils/api'
import { useTemplateRef } from 'vue'
// 通过inject获取祖先组件提供的客户id
const customerId = inject('customerId', null)
const trackingForm = useTemplateRef('trackingForm')
const formInitData = {
    customer_id: '',
    tracking_way: '',
    tracking_time: '',
    status: '',
    description: ''
}
const loading = ref(true)
// 客户下拉框中的选项数据
const customerList = ref([])
const { pk, visible, title, reset, formData } = useDialog({ title: '新增跟踪记录', formInitData, formRef: trackingForm })
// value: 客户姓名 或者 客户id
const queryCustomer = async (value) => {
    if (value) {
        let result
        if (typeof value === 'string') {
            // 返回值是客户列表
            result = await getCustomerList({ name: value })
        } else {
            // 根据客户id获取客户数据: 返回单条客户对象
            result = await getCustomer(value)
        }
        if (result.status === 200) {
            if (result.data.results) {
                customerList.value = result.data.results
            } else {
                customerList.value = [result.data]
            }
            // 根据用户输入关键词查询客户
            loading.value = false
        }
    }
}
onMounted(() => {
    // 手动调用queryCustomer, 获取客户列表
    queryCustomer(customerId)
    // 更新和客户下拉框绑定的数据
    formData.value.customer_id = customerId
})
const rules = {
    customer_id: [{ required: true, message: '请选择客户' }],
    tracking_way: [{ required: true, message: '请选择跟踪方式' }],
    tracking_time: [{ required: true, message: '请选择跟踪时间' }],
    status: [{ required: true, message: '请选择跟踪状态' }],
    description: [{ required: true, message: '请输入跟踪描述' }],
}
const emit = defineEmits(['updateTracking'])
const submit = () => {
    trackingForm.value.validate(async valid => {
        let result
        if (valid) {
            if (pk.value > 0) {
                // 更新
                result = await updateCustomerTracking(pk.value, formData.value)
            } else {
                result = await createCustomerTracking(formData.value)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                reset()
                // 通知父组件更新跟踪数据
                emit('updateTracking')
            }
        }
    })
}

const openUpdateForm = ({ id, customer, tracking_way, tracking_time, status, description }) => {
    pk.value = id
    formData.value = { tracking_way, tracking_time, status, customer, description }
    visible.value = true
    title.value = '更新跟踪记录'
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>