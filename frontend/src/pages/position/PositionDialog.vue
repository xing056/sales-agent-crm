<template>
    <el-dialog @close="reset" :title="title" v-model="visible">
        <el-form :rules="rules" :model="formData" label-width="80px" ref="positionRef">
            <el-form-item prop="name" label="职位名称">
                <el-input v-model.trim="formData.name" placeholder="请输入职位名称"></el-input>
            </el-form-item>
            <el-form-item prop="level" label="职位等级">
                <el-input @input="levelInput" v-model.number="formData.level" placeholder="请输入职位等级"></el-input>
            </el-form-item>
            <el-form-item prop="status" label="职位状态">
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
import { createPosition, updatePosition } from '@/utils/api'
import { useDialog } from '@/utils/hooks'
import { useTemplateRef } from 'vue';
import { ElMessage } from 'element-plus';
const positionRef = useTemplateRef('positionRef')
const formInitData = {
    name: '', level: 1, status: ''
}
const { pk, formData, title, visible, reset } = useDialog({ title: '新增职位', formInitData, formRef: positionRef })
const rules = {
    name: [{ required: true, message: '请输入职位名称' }],
    level: [{ required: true, message: '请输入职位等级' }],
    status: [{ required: true, message: '请选择职位状态' }],
}
const emit = defineEmits(['updatePos'])
const submit = () => {
    positionRef.value.validate(async valid => {
        if (valid) {
            let result
            if (pk.value > 0) {
                // 更新
                result = await updatePosition(pk.value, formData.value)
            } else {
                // 新增
                result = await createPosition(formData.value)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                // 重置数据
                reset()
                // 更新职位列表: 通过父组件
                emit('updatePos')
            }
        }
    })
}
// obj:待编辑的职位数据
const openUpdateForm = ({ id, name, level, status }) => {
    pk.value = id
    // 更新表单数据
    formData.value = { name, level, status }
    visible.value = true
}
const levelInput = () => {
    const reg = /^\d+$/
    if (!reg.test(formData.value.level)) {
        formData.value.level = 1
    }
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>