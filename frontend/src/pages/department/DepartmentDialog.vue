<template>
    <el-dialog @close="resetHandler" :title="title" v-model="visible">
        <el-form :rules="rules" :model="formData" label-width="80px" ref="departRef">
            <el-form-item prop="parent" label="上级部门">
                <!-- check-strictly: 可以选择任意节点(默认必须选择最后一级节点数据) -->
                <el-tree-select check-strictly v-model="formData.parent" :props="{ value: 'id', label: 'name' }"
                    :data="departmentList"></el-tree-select>
            </el-form-item>
            <el-form-item prop="name" label="部门名称">
                <el-input v-model.trim="formData.name" placeholder="请输入部门名称"></el-input>
            </el-form-item>
            <el-form-item prop="description" label="部门介绍">
                <el-input v-model="formData.description" type="textarea" :rows="3" placeholder="请输入部门介绍"></el-input>
            </el-form-item>
            <el-form-item prop="name" label="部门主管">
                <el-select :loading="loading" clearable filterable v-model="formData.manager_id"
                    :props="{ value: 'id', label: 'name' }" remote :remote-method="remoteMethod">
                    <el-option v-for="item in empList" :key="item.id" :value="item.id" :label="item.name"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="status" label="部门状态">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true" label="启用"></el-radio>
                    <el-radio :value="false" label="禁用"></el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="resetHandler">取消</el-button>
            <el-button @click="submit" type="primary" plain>确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { createDepartment, updateDepartment, getEmployeeList } from '@/utils/api'
import { useDialog } from '@/utils/hooks'
import { useTemplateRef, ref } from 'vue';
import useDepartmentStore from '@/stores/department'
import { storeToRefs } from 'pinia'
import { ElMessage } from 'element-plus';
// 数据接口返回的员工列表
const empList = ref([])
const loading = ref(true)
// name:用户输入关键词
const remoteMethod = async (name) => {
    if (name) {
        // 发送数据请求
        const result = await getEmployeeList({ name })
        if (result.status === 200) {
            empList.value = result.data.results
            loading.value = false
        }
    }
}
const departmentStore = useDepartmentStore()
const { departmentList } = storeToRefs(departmentStore)
const { getDepartmentListAction } = departmentStore
const departRef = useTemplateRef('departRef')
const formInitData = {
    name: '', description: '', status: '', parent: '', manager_id: ''
}
const { pk, formData, title, visible, reset } = useDialog({ title: '新增部门', formInitData, formRef: departRef })
const rules = {
    name: [{ required: true, message: '请输入部门名称' }],
    description: [{ required: true, message: '请输入部门介绍' }],
    status: [{ required: true, message: '请选择部门状态' }],
    // parent: [{ required: true, message: '请选择上级部门' }],
}
const resetHandler = () => {
    reset()
    empList.value = []
}
const submit = () => {
    departRef.value.validate(async valid => {
        if (valid) {
            let result
            if (pk.value > 0) {
                // 更新
                result = await updateDepartment(pk.value, formData.value)
            } else {
                // 新增
                result = await createDepartment(formData.value)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                // 重置数据
                resetHandler()
                // 更新部门列表
                getDepartmentListAction()
            }
        }
    })
}
// obj:待编辑的部门数据
const openUpdateForm = ({ id, name, parent, description, status }) => {
    pk.value = id
    // 更新表单数据
    formData.value = { name, parent, description, status }
    visible.value = true
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>