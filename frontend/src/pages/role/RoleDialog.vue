<template>
    <el-dialog @close="resetHandler" :title="title" v-model="visible">
        <el-form :rules="rules" :model="formData" ref="roleForm">
            <el-form-item prop="name" label="角色名称">
                <el-input v-model="formData.name" placeholder="请输入角色名称"></el-input>
            </el-form-item>
            <el-form-item prop="permission_ids" label="角色权限">
                <el-tree ref="tree" style="max-width: 600px" :data="permList" show-checkbox node-key="id"
                    :default-checked-keys="checkedKeys" :props="defaultProps" />
            </el-form-item>
            <el-form-item prop="status" label="角色状态">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true">启用</el-radio>
                    <el-radio :value="false">禁用</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item prop="remark" label="角色说明">
                <el-input v-model="formData.remark" type="textarea" :rows="3" placeholder="请输入角色说明"></el-input>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="resetHandler">取消</el-button>
            <el-button @click="submit" type="primary">确认提交</el-button>
        </template>
    </el-dialog>
</template>
<script setup>
import { storeToRefs } from 'pinia'
import usePermStore from '@/stores/perm';
import { useTemplateRef, ref } from 'vue';
import { useDialog } from '../../utils/hooks'
import { createRole, updateRole } from '../../utils/api'
import { ElMessage } from 'element-plus'
const tree = useTemplateRef('tree')
// 树形组件默认勾选的节点
const checkedKeys = ref([])
// 获取权限模块数据仓库对象
const permStore = usePermStore()
// 请求权限列表的方法
const { getPermListAction } = permStore
// 请求权限列表
getPermListAction()
// 获取权限列表
const { permList } = storeToRefs(permStore)
// 获取表单组件对象
const roleForm = useTemplateRef('roleForm')
// 表单初始数据
const formInitData = {
    name: '', permission_ids: [], status: '', remark: ''
}
const { pk, title, visible, formData, reset } = useDialog({ title: '新增角色', formInitData, formRef: roleForm })
const rules = {
    name: [{ required: true, message: '请输入角色名称' }],
    permission_ids: [{ required: true, message: '请选择角色权限' }],
    status: [{ required: true, message: '请选择角色状态' }],
    remark: [{ required: true, message: '请输入角色说明' }],
}
const emit = defineEmits(['updateRole'])
const resetHandler = () => {
    // 取消树形组件中勾选过的节点
    checkedKeys.value = []
    tree.value.setCheckedKeys([])
    // 数据重置
    reset()
}
const submit = () => {
    // 手动获取用户勾选的权限节点, 将其同步到表单数据中
    formData.value.permission_ids = tree.value.getCheckedKeys()
    roleForm.value.validate(async valid => {
        if (valid) {
            // 提交表单数据
            let result
            if (pk.value > 0) {
                // 执行更新操作
                result = await updateRole(pk.value, formData.value)
            } else {
                // 执行新增操作
                result = await createRole(formData.value)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                // 重新请求最新的角色列表: 通知父组件请求最新的角色列表
                // 触发自定义事件updateRole
                emit('updateRole')
                // 数据重置
                resetHandler()
            }
        }
    })
}
// obj: 待更新的角色数据
const openUpdateForm = ({ id, name, permission, status, remark }) => {
    // 更新当前待更新的数据唯一标识pk
    pk.value = id
    // 更新对话框标题
    title.value = '更新角色'
    // 显示对话框
    visible.value = true
    // 更新表单数据
    formData.value = { name, status, remark }
    formData.value.permission_ids = permission.map(item => item.id)
    // 设置树形组件默认勾选节点
    checkedKeys.value = formData.value.permission_ids
}

defineExpose({
    visible, openUpdateForm
})
const defaultProps = {
    children: 'children',
    label: 'name',
}
</script>

<style></style>