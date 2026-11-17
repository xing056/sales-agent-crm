import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getCommissionList, getCommissionListOfMe } from '@/utils/api'
const useCommisionStore = defineStore('commission', () => {
    // 员工提成列表
    const commisionList = ref([])
    // 员工提成总数
    const commisionCount = ref(0)
    // 请求员工提成数据 params={page,size}
    const getCommissionAction = async (params = {}) => {
        const result = await getCommissionList(params)
        if (result.status === 200) {
            commisionList.value = result.data.results
            commisionCount.value = result.data.count
        }
    }
    // 获取我的提成列表
    const getMyCommissionAction = async (params = {}) => {
        const result = await getCommissionListOfMe(params)
        if (result.status === 200) {
            commisionList.value = result.data.results
            commisionCount.value = result.data.count
        }
    }
    return {
        commisionList, commisionCount, getCommissionAction, getMyCommissionAction
    }
})
export default useCommisionStore