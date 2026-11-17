import { defineStore } from 'pinia'
import { getProductList } from '@/utils/api'
import { ref } from 'vue'
const useProductStore = defineStore('prodcut', () => {
    // 商品列表
    const productList = ref([])
    // 商品总数
    const productCount = ref(0)
    // 请求商品数据 params={page,size}
    const getGoodsListAction = async (params = {}) => {
        const result = await getProductList(params)
        if (result.status === 200) {
            productList.value = result.data.results
            productCount.value = result.data.count
        }
    }
    return { productList, productCount, getGoodsListAction }
})
export default useProductStore