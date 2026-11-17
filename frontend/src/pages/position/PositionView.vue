<template>
  <el-card>
    <h3>职位管理</h3>
    <div class="actions">
      <el-button v-if="hasPermission(['api:position:create'])" type="primary" @click="dialog.visible = true"
        plain>新增职位</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="positionList" row-key="id">
      <el-table-column prop="id" min-width="100" label="职位序号"></el-table-column>
      <el-table-column prop="name" min-width="100" label="职位名称"></el-table-column>
      <el-table-column prop="level" min-width="100" label="职位等级"></el-table-column>
      <el-table-column prop="status" min-width="100" label="职位状态">
        <template v-slot="props">
          <el-tag v-if="props.row.status" type="primary" size="small" plain>正常</el-tag>
          <el-tag v-else type="danger" size="small" plain>禁用</el-tag>
        </template>
      </el-table-column>
      <el-table-column v-if="hasPermission(['api:position:update','api:position:destroy'])" min-width="100" label="操作">
        <template v-slot="props">
          <el-button v-if="hasPermission(['api:position:update'])" @click="edit(props.row)" type="primary" size="small"
            plain>编辑</el-button>
          <el-button v-if="hasPermission(['api:position:destroy'])" @click="del(props.row.id)" type="danger" size="small"
            plain>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
  </el-card>
  <br>
  <el-pagination @current-change="pageChange" :total="positionCount" layout="total,prev,pager,next,jumper" background
    :page-size="size"></el-pagination>
  <PositionDialog ref="dialog" @updatePos="updatePos" />
</template>

<script setup>
import { removePosition } from '@/utils/api'
import PositionDialog from './PositionDialog.vue'
import usePositionStore from '@/stores/position'
import { withConfirm, hasPermission } from '@/utils/util'
import { storeToRefs } from 'pinia'
import { useTemplateRef, ref } from 'vue'
const positionStore = usePositionStore()
const { getPositionListAction } = positionStore
const { positionList, positionCount } = storeToRefs(positionStore)
const dialog = useTemplateRef('dialog')
const page = ref(1)
const size = ref(10)
// 请求职位列表数据
getPositionListAction({ page: page.value })
const edit = ({ id, name, level, status }) => {
  dialog.value.openUpdateForm({ id, name, level, status })
}
const del = (id) => {
  withConfirm(async () => {
    // 删除职位数据
    return await removePosition(id)
  }, () => {
    // 更新职位列表
    getPositionListAction({ page: page.value })
  })
}

// num: 点击分页按钮的页码
const pageChange = (num) => {
  // 更新页码
  page.value = num
  // 重新请求数据
  getPositionListAction({ page: page.value })
}
// 自定义事件updatePos处理函数
const updatePos = () => {
  getPositionListAction({ page: page.value })
}
</script>

<style></style>