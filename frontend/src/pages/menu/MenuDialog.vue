<template>
    <el-dialog @close="reset" :title="dialogTitle" v-model="visible">
        <el-form label-width="80px" label-position="right" :rules="rules" :model="formData" ref="menuForm">
            <el-form-item prop="parent" label="上级菜单">
                <el-tree-select clearable filterable check-strictly :props="{ value: 'id', label: 'title' }"
                    v-model="formData.parent" :data="menuList" />
            </el-form-item>
            <el-form-item prop="menu_type" label="菜单类型">
                <el-select v-model="formData.menu_type" placeholder="请选择菜单类型">
                    <el-option v-for="(item, key) in menuType" :key="key" :value="key" :label="item.value"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="title" label="菜单名称">
                <el-input v-model="formData.title" placeholder="请输入菜单名称"></el-input>
            </el-form-item>
            <el-form-item v-if="formData.menu_type !== 'dir'" prop="permission_id" label="菜单权限">
                <!-- check-strictly=true: 任意一个节点都可以被选择 -->
                <el-tree-select clearable filterable check-strictly :props="{ value: 'id', label: 'name' }"
                    v-model="formData.permission_id" :data="permList" :render-after-expand="false" />
            </el-form-item>
            <el-form-item v-if="formData.menu_type === 'dir'" prop="icon" label="菜单图标">
                <el-select v-model="formData.icon" placeholder="请选择菜单图标">
                    <el-option v-for="(item, key) in icons" :key="item" :value="key">
                        <el-icon :size="20">
                            <component :is="item" />
                        </el-icon>
                    </el-option>
                </el-select>
            </el-form-item>
            <el-form-item v-if="['nav', 'link'].includes(formData.menu_type)" prop="path" label="菜单地址">
                <el-input v-model="formData.path" placeholder="请输入菜单地址"></el-input>
            </el-form-item>
            <el-form-item prop="sort_order" label="菜单顺序">
                <el-input @input="sortOrderInput" v-model="formData.sort_order" placeholder="请输入菜单顺序"></el-input>
            </el-form-item>
            <el-form-item prop="status" label="菜单状态">
                <el-radio-group v-model="formData.status">
                    <el-radio :value="true" label="启用"></el-radio>
                    <el-radio :value="false" label="禁用"></el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button @click="submit" type="primary">确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { menuType, icons } from '../../utils/config'
import { storeToRefs } from 'pinia'
import { useTemplateRef } from 'vue';
import { useDialog } from '../../utils/hooks'
import useMenuStore from '@/stores/menu';
import usePermStore from '@/stores/perm';
import { createMenu, updateMenu } from '@/utils/api'
import { ElMessage } from 'element-plus';
// 获取权限模块数据仓库对象
const permStore = usePermStore()
// 权限列表数据
const { permList } = storeToRefs(permStore)
const { getPermListAction } = permStore
// 请求权限列表数据
getPermListAction()
// 获取菜单模块数据仓库对象
const menuStore = useMenuStore()
// 获取菜单列表
const { menuList } = storeToRefs(menuStore)
const { getMenuListAction } = menuStore
// 表单组件对象
const menuForm = useTemplateRef('menuForm')
// 表单初始数据
const formInitData = {
    parent: '',
    permission_id: '',
    title: '',
    path: '',
    icon: '',
    menu_type: '',
    status: '',
    sort_order: ''
}
const { pk, title: dialogTitle, visible, formData, reset } = useDialog({ formInitData, title: '新增菜单', formRef: menuForm })
const rules = {
    title: [{ required: true, message: '请输入菜单名称' }],
    menu_type: [{ required: true, message: '请选择菜单类型' }],
    icon: [{ required: true, message: '请选择菜单图标' }],
    path: [{ required: true, message: '请输入菜单地址' }],
    status: [{ required: true, message: '请选择菜单状态' }],
    permission_id: [{ required: true, message: '请选择菜单权限' }]
}
const submit = () => {
    menuForm.value.validate(async valid => {
        const menuData = { ...formData.value }
        // 获取上级菜单id
        if (!formData.value.parent) {
            delete menuData.parent
        }
        if (!menuData.permission_id) {
            delete menuData.permission_id
        }
        if (valid) {
            let result
            if (pk.value > 0) {
                // 更新
                result = await updateMenu(pk.value, menuData)
            } else {
                // 新增
                result = await createMenu(menuData)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                // 数据重置
                reset()
                // 请求最新的菜单数据
                getMenuListAction()
            }
        }
    })
}
const openUpdateForm = ({ id, title, menu_type, parent, permission_id, status, icon, path, sort_order }) => {
    pk.value = id
    dialogTitle.value = '更新菜单'
    visible.value = true
    console.log(title, menu_type, parent, permission_id, status, icon, path)
    formData.value = { title, menu_type, parent, permission_id, status, icon, path, sort_order }
}
const sortOrderInput = () => {
    const reg = /^\d{1,}$/
    if (!reg.test(formData.value.sort_order)) {
        formData.value.sort_order = ''
    }
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>