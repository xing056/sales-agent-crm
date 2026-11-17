import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getDepartmentList } from '@/utils/api'
const useDepartmentStore = defineStore('department', () => {
    // 部门列表
    const departmentList = ref([])
    // 请求部门列表
    const getDepartmentListAction = async () => {
        const result = await getDepartmentList()
        if (result.status === 200) {
            departmentList.value = result.data
        }
    }
    return { departmentList, getDepartmentListAction }
})
export default useDepartmentStore