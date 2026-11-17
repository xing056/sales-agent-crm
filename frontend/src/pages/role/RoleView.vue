<template>
  <el-card>
    <h3>角色管理</h3>
    <div class="actions">
      <el-button @click="dialog.visible = true" type="primary" plain
        v-if="hasPermission(['api:role:create'])">新增角色</el-button>
    </div>
    <el-divider></el-divider>
    <el-table row-key="id" :data="roleList">
      <el-table-column label="序号" prop="id" min-width="60"></el-table-column>
      <el-table-column label="角色名称" prop="name" min-width="100"></el-table-column>
      <el-table-column label="角色状态" prop="status" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.status ? 'success' : 'danger'">{{ props.row.status ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="角色说明" prop="remark" min-width="100"></el-table-column>
      <el-table-column label="操作" v-if="hasPermission(['api:role:update', 'api:role:destroy'])">
        <template v-slot="props">
          <el-button @click="edit(props.row)" type="primary" size="small" plain
            v-if="hasPermission(['api:role:update'])">编辑</el-button>
          <el-button @click="del(props.row.id)" type="danger" size="small" plain
            v-if="hasPermission(['api:role:destroy'])">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <el-pagination @current-change="pagChange" background :page-size="size" :total="roleCount"
      layout="total,prev,pager,next,jumper"></el-pagination>
  </el-card>
  <RoleDialog ref="dialog" @update-role="updateRole" />
</template>

<script setup>
import RoleDialog from './RoleDialog.vue'
import { ref, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
import useRoleStore from '@/stores/role'
import { hasPermission, withConfirm } from '@/utils/util'
import { removeRole } from '@/utils/api'
const dialog = useTemplateRef('dialog')
// 获取角色模块数据仓库对象
const roleStore = useRoleStore()
const { roleList, roleCount } = storeToRefs(roleStore)
const { getRoleListAction } = roleStore
// 页码
const page = ref(1)
const size = ref(10)
// 请求角色列表数据
getRoleListAction({ page: page.value })
// num: 被点击的页码按钮的数值
const pagChange = (num) => {
  // 更新页码
  page.value = num
  // 重新请求分页数据
  getRoleListAction({ page: page.value })
}
// 自定义事件updateRole的处理函数
const updateRole = () => {
  getRoleListAction({ page: page.value })
}
const edit = (row) => {
  console.log(row, 'row');
  dialog.value.openUpdateForm(row)
}
const del = (id) => {
  withConfirm(async () => {
    // 删除角色
    return await removeRole(id)
  }, () => {
    // 更新角色列表
    // 如果当前在最后一页, 并且最后一页只有一条数据, 那么就应该请求上一页数据
    // const maxPage=Math.ceil(roleCount.value/size.value)
    // if(maxPage===page.value&&roleCount.value%size.value===1){
    //   if(page.value){
    //     page.value-=1
    //   } 
    // }
    if (roleList.value.length === 1) {
      if (page.value > 1) {
        page.value -= 1
      }
    }
    getRoleListAction({ page: page.value })
  })
}
</script>

<style></style>