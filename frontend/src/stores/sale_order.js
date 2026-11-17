import { defineStore } from 'pinia'
import { getSaleOrderList } from '@/utils/api'
import { ref } from 'vue'
const useSaleOrderStore = defineStore('saleOrder', () => {
    // 订单列表
    const saleOrderList = ref([])
    // 订单总数
    const saleOrderCount = ref(0)

    // 请求订单列表数据 params={page,size}
    const getSaleOrderListAction = async (params = {}) => {
        const result = await getSaleOrderList(params)
        if (result.status === 200) {
            saleOrderList.value = result.data.results
            saleOrderCount.value = result.data.count
        }
    }
    return {
        saleOrderList, saleOrderCount, getSaleOrderListAction
    }
})
export default useSaleOrderStore