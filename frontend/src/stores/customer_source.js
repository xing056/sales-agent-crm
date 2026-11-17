import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCustomerSourceList } from '@/utils/api'
const useCustomerSourceStore = defineStore('customer_source', () => {
    // 客户来源列表
    const customerSourceList = ref([])
    // 客户来源总数
    const customerSourceCount = ref(0)
    // 请求客户来源数据 params={page,size}
    const getCustomerSource = async (params = {}) => {
        const result = await getCustomerSourceList(params)
        if (result.status === 200) {
            customerSourceList.value = result.data.results
            customerSourceCount.value = result.data.count
        }
    }
    return {
        customerSourceList, customerSourceCount, getCustomerSource
    }
})
export default useCustomerSourceStore