<template>
    <el-card>
        <h3>客户【{{ customer.name }}】跟踪记录</h3>
        <TrackingList :customerId="customerId" />
    </el-card>
</template>

<script setup>
import { useRoute } from 'vue-router'
import TrackingList from '@/components/TrackingList.vue'
import { onMounted, ref,provide } from 'vue'
import { getCustomer } from '@/utils/api'
const route = useRoute()
// 获取路径参数
const customerId = parseInt(route.params.id)
// 通过provide向后代组件提供客户id
provide('customerId', customerId)
const customer = ref({})
onMounted(async () => {
    const result = await getCustomer(customerId)
    if (result.status === 200) {
        customer.value = result.data
    }
})

</script>

<style></style>