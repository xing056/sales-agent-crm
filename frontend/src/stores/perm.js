import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getPermList } from '../utils/api'
const usePermStore = defineStore('perm', () => {
    // 权限列表的数据
    const permList = ref([])
    // 请求权限列表
    const getPermListAction = async () => {
        const result = await getPermList()
        if (result.status === 200) {
            // 更新权限列表数据
            permList.value = result.data
        }
    }
    return { permList, getPermListAction }
})
export default usePermStore