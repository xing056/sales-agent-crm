<template>
  <el-card>
    <h3>部门【{{ department.name }}】员工列表</h3>
    <!-- 调用员工列表组件 -->
    <EmpList :department_id="department_id" />
  </el-card>
</template>

<script setup>
import EmpList from '@/components/EmpList.vue'
import { useRoute } from 'vue-router'
import { onMounted, provide, ref } from 'vue'
import { getDepartment } from '@/utils/api'
const route = useRoute()
// 获取路径参数: department_id
const department_id = parseInt(route.params.id)
// 将department_id传递给新增员工的对话框组件
provide('department_id', department_id)
// 获取部门数据
const department = ref({})
onMounted(async () => {
  const result = await getDepartment(department_id)
  if (result.status === 200) {
    department.value = result.data
  }
})

</script>

<style></style>