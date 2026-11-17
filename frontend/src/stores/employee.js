import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getEmployeeList } from '@/utils/api'
const useEmployeeStore = defineStore('employee', () => {
    // 员工列表
    const employeeList = ref([])
    // 员工总数
    const employeeCount = ref(0)
    // 请求员工列表
    const getEmployeeListAction = async (params = {}) => {
        const result = await getEmployeeList(params)
        if (result.status === 200) {
            employeeList.value = result.data.results
            employeeCount.value = result.data.count
        }
    }
    return { employeeList, employeeCount, getEmployeeListAction }
})
export default useEmployeeStore