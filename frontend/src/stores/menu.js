import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMenuList } from '../utils/api'
const useMenuStore = defineStore('menu', () => {
    // 权限列表的数据
    const menuList = ref([])
    // 请求权限列表
    const getMenuListAction = async () => {
        const result = await getMenuList()
        if (result.status === 200) {
            // 更新权限列表数据
            menuList.value = result.data
        }
    }
    return { menuList, getMenuListAction }
})
export default useMenuStore