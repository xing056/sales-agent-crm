import { ElMessage, ElMessageBox } from 'element-plus';
// 自定义函数实现安全权限控制
import useUserStore from '../stores/user'
import { storeToRefs } from 'pinia'
// codes: 权限编码,['']
export function hasPermission(codes) {
  if (!Array.isArray(codes)) {
    return false
  }
  // 获取权限模块数据仓库对象
  const userStore = useUserStore()
  // 获取当前角色对象
  const { currRole } = storeToRefs(userStore)
  return codes.some(item => currRole.value.btn_menu.includes(item))
}
// 删除功能封装函数
// task: 主任务函数
// callback: 主任务函数执行成功之后的回调函数
export function withConfirm(task, callback) {
  ElMessageBox.confirm('确认当前操作?', '提示').then(async () => {
    // 请求删除数据接口
    const result = await task()
    if ([200, 201, 204].includes(result.status) || result === true) {
      ElMessage.success('操作成功')
      // 调用回调函数
      callback && callback()
    }
  }).catch(() => { })
}  