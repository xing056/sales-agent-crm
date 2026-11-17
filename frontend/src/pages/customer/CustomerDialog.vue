<template>
    <el-dialog @close="reset" :title="title" v-model="visible">
        <el-form label-width="80px" label-position="right" :rules="rules" :model="formData" ref="customerForm">
            <el-form-item prop="source_id" label="客户来源">
                <el-select clearable placeholder="请选择客户来源" v-model="formData.source_id">
                    <el-option v-for="item in customerSourceList" :key="item.id" :value="item.id"
                        :label="item.name"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item v-if="formData.source_id === 1" prop="parent_id" label="推荐者">
                <el-select :loading="loading" filterable clearable remote :remote-method="queryCustomer"
                    placeholder="请选择推荐者" v-model="formData.parent_id">
                    <el-option v-for="item in customerList" :key="item.id" :value="item.id"
                        :label="item.name"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="name" label="客户姓名">
                <el-input placeholder="请输入客户姓名" v-model="formData.name"></el-input>
            </el-form-item>
            <el-form-item prop="phone" label="客户电话">
                <el-input placeholder="请输入客户电话" v-model="formData.phone"></el-input>
            </el-form-item>
            <el-form-item prop="name" label="地区">
                <el-cascader @change="regionChange" :options="pcaTextArr" v-model="formData.region">
                </el-cascader>
            </el-form-item>
            <el-form-item prop="name" label="详细地址">
                <el-input placeholder="请输入客户详细地址" v-model="formData.address"></el-input>
            </el-form-item>
            <el-form-item prop="remark" label="客户备注">
                <el-input placeholder="请输入客户备注" v-model="formData.remark"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button @click="submit" type="primary" plain>确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import useCustomerSourceStore from '@/stores/customer_source';
import { storeToRefs } from 'pinia'
import { createCustomer, getCustomerList } from '@/utils/api'
import { pcaTextArr } from 'element-china-area-data'
import { useDialog } from '@/utils/hooks'
import { useTemplateRef, ref } from 'vue';
import { ElMessage } from 'element-plus';
// 获取客户来源数据仓库对象
const sourceStore = useCustomerSourceStore()
const { customerSourceList } = storeToRefs(sourceStore)
const { getCustomerSource } = sourceStore
// 请求客户来源数据
getCustomerSource()

const formInitData = {
    name: '', phone: '', province: '', city: '', county: '', address: '', parent_id: '', user_id: '', remark: '', region: []
}
const customerForm = useTemplateRef('customerForm')
const { title, visible, reset, formData } = useDialog({ formInitData, title: '新增客户', formRef: customerForm })
// 推荐者列表
const customerList = ref([])
const loading = ref(true)
const queryCustomer = async (name) => {
    if (name) {
        // 根据关键词查询客户列表数据
        const result = await getCustomerList({ name })
        if (result.status === 200) {
            customerList.value = result.data.results
            loading.value = false
        }
    }
}
const rules = {
    name: [{ required: true, message: '请输入客户姓名' }],
    phone: [{ pattern: /^1[3456789]\d{9}$/, required: true, message: '请输入客户手机号' }],
    region: [{ required: true, message: '请选择地区' }],
    address: [{ required: true, message: '请输入详细地址' }],
    source_id: [{ required: true, message: '请选择客户来源' }],
}
const regionChange = (region) => {
    const [province, city, county] = region
    formData.value.province = province
    formData.value.city = city
    formData.value.county = county
}
const emit = defineEmits(['updateCustomer'])
const submit = () => {
    customerForm.value.validate(async valid => {
        if (valid) {
            if (!formData.value.parent_id) {
                delete formData.value.parent_id
            }
            const result = await createCustomer(formData.value)
            if (result.status === 201) {
                ElMessage.success('操作成功')
                reset()
                // 请求最新的客户列表数据
                emit('updateCustomer')
                customerList.value = []
            }
        }
    })
}
defineExpose({
    visible
})
</script>

<style></style>