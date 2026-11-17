<template>
    <div class="actions">
        <el-button v-if="hasPermission(['api:employee:download'])" type="primary" @click="download" plain>导出员工数据</el-button>
        <el-button v-if="hasPermission(['api:employee:create'])" type="primary" @click="dialog.visible = true" plain>新增员工</el-button>
    </div>
    <el-divider></el-divider>
    <el-table :data="employeeList">
        <el-table-column prop="id" label="序号" min-width="80"></el-table-column>
        <el-table-column prop="department.name" label="部门" min-width="100"></el-table-column>
        <el-table-column prop="position.name" label="职位" min-width="100"></el-table-column>
        <el-table-column prop="is_manager" label="是否为主管" min-width="100">
            <template v-slot="props">
                <el-tag :type="props.row.is_manager ? 'primary' : 'info'">{{ props.row.is_manager ? '是' : '否'
                    }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="work_no" label="工号" min-width="100"></el-table-column>
        <el-table-column prop="name" label="姓名" min-width="100"></el-table-column>
        <el-table-column prop="gender" label="性别" min-width="100">
            <template v-slot="props">
                <el-tag>{{ props.row.gender === 'male' ? '男' : '女' }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="birthday" label="出生年月日" min-width="100"></el-table-column>
        <el-table-column prop="phone" label="手机号" min-width="100"></el-table-column>
        <el-table-column prop="email" label="邮箱" min-width="100"></el-table-column>
        <el-table-column prop="education" label="学历" min-width="100">
            <!-- 1 高中及以下 2-专科 3-本科 4-硕士 5-博士 -->
            <template v-slot="props">
                <el-tag :type="props.row.education ? educationLevel[props.row.education].color : 'info'">
                    {{ props.row.education ? educationLevel[props.row.education].label : '暂无' }}</el-tag>
            </template>
        </el-table-column>
        <el-table-column prop="school" label="毕业院校" min-width="100"></el-table-column>
        <el-table-column prop="major" label="专业" min-width="100"></el-table-column>
        <el-table-column prop="create_time" label="入职时间" min-width="100"></el-table-column>
        <el-table-column  v-if="hasPermission(['api:employee:detail','api:employee:destroy'])"  label="操作" fixed="right" min-width="140">
            <template v-slot="props">
                <el-button v-if="hasPermission(['api:employee:detail'])"  @click="$router.push({ name: 'empDetail', params: { id: props.row.id } })" size="small"
                    type="primary">详情</el-button>
                <el-button v-if="hasPermission(['api:employee:destroy'])"  @click="del(props.row.id)" size="small" type="danger">删除</el-button>
            </template>
        </el-table-column>
    </el-table>
    <br>
    <el-pagination :total="employeeCount" layout="total,prev,pager,next,jumper" background :page-size="size"
        @current-change="pageChange"></el-pagination>
    <EmployeeDialog @updateEmployee="updateEmployee" ref="dialog" />
</template>

<script setup>
import { hasPermission } from '@/utils/util'
import EmployeeDialog from '@/pages/employee/EmployeeDialog.vue'
import { educationLevel } from '@/utils/config'
import { ref, useTemplateRef } from 'vue'
import { storeToRefs } from 'pinia'
const dialog = useTemplateRef('dialog')
import useEmployeeStore from '@/stores/employee'
import { withConfirm } from '@/utils/util'
import { removeEmployee, downloadEmployee } from '@/utils/api'
import { saveAs } from 'file-saver'

// 接收父组件传递的部门id
const { department_id } = defineProps({
    department_id: {
        type: Number,
        default: null
    }
})

const employeeStore = useEmployeeStore()
const { getEmployeeListAction } = employeeStore
const { employeeList, employeeCount } = storeToRefs(employeeStore)
const page = ref(1)
const size = ref(2)
const query = { page: page.value, size: size.value }
if (department_id) {
    query.department_id = department_id
}
// 请求员工相关数据
getEmployeeListAction(query)
const pageChange = (num) => {
    // 更新页码
    query.page = page.value = num
    // 请求最新的数据
    getEmployeeListAction(query)
}
// 自定义事件处理函数
const updateEmployee = () => {
    // 请求最新的数据
    getEmployeeListAction(query)
}
const del = (id) => {
    withConfirm(async () => {
        // 删除员工信息
        return await removeEmployee(id)
    }, () => {
        // 更新员工列表
        getEmployeeListAction(query)
    })
}
// import { downloadEmployee } from '@/utils/api'
// 导出员工数据
const download = async () => {
    const params = { ...query }
    delete params.page
    delete params.size
    // 优点: 可以携带登录凭证
    // 缺点: 如果下载文件体积较大, 会比较消耗性能
    const result = await downloadEmployee(params)
    if (result.status === 200) {
        // saveAs(blob对象,'文件名')
        // saveAs(new Blob([result.data]), '员工信息.xlsx')
        saveAs(result.data, '员工信息.xlsx')
    }
    // 直接跳转到接口地址, 触发浏览器默认的下载行为
    // 优点: 文件直接通过浏览器写入了磁盘(硬盘), 没有经过前端js代码的处理
    // 缺点: 无法携带登录凭证
    // window.open('/api/employee/download/')
}
</script>

<style></style>