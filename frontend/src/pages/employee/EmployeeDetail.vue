<template>
    <el-card>
        <div class="actions">
            <el-button @click="$router.back()" type="primary" plain>返回</el-button>
        </div>
        <EmpForm :empId="id" />
        <el-divider>关联账号</el-divider>
        <el-descriptions border v-if="userInfo.username">
            <el-descriptions-item label="用户名">
                {{ userInfo.username }}
            </el-descriptions-item>
            <el-descriptions-item label="角色信息">
                <el-space>
                    <el-tag v-for="item in userInfo.role" :key="item.id">{{ item.name }}</el-tag>
                </el-space>
            </el-descriptions-item>
            <el-descriptions-item label="账号状态">
                <el-tag :type="userInfo.status ? 'primary' : 'danger'">{{ userInfo.status ? '正常' : '禁用' }}</el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="操作">
                <!-- 将employee数据表中的user_id置空 -->
                <el-button @click="unBindUser" type="danger" plain>解除绑定</el-button>
            </el-descriptions-item>
        </el-descriptions>
        <el-descriptions v-else border>
            <el-descriptions-item label="绑定账号">
                <el-form ref="bindUserForm" inline :rules="rules" :model="userFormData">
                    <el-form-item prop="user_id">
                        <!-- <el-input placeholder="请输入要绑定的账号用户名"></el-input> -->
                        <el-select clearable v-model="userFormData.user_id" :props="{ value: 'id', label: 'username' }"
                            filterable remote reserve-keyword placeholder="请输入要绑定的账号用户名" :remote-method="remoteMethod"
                            :loading="loading" style="width: 240px">
                            <el-option v-for="item in userList" :key="item.id" :label="item.username"
                                :value="item.id" />
                        </el-select>
                    </el-form-item>
                    <el-form-item>
                        <el-button @click="bindUser" type="primary">立即绑定</el-button>
                    </el-form-item>
                </el-form>
            </el-descriptions-item>
        </el-descriptions>
    </el-card>
</template>

<script setup>
import { ref, useTemplateRef } from 'vue'
import EmpForm from '../../components/EmpForm.vue';
import { useRoute } from 'vue-router'
import { getEmployee, getUserList, updateEmployee } from '@/utils/api'
import { onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { withConfirm } from '@/utils/util';
// 通过路径参数获取员工id
const route = useRoute()
const { id } = route.params
const userInfo = ref({})


// 要获取账号数据, 必须获取员工数据
onMounted(async () => {
    // 获取员工资料
    const result = await getEmployee(id)
    if (result.status === 200) {
        if (result.data.user) {
            userInfo.value = result.data.user

        }
    }
})
// 获取表单组件对象
const bindUserForm = useTemplateRef('bindUserForm')
// 表单对象
const userFormData = ref({ user_id: '' })
const rules = {
    user_id: [{ required: true, message: '请选择要绑定的账号' }]
}
// 让select下拉框显示一个加载中的图标
const loading = ref(true)
// 保存搜索到的账号列表
const userList = ref([])
// 实现搜索的方法
// keywords: 用户输入的搜索关键词
const remoteMethod = async (username) => {
    if (username) {
        // 通过用户输入的搜索关键词搜索账号数据
        const result = await getUserList({ username })
        if (result.status === 200) {
            userList.value = result.data.results
        }
        // 关闭loading图标
        loading.value = false
    }
}
const bindUser = () => {
    bindUserForm.value.validate(async valid => {
        if (valid) {
            // 请求数据接口, 实现绑定账号, 更新员工数据表
            const result = await updateEmployee(id, userFormData.value)
            if (result.status === 200) {
                ElMessage.success('操作成功')
                // 更新userInfo, 驱动视图更新
                userInfo.value = result.data.user
            }
        }
    })
}
const unBindUser = () => {
    withConfirm(async () => {
        const result = await updateEmployee(id, { user_id: null })
        if (result.status === 200) {
            ElMessage.success('操作成功')
            // 更新userInfo, 驱动视图更新
            userInfo.value = {}
        }
    })
}
</script>

<style></style>