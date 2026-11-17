<template>
    <el-dialog @close="reset" :title="title" v-model="visible" width="500">
        <el-form label-width="80px" label-position="left" ref="userForm" :rules="rules" :model="formData">
            <el-form-item label="用户名" prop="username">
                <span v-if="pk > 0">{{ formData.username }}</span>
                <el-input v-else clearable v-model="formData.username" placeholder="请输入用户名"></el-input>
            </el-form-item>
            <el-form-item label="角色" prop="role_ids">
                <!-- multiple: 支持多选 -->
                <!-- clearable: 支持清空功能 -->
                <!-- vue3中v-if指令和v-for指令如果同时应用在同一个元素上,v-if先执行( vue2中v-for先执行 )  -->
                <el-select clearable multiple v-model="formData.role_ids" placeholder="请选择角色类型">
                    <el-option v-for="item in activeRoleList" :key="item.id" :label="item.name"
                        :value="item.id"></el-option>
                </el-select>
            </el-form-item>

            <el-form-item label="密码" prop="password">
                <el-input type="password" show-password clearable v-model="formData.password"
                    placeholder="请输入密码"></el-input>
            </el-form-item>
            <el-form-item label="手机号码" prop="phone">
                <el-input clearable :maxlength="11" v-model="formData.phone" placeholder="请输入手机号码"></el-input>
            </el-form-item>
            <el-form-item label="电子邮箱" prop="email">
                <el-input clearable v-model="formData.email" placeholder="请输入电子邮箱"></el-input>
            </el-form-item>
            <el-form-item label="状态 " prop="status">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true" label="启用"></el-radio>
                    <el-radio :value="false" label="禁用"></el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item label="超级用户 " prop="is_superuser">
                <el-switch v-model="formData.is_superuser"></el-switch>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button type="primary" @click="submit">确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { useDialog } from '../../utils/hooks'
import { useTemplateRef, computed } from 'vue'
import { storeToRefs } from 'pinia'
import useRoleStore from '@/stores/role'
import { createUser, updateUser } from '@/utils/api'
import { ElMessage } from 'element-plus'
// 获取角色模块数据仓库对象
const roleStore = useRoleStore()
const { getRoleListAction } = roleStore
// 角色列表
const { roleList } = storeToRefs(roleStore)
// 请求角色列表
getRoleListAction()
// 获取正常状态的角色列表数据
const activeRoleList = computed(() => {
    return roleList.value.filter(item => item.status)
})
// 获取表单组件对象
const userForm = useTemplateRef('userForm')
const formInitData = {
    username: '',
    password: '',
    status: '',
    phone: '',
    email: '',
    is_superuser: false
}
const { pk, title, visible, reset, formData } = useDialog({ title: '新增用户', formInitData, formRef: userForm })
const phoneValid = (rule, value, callback) => {
    const reg = /^1[3456789]\d{9}$/
    if (!reg.test(formData.value.phone)) {
        return callback(new Error('手机号码格式不正确'))
    }
    // 表示表单验证通过
    callback()
}
const emailValid = (rule, value, callback) => {
    const reg = /^\w+@\w+(\.\w+){1,2}$/
    if (!reg.test(formData.value.email)) {
        return callback(new Error('电子邮箱格式不正确'))
    }
    // 表示表单验证通过
    callback()
}
const rules = {
    role_ids: [{ required: true, message: '请选择角色' }],
    username: [{ required: true, message: '请输入用户名' }],
    password: [{ required: true, message: '请输入密码' }],
    email: [{ required: true, message: '请输入邮箱' }, { validator: emailValid }],
    phone: [{ required: true, message: '请输入手机号码' }, { validator: phoneValid }],
    status: [{ required: true, message: '请选择用户状态' }]
}
const emit = defineEmits(['updateUser'])
const submit = () => {
    userForm.value.validate(async valid => {
        if (valid) {
            let result
            if (pk.value > 0) {
                result = await updateUser(pk.value, formData.value)
            } else {
                result = await createUser(formData.value)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                // 重置数据
                reset()
                // 获取最新的用户列表
                emit('updateUser')
            }
        }
    })
}
const openUpdateForm = ({ id, username, phone, email, status, role, is_superuser }) => {
    pk.value = id
    title.value = '更新用户'
    visible.value = true
    const role_ids = role.map(item => item.id)
    formData.value = { username, phone, email, status, role_ids, is_superuser }
}

defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>