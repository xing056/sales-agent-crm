import { defineStore } from 'pinia'
import { getCustomerTrackingList } from '@/utils/api'
import { ref } from 'vue'
const useCustomerTrackingStore = defineStore('customer_tracking', () => {
    //客户跟踪记录列表
    const customerTrackingList = ref([])
    //客户跟踪记录总数
    const customerTrackingCount = ref(0)
    // 请求客户跟踪数据
    const getCustomerTrackingAction = async (params = {}) => {
        const result = await getCustomerTrackingList(params)
        if (result.status === 200) {
            customerTrackingList.value = result.data.results
            customerTrackingCount.value = result.data.count
        }
    }
    return { customerTrackingList, customerTrackingCount, getCustomerTrackingAction }
})
export default useCustomerTrackingStore