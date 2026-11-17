// 自定义组合函数
import { ref } from 'vue'
// options={formInitData}
export function useDialog(options = {}) {
    const title = ref(options.title || '新增')
    // 待编辑数据的唯一标识
    const pk = ref('')
    // 控制对话框显示状态
    const visible = ref(false)
    // 表单数据
    const formData = ref({ ...options.formInitData } || {})
    // 重置方法
    const reset = () => {
        pk.value=''
        // 重置对话框标题
        title.value = options.title || '新增'
        // 重置表单
        formData.value = { ...options.formInitData } || {}
        // 移除表单组件的验证信息
        options.formRef.value.resetFields()
        // 关闭对话框
        visible.value = false
    }
    return {
        title, pk, visible, formData, reset
    }
}

export function usePager(){
    const page=ref(1)
    const size=ref(10)
    return {page,size}
}