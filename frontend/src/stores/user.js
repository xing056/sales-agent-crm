import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import { login, getUserList } from '../utils/api'
const useUserStore = defineStore('user', () => {
    // 用户列表
    const userList = ref([])
    // 用户总数
    const userCount = ref(0)
    // 登录数据
    const loginInfo = ref({})
    // 员工信息
    const empInfo = ref({})
    // 登录凭证
    const accessToken = ref('')
    // refreshToken
    const refreshToken = ref('')
    // 当前默认角色序号(角色数组的下标)
    const currRoleIndex = ref(0)
    const currRole = computed(() => {
        return loginInfo.value.role ? loginInfo.value.role[currRoleIndex.value] : {}
    })
    // 切换角色的方法
    const toggleRole = (index) => {
        currRoleIndex.value = index
    }
    // 登录方法
    // payload={username,password}
    const loginAction = async (payload) => {
        const result = await login(payload)
        if (result.status === 200) {
            // 更新数据
            loginInfo.value = result.data.data
            // 判断employee是否存在
            if (result.data.employee) {
                empInfo.value = result.data.employee
            }
            accessToken.value = result.data.access_token
            refreshToken.value = result.data.refresh_token
            return true
        }
        return false
    }
    // 请求用户列表数据
    // params={page:'页码'}
    const getUserListAction = async (params) => {
        const result = await getUserList(params)
        if (result.status === 200) {
            userList.value = result.data.results
            userCount.value = result.data.count
        }
    }
    // 重置数据仓库中的数据
    const reset = () => {
        loginInfo.value = {}
        empInfo.value = {}
        currRoleIndex.value = 0
        accessToken.value = ''
        refreshToken.value = ''
    }

    // pinia-plugin-persistedstate数据持久化插件只会对此处返回的数据进行持久化
    return { reset,getUserListAction, userCount, userList, loginInfo, empInfo, accessToken, refreshToken, loginAction, toggleRole, currRole, currRoleIndex }
}, {
    // 开启数据持久化功能
    persist: true
})
export default useUserStore