<template>
    <el-card>
        <h3>我的客户</h3>
        <CustomerList :userId="loginInfo.id" />
    </el-card>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user';
import CustomerList from '@/components/CustomerList.vue'
import { login } from '@/utils/api';
// 通过本地存储获取当前登录账号数据
const userStore = useUserStore()
const { loginInfo } = storeToRefs(userStore)
</script>

<style></style>