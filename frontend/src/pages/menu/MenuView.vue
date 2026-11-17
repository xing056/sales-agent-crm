<template>
  <el-card>
    <h3>菜单管理</h3>
    <div class="actions">
      <el-button @click="dialog.visible=true" v-if="hasPermission(['api:menu:create'])" type="primary" plain>新增菜单</el-button>
    </div>
    <el-divider></el-divider>
    <el-table  row-key="id" :data="menuList">
      <el-table-column label="序号" prop="id" min-width="60"></el-table-column>
      <el-table-column label="菜单标题" prop="title" min-width="100"></el-table-column>
      <el-table-column label="菜单图标" prop="icon" min-width="100">
        <template v-slot="props">
          <el-icon :size="20">
            <component :is="icons[props.row.icon]" />
          </el-icon>
        </template>
      </el-table-column>
      <el-table-column label="菜单地址" prop="path" min-width="100"></el-table-column>
      <el-table-column label="菜单类型" prop="menu_type" min-width="100">
        <template v-slot="props">
          <el-tag :type="menuType[props.row.menu_type].color">{{ menuType[props.row.menu_type].value }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="菜单排序" prop="sort_order" min-width="100"></el-table-column>
      <el-table-column label="菜单权限编码" prop="permission_code" min-width="100"></el-table-column>
      <el-table-column label="菜单状态" prop="status" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.status ? 'success' : 'danger'">{{ props.row.status ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column fixed="right" v-if="hasPermission(['api:menu:update', 'api:menu:destroy'])" label="操作"
        min-width="120">
        <template v-slot="props">
          <el-button @click="edit(props.row)" v-if="hasPermission(['api:menu:update'])" type="primary" size="small" plain>编辑</el-button>
          <el-button @click="del(props.row.id)" type="danger" v-if="hasPermission(['api:menu:destroy'])" size="small" plain>删除</el-button>
        </template>

      </el-table-column>
    </el-table>
  </el-card>
  <MenuDialog ref="dialog" />
</template>

<script setup>
import {icons} from '@/utils/config'
import MenuDialog from './MenuDialog.vue';
import { menuType } from '../../utils/config'
import { hasPermission, withConfirm } from '../../utils/util'
import useMenuStore from '@/stores/menu'
import { storeToRefs } from 'pinia'
import { useTemplateRef } from 'vue'
import { removeMenu } from '@/utils/api';
// 获取对话框组件对象
const dialog = useTemplateRef('dialog')
// 获取菜单模块数据仓库对象
const menuStore = useMenuStore()
// menuList: 菜单列表数据
const { menuList } = storeToRefs(menuStore)
const { getMenuListAction } = menuStore
// 请求菜单列表
getMenuListAction()
const edit=(row)=>{
  dialog.value.openUpdateForm(row)
}
const del=(id)=>{
  withConfirm(async()=>{
    // 删除菜单数据
    return await removeMenu(id)
  },()=>{
    // 更新菜单列表
    getMenuListAction()
  })
}
</script>

<style></style>