<template>
  <el-card>
    <h3>用户管理</h3>
    <div class="actions">
      <el-button @click="dialog.visible = true" v-if="hasPermission(['api:user:create'])" type="primary"
        plain>新增用户</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="userList">
      <el-table-column label="序号" prop="id" min-width="60"></el-table-column>
      <el-table-column label="角色" prop="role" min-width="100">
        <template v-slot="props">
          <el-space wrap><el-tag v-for="item in props.row.role" :key="item">{{ item.name }}</el-tag></el-space>
        </template>
      </el-table-column>
      <el-table-column label="用户名" prop="username" min-width="80"></el-table-column>
      <el-table-column label="手机" prop="phone" min-width="120"></el-table-column>
      <el-table-column label="邮箱" prop="email" min-width="120"></el-table-column>
      <el-table-column label="状态" prop="status" min-width="80">
        <template v-slot="props">
          <el-tag :type="props.row.status ? 'success' : 'danger'">{{ props.row.status ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="超级用户" prop="is_superuser" min-width="100">
        <template v-slot="props">
          <el-tag :type="props.row.is_superuser ? 'success' : 'danger'">{{ props.row.is_superuser ? '是' : '否'
          }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="创建时间" prop="create_time" min-width="120"></el-table-column>
      <el-table-column fixed="right" label="操作" v-if="hasPermission(['api:user:update', 'api:user:destroy'])"
        min-width="120">
        <template v-slot="props">
          <el-button @click="edit(props.row)" type="primary" v-if="hasPermission(['api:user:update'])" size="small"
            plain>编辑</el-button>
          <el-button @click="del(props.row.id)" type="danger" v-if="hasPermission(['api:user:destroy'])" size="small"
            plain>删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <br>
    <el-pagination @current-change="pageChange" background :total="userCount" :page-size="size"
      layout="total,prev,pager,next,jumper"></el-pagination>
  </el-card>
  <UserDialog ref="dialog" @updateUser="updateUser" />

</template>

<script setup>
import UserDialog from './UserDialog.vue';
import { hasPermission, withConfirm } from '../../utils/util'
import { useTemplateRef, ref, computed } from 'vue';
import { storeToRefs } from 'pinia'
import useUserStore from '@/stores/user';
import { removeUser } from '@/utils/api';
// 获取用户模块数据仓库对象
const userStore = useUserStore()
const { userCount, userList } = storeToRefs(userStore)
const { getUserListAction } = userStore

const page = ref(1)
const size = ref(10)
// 获取对话框组件对象
const dialog = useTemplateRef('dialog')
const edit = (row) => {
  dialog.value.openUpdateForm(row)
}
const pageChange = (num) => {
  // 更新页码
  page.value = num
  // 获取下一页数据
  getUserListAction({ page: page.value })
}
// 请求用户列表数据
getUserListAction({ page: page.value })
const del = (id) => {
  withConfirm(async () => {
    // 删除用户
    return removeUser(id)
  }, () => {
    if (userList.value.length === 1) {
      if (page.value > 1) {
        page.value -= 1
      }
    }
    // 更新用户列表
    getUserListAction({ page: page.value })
  })
}
// 自定义事件updateUser的处理函数
const updateUser = () => {
  getUserListAction({ page: page.value })
}
</script>

<style></style>