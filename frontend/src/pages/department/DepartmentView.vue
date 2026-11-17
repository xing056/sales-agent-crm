<template>
  <el-card>
    <h3>部门管理</h3>
    <div class="actions">
      <el-button v-if="hasPermission(['api:department:create'])" type="primary" @click="dialog.visible = true"
        plain>新增部门</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="departmentList" row-key="id">
      <el-table-column prop="id" min-width="60" label="序号"></el-table-column>
      <el-table-column prop="name" min-width="100" label="部门名称"></el-table-column>
      <el-table-column align="center" prop="manager.name" min-width="100" label="部门主管">
        <template v-slot="props">
          <template v-if="props.row.manager">
            【{{ props.row.manager?.work_no }}】{{ props.row.manager?.name }}
            <el-link underline="hover" v-if="hasPermission(['api:employee:detail'])" type="primary" plain size="small"
              @click="$router.push({ name: 'empDetail', params: { id: props.row.manager?.id } })">查看</el-link>
          </template>
          <template v-else>暂无主管</template>
        </template>
      </el-table-column>
      <el-table-column prop="description" min-width="100" label="部门介绍"></el-table-column>
      <el-table-column prop="status" min-width="100" label="部门状态">
        <template v-slot="props">
          <el-tag v-if="props.row.status" type="primary" size="small" plain>正常</el-tag>
          <el-tag v-else type="danger" size="small" plain>禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="create_time" min-width="100" label="创建时间"></el-table-column>
      <el-table-column min-width="100" fixed="right" label="操作">
        <template v-slot="props">
          <el-space wrap>
            <el-button @click="$router.push({ name: 'departmentEmp', params: { id: props.row.id } })" type="primary"
              size="small" plain>部门员工</el-button>
            <el-button v-if="hasPermission(['api:department:update'])" @click="edit(props.row)" type="primary"
              size="small" plain>编辑</el-button>
            <el-button v-if="hasPermission(['api:department:destroy'])" @click="del(props.row.id)" type="danger"
              size="small" plain>删除</el-button>
          </el-space>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
  <DepartmentDialog ref="dialog" />
</template>

<script setup>
import { hasPermission } from '@/utils/util'
import { removeDepartment } from '@/utils/api'
import DepartmentDialog from './DepartmentDialog.vue'
import useDepartmentStore from '@/stores/department'
import { withConfirm } from '@/utils/util'
import { storeToRefs } from 'pinia'
import { useTemplateRef } from 'vue'
const departmentStore = useDepartmentStore()
const { getDepartmentListAction } = departmentStore
const { departmentList } = storeToRefs(departmentStore)
const dialog = useTemplateRef('dialog')
// 请求部门列表数据
getDepartmentListAction()
const edit = ({ id, name, parent, description, status }) => {
  dialog.value.openUpdateForm({ id, name, parent, description, status })
}
const del = (id) => {
  withConfirm(async () => {
    // 删除部门数据
    return await removeDepartment(id)
  }, () => {
    // 更新部门列表
    getDepartmentListAction()
  })
}
</script>

<style></style>