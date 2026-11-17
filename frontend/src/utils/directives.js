import useUserStore from "@/stores/user"
import { storeToRefs } from 'pinia'
import { watch } from 'vue'
// 自定义指令
export const hasPermission = {
    // 当指令所在的元素初次挂在的时候, 自动执行
    // el: 指令所在元素(组件)对象
    // binding: 当前指令相关信息, 比如指令的属性值
    mounted(el, binding) {
        // 获取用户模块数据仓库
        const userStore = useUserStore()
        // 获取当前角色
        const { currRole } = storeToRefs(userStore)
        // 获取当前角色的按钮权限数据
        // 侦听当前角色对象
        watch(currRole, () => {
            if (!currRole.value.btn_menu.includes(binding.value)) {
                // 隐藏当前按钮
                el.style.display = 'none'
                // el.remove()
            } else {
                // 显示按钮
                el.style.display = 'inline-block'
                // console.log(el.parentNode, 'el');
            }
        }, { immediate: true })
    }
}
// 注册 app.directive('hasPermission',指令对象)
// 调用  <el-button v-has-permission="api:permission:create"></el-button>