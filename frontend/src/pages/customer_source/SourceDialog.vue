<template>
    <el-dialog @close="reset" :title="title" v-model="visible">
        <el-form :model="formData" :rules="rules" ref="sourceForm" label-width="80px">
            <el-form-item prop="name" label="来源名称">
                <el-input v-model="formData.name" placeholder="请输入客户来源名称"></el-input>
            </el-form-item>
            <el-form-item prop="status" label="来源状态">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true" label="启用"></el-radio>
                    <el-radio :value="false" label="禁用"></el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button @click="submit" type="primary" plain>确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { createCustomerSource, updateCustomerSource } from '@/utils/api'
import { useDialog } from '@/utils/hooks'
import { ElMessage } from 'element-plus';
import { useTemplateRef } from 'vue';
const formInitData = {
    name: '', status: ''
}
const sourceForm = useTemplateRef('sourceForm')
const { pk, title, visible, formData, reset } = useDialog({ formInitData, title: '新增客户来源', formRef: sourceForm })
const rules = {
    name: [{ required: true, message: '请输入客户来源名称' }],
    status: [{ required: true, message: '请选择客户来源状态' }]
}
const openUpdateForm = ({ id, name, status }) => {
    pk.value = id
    formData.value = { name, status }
    visible.value = true
    title.value = '更新客户来源'
}
const emit = defineEmits(['updateSource'])
const submit = () => {
    sourceForm.value.validate(async valid => {
        let result
        if (valid) {
            if (pk.value > 0) {
                // 更新
                result = await updateCustomerSource(pk.value, formData.value)
            } else {
                // 新增
                result = await createCustomerSource(formData.value)
            }
            if (result.status === 200 || result.status === 201) {
                ElMessage.success('操作成功')
                reset()
                // 通知父组件更新列表
                emit('updateSource')
            }
        }
    })
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>