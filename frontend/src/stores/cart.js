import { defineStore } from 'pinia'
import { ref } from 'vue'
const useCartStore = defineStore('cart', () => {
    // 购物车商品列表 {id,num,name,price,commission_rate}
    const cartList = ref([])
    // 添加商品到购物车
    const addCartProduct = (product) => {
        const index = cartList.value.findIndex(item => item.id === product.id)
        // 说明商品之前已经存在于购物商品列表中
        if (index != -1) {
            cartList.value[index].num += 1
        } else {
            const { id, name, price, commission_rate, cover } = product
            cartList.value.push({
                id, name, price, commission_rate, cover, num: 1
            })
        }
    }
    // 批量添加商品到购物车商品列表中
    const bulkAddCartProduct = (productlist) => {
        productlist.forEach(item => {
            addCartProduct(item)
        })
    }

    // 删除指定商品
    const removeCartProduct = (index) => {
        cartList.value.splice(index, 1)
    }
    // 清空购物车商品列表数据
    const resetCartProduct = () => {
        cartList.value = []
    }
    return { cartList, addCartProduct, bulkAddCartProduct, resetCartProduct, removeCartProduct }
}, { persist: true })
export default useCartStore