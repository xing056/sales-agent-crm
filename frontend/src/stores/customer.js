import { defineStore } from 'pinia'
import { getCustomerList, getCustomerListOfMe } from '@/utils/api'
import { ref } from 'vue'
const useCustomerStore = defineStore('customer', () => {
    // 客户列表
    const customerList = ref([])
    // 客户总数
    const customerCount = ref(0)
    // 请求客户数据
    const getCustomerAction = async (params = {}) => {
        let result
        if (params.userId) {
            result = await getCustomerListOfMe(params)
        } else {
            result = await getCustomerList(params)
        }
        if (result.status === 200) {
            customerList.value = result.data.results
            customerCount.value = result.data.count
        }
    }
    return { customerList, customerCount, getCustomerAction }
})
export default useCustomerStore