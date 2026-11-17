import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getPositionList } from '@/utils/api'
const usePositionStore = defineStore('position', () => {
    // 职位列表
    const positionList = ref([])
    // 职位总数
    const positionCount = ref(0)
    // 请求职位列表
    const getPositionListAction = async (params = {}) => {
        const result = await getPositionList(params)
        if (result.status === 200) {
            positionList.value = result.data.results
            positionCount.value = result.data.count
        }
    }
    return { positionList, positionCount, getPositionListAction }
})
export default usePositionStore