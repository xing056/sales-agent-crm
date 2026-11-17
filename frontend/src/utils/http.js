import axios from 'axios'
import { ElMessage } from 'element-plus';
import useUserStore from '@/stores/user';

// 创建axios实例
const instance = axios.create({
    // 后端数据接口的基础域名
    baseURL: '/api'
})
// 请求拦截器
instance.interceptors.request.use(request => {
    // 获取用户模块数据仓库对象
    const userStore = useUserStore()
    // 获取登录凭证accessToken
    const { accessToken } = userStore
    if (accessToken) {
        // 动态添加请求头Authorization
        request.headers.Authorization = `Bearer ${accessToken}`
    }
    return request
})
// 响应拦截器
// 约定：失败统一返回 false（而不是 reject）。页面里的写法都是
//     const result = await xxx()
//     if (result.status === 200) { ... }
// 返回 false 时 result.status 是 undefined，分支自然跳过，不会把
// "403 没有权限"这种正常业务分支变成未捕获的 Promise 异常。
instance.interceptors.response.use(response => {
    // 处理响应状态码为200的响应
    return response
}, error => {
    // 把后端各种形态的错误都收敛成一句人话
    //（之前直接读 error.response.data，断网时 error.response 是 undefined，会再抛一次异常）
    const response = error.response
    if (!response) {
        ElMessage.error('无法连接后端服务，请确认后端已启动')
        return false
    }
    const data = response.data
    let msg = ''
    if (typeof data === 'string') {
        // 500 时 Django 可能直接返回一整个 HTML 错误页，别把它塞进提示框
        msg = data.trimStart().startsWith('<') ? '' : data.slice(0, 200)
    } else if (data && typeof data === 'object') {
        if (data.message) {
            msg = data.message
        } else if (data.detail) {
            msg = typeof data.detail === 'string' ? data.detail : JSON.stringify(data.detail)
        } else {
            // DRF 字段级校验错误：{ field: ["错误1", "错误2"] }
            msg = Object.entries(data)
                .map(([key, val]) => `${key}: ${Array.isArray(val) ? val.join('，') : val}`)
                .join('；')
        }
    }
    const url = (error.config && error.config.url) || ''
    // 登录接口自己返回 401 是"账号密码错"，不是"会话过期"，
    // 不能在这里清状态 + 跳登录页，否则密码输错会变成一句"登录已失效"。
    const isLoginRequest = url.includes('/user/login/')
    if (response.status === 401 && !isLoginRequest) {
        // 令牌过期/无效：清掉本地状态回登录页，否则用户会一直点、一直 401
        ElMessage.warning(msg || '登录状态已失效，请重新登录')
        useUserStore().reset()
        if (window.location.pathname !== '/login') {
            window.location.href = '/login'
        }
        return false
    }
    if (response.status >= 500) {
        // 服务端异常：界面只给一句人话（带编号），原始响应丢进控制台留着排查
        console.error('[api] 服务端异常', url, response.status, data)
    }
    ElMessage.warning(msg || `请求失败（HTTP ${response.status}）`)
    return false
})

export default instance