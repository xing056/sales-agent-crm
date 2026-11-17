import { defineStore } from 'pinia'
import { getCategoryList } from '@/utils/api'
import { ref } from 'vue'
const useCategoryStore = defineStore('category', () => {
    // 分类列表数据
    const categoryList = ref([])
    // 请求分类列表数据
    const getCategoryListAction = async () => {
        const result = await getCategoryList()
        if (result.status === 200) {
            categoryList.value = result.data
        }
    }
    return { categoryList, getCategoryListAction }
})
export default useCategoryStore