import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getRoleList } from '../utils/api'
const useRoleStore = defineStore('role', () => {
    // 角色列表的数据
    const roleList = ref([])
    // 角色总数
    const roleCount = ref(0)
    // 请求角色列表
    // params={page}
    const getRoleListAction = async (params={}) => {
        const result = await getRoleList(params)
        if (result.status === 200) {
            // 更新角色列表数据
            roleList.value = result.data.results
            roleCount.value = result.data.count
        }
    }
    return { roleList,roleCount, getRoleListAction }
})
export default useRoleStore