<template>
    <el-card>
        <h3>个人资料</h3>
        <el-divider></el-divider>
        <el-form ref="userForm" :rules="rules" :model="formData">
            <el-descriptions border title="账号资料">
                <el-descriptions-item label="用户名">
                    {{ loginInfo.username }}
                </el-descriptions-item>
                <el-descriptions-item label="角色">
                    <el-space>
                        <el-tag v-for="item in loginInfo.role" :key="item.id">{{ item.name }}</el-tag>
                    </el-space>
                </el-descriptions-item>
                <el-descriptions-item v-if="isEdit" label="密码">
                    <el-form-item prop="password">
                        <el-input show-password clearable v-model.trim="formData.password" type="password" placeholder="请输入新密码"></el-input>
                    </el-form-item>
                </el-descriptions-item>
                <el-descriptions-item label="操作">
                    <template v-if="isEdit">
                        <el-button @click="submit" type="primary" plain>确认修改</el-button>
                        <el-button @click="isEdit = false" type="info" plain>取消</el-button>
                    </template>
                    <el-button @click="isEdit = true" type="primary" plain v-else>修改密码</el-button>
                </el-descriptions-item>
            </el-descriptions>
        </el-form>
        <el-divider></el-divider>
        <!-- 如果账号有关联的员工数据, 则加载该组件 -->
        <EmpForm v-if="empInfo.id" :empId="empInfo.id" />
    </el-card>
</template>

<script setup>
import { ref, useTemplateRef } from 'vue'
import EmpForm from '../../components/EmpForm.vue';
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user';
import { updateUser } from '@/utils/api'
import { ElMessage } from 'element-plus';
const userStore = useUserStore()
// 通过登录信息获取员工id
const { empInfo, loginInfo } = storeToRefs(userStore)
const isEdit = ref(false)
const formData = ref({
    password: ''
})
const rules = {
    password: [{ required: true, message: '请输入新密码' }]
}
const userForm = useTemplateRef('userForm')
const submit = () => {
    userForm.value.validate(async valid => {
        if (valid) {
            // 提交表单: 调用更新用户的接口
            const result = await updateUser(loginInfo.value.id, formData.value)
            if (result.status === 200) {
                ElMessage.success("操作成功")
                isEdit.value = false
            }
        }
    })
}
</script>

<style></style>