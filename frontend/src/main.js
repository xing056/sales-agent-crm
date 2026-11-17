import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
// 导入公共样式文件
import './assets/css/common.css'
// Element Plus 官方暗色变量表：给 <html> 加 class="dark" 即可全局生效
import 'element-plus/theme-chalk/dark/css-vars.css'
// 项目里写死颜色的暗色补充
import './assets/css/theme-dark.css'
// 手动导入ElMessage,ElMessageBox组件的样式文件
import 'element-plus/es/components/message/style/css'
import 'element-plus/es/components/message-box/style/css'
import 'element-plus/es/components/notification/style/css'
import App from './App.vue'
import router from './router'
// 导入自定义指令
import {hasPermission} from './utils/directives'
// 主题：在挂载前应用，避免首屏闪白
import { initTheme } from './utils/theme'

initTheme()

const app = createApp(App)
// 创建pinia实例对象
const pinia=createPinia()
// 注册pinia数据持久化插件
pinia.use(piniaPluginPersistedstate)
// 注册pinia
app.use(pinia)
app.use(router)

// 注册自定义指令
app.directive('hasPermission',hasPermission)

app.mount('#app')
