<template>
  <el-card>
    <h3>权限管理</h3>
    <div class="actions">
      <!-- 调用自定义指令 -->
      <!-- <el-button v-has-permission="'api:permission:create'" type="primary" plain
        @click="dialog.visible = true">新增权限</el-button> -->
      <el-button v-if="hasPermission(['api:permission:create'])" type="primary" plain
        @click="dialog.visible = true">新增权限</el-button>
    </div>
    <el-divider></el-divider>
    <el-table row-key="id" :data="permList">
      <el-table-column label="序号" prop="id" min-width="60"></el-table-column>
      <el-table-column label="权限名称" prop="name" min-width="100"></el-table-column>
      <el-table-column label="权限编码" prop="code" min-width="100"></el-table-column>
      <el-table-column label="权限状态" prop="status" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.status ? 'success' : 'danger'">{{ props.row.status ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="是否公开" prop="is_public" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.is_public ? 'success' : 'danger'">{{ props.row.is_public ? '是' : '否' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column v-if="hasPermission(['api:permission:update', 'api:permission:destroy'])" label="操作"
        min-width="120">
        <template v-slot="props">
          <!-- <el-button v-has-permission="'api:permission:update'" type="primary" size="small" plain>编辑</el-button>
        <el-button type="danger" v-has-permission="'api:permission:destroy'" size="small" plain>删除</el-button> -->
          <el-button @click="edit(props.row)" v-if="hasPermission(['api:permission:update'])" type="primary"
            size="small" plain>编辑</el-button>
          <el-button @click="del(props.row.id)" type="danger" v-if="hasPermission(['api:permission:destroy'])"
            size="small" plain>删除</el-button>
        </template>

      </el-table-column>
    </el-table>
  </el-card>
  <!-- 调用对话框组件 -->
  <PermDialog ref="dialog" />
</template>

<script setup>
import { useTemplateRef } from 'vue'
import PermDialog from './PermDialog.vue';
import { storeToRefs } from 'pinia';
import usePermStore from '../../stores/perm'
import { hasPermission, withConfirm } from '../../utils/util'
import { removePerm } from '../../utils/api'

// 获取对话框组件对象
const dialog = useTemplateRef('dialog')
// 获取数据仓库对象
const permStore = usePermStore()
const { permList } = storeToRefs(permStore)
const { getPermListAction } = permStore
// 获取权限列表数据
getPermListAction()
// id:待删除的数据id
const del = (id) => {
  withConfirm(async () => {
    // 删除权限数据
    return await removePerm(id)
  }, () => {
    // 请求最新的权限列表
    getPermListAction()
  })
}
const edit = (row) => {
  console.log(row,'row');
  
  dialog.value.openUpdateForm(row)
}
</script>

<style></style>