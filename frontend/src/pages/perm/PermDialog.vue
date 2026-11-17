<template>
    <el-dialog @close="reset" :title="title" v-model="visible">
        <el-form label-width="80px" ref="permForm" :rules="rules" :model="formData">
            <el-form-item prop="parent" label="父级节点">
                <!-- multiple: 支持多选 -->
                <!-- el-tree-select:el-tree和el-select的二次封装 -->
                <!-- clearable: 显示清空图标 -->
                <el-tree-select clearable filterable check-strictly :props="{ value: 'id', label: 'name' }"
                    v-model="formData.parent" :data="permList" />
            </el-form-item>
            <el-form-item prop="name" label="权限名称">
                <el-input v-model="formData.name" placeholder="请输入权限名称"></el-input>
            </el-form-item>
            <el-form-item prop="code" label="权限编码">
                <el-input v-model="formData.code" placeholder="请输入权限编码"></el-input>
            </el-form-item>
            <el-form-item prop="status" label="权限状态">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true">启用</el-radio>
                    <el-radio :value="false">禁用</el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item prop="is_public" label="是否公开">
                <el-switch v-model="formData.is_public" :inactive-value="false" :active-value="true"></el-switch>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button @click="submit" type="primary">确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { createPerm, updatePerm } from '../../utils/api'
import { ref, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import usePermStore from '../../stores/perm'
import { ElMessage } from 'element-plus'
import { useDialog } from '../../utils/hooks'
// 获取form表单组件对象
const permForm = useTemplateRef('permForm')
// 表单数据初始值
const formInitData = {
    name: '',
    code: '',
    status: '',
    parent: '',
    is_public: false
}
// 调用自定义组合函数
const { title, visible, pk, formData, reset } = useDialog({ title: '新增权限', formInitData, formRef: permForm })
// 获取权限模块数据仓库对象
const permStore = usePermStore()
// 解构请求权限列表的方法
const { getPermListAction } = permStore
// 解构需要的数据
const { permList } = storeToRefs(permStore)
// 表单验证规则
const rules = {
    // parent: [{ required: true, message: '请选择父级节点' }],
    name: [{ required: true, message: '请输入权限名称' }],
    code: [{ required: true, message: '请输入权限编码' }],
    status: [{ required: true, message: '请选择权限状态' }]
}
const submit = () => {
    permForm.value.validate(async valid => {
        if (valid) {
            let result
            if (pk.value > 0) {
                // 提交更新表单
                result = await updatePerm(pk.value, formData.value)
            } else {
                // 提交新增表单
                result = await createPerm(formData.value)
            }
            if ([201, 200].includes(result.status)) {
                ElMessage.success('操作成功')
                // 重置数据
                reset()
                // 更新权限列表数据
                getPermListAction()
            }
        }
    })
}
// 打开更新表单
// obj: 待编辑的权限数据
const openUpdateForm = ({ id, name, code, status, parent, is_public }) => {
    pk.value = id
    // 更新表单数据
    formData.value = { name, code, status, parent, is_public }
    // 显示对话框
    visible.value = true,
        // 更新对话框标题
        title.value = '更新权限'
}
// 暴漏数据给外部
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>