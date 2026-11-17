<template>
    <el-form ref="empForm" :rules="rules" :model="empInfo">
        <el-descriptions title="员工资料" border>
            <el-descriptions-item :rowspan="2" :width="140" label="员工照片" align="center">
                <el-form-item prop="photo" v-if="isEdit">
                    <el-upload :file-list="photoList" :on-change="photoChange"
                        :on-exceed="() => ElMessage.warning('此处只能选择一张照片')" :limit="1" list-type="picture-card"
                        action="#" :auto-upload="false" show-file-list>
                        <el-icon>
                            <Plus />
                        </el-icon>
                    </el-upload>
                </el-form-item>
                <el-image v-else style="width: 100px; height: 100px" :src="empInfo.photo" />
            </el-descriptions-item>
            <el-descriptions-item label="工号">{{ empInfo.work_no }}</el-descriptions-item>
            <el-descriptions-item label="是否为主管">
                <el-tag :type="empInfo.is_manager ? 'primary' : 'info'">
                    {{ empInfo.is_manager ? '是' : '否' }}
                </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="部门">
                <el-form-item prop="department_id" v-if="isEdit">
                    <!-- 部门列表 -->
                    <el-tree-select v-model="empInfo.department_id" check-strictly :data="departmentList"
                        :props="{ value: 'id', label: 'name' }"></el-tree-select>
                </el-form-item>
                <span v-else>
                    {{ empInfo.department?.name }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="职位">
                <el-form-item prop="position_id" v-if="isEdit">
                    <!-- 职务列表 -->
                    <el-tree-select v-model="empInfo.position_id" :data="positionList"
                        :props="{ value: 'id', label: 'name' }"></el-tree-select>
                </el-form-item>
                <span v-else>
                    {{ empInfo.position?.name }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="姓名">
                <el-form-item prop="name" v-if="isEdit">
                    <el-input v-model="empInfo.name" placeholder="请输入姓名"></el-input>
                </el-form-item>
                <span v-else>
                    {{ empInfo.name }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="性别">
                <el-form-item prop="gender" v-if="isEdit">
                    <el-radio-group v-model="empInfo.gender">
                        <el-radio value="male" label="男"></el-radio>
                        <el-radio value="female" label="女"></el-radio>
                    </el-radio-group>
                </el-form-item>
                <span v-else>
                    {{ empInfo.gender === 'male' ? '男' : '女' }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="出生日期">
                <el-form-item prop="birthday" v-if="isEdit">
                    <el-date-picker v-model="empInfo.birthday" value-format="YYYY-MM-DD"></el-date-picker>
                </el-form-item>
                <span v-else>{{ empInfo.birthday }}</span>
            </el-descriptions-item>
            <el-descriptions-item label="联系电话">
                <el-form-item prop="phone" v-if="isEdit">
                    <el-input :maxlength="11" v-model="empInfo.phone" type="tel" placeholder="请输入联系电话"></el-input>
                </el-form-item>
                <span v-else>
                    {{ empInfo.phone }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="电子邮箱">
                <el-form-item prop="email" v-if="isEdit">
                    <el-input v-model="empInfo.email" type="email" placeholder="请输入电子邮箱"></el-input>
                </el-form-item>
                <span v-else>
                    {{ empInfo.email }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="学历">
                <el-form-item prop="education" v-if="isEdit">
                    <el-select v-model="empInfo.education" placeholder="请选择学历">
                        <el-option v-for="item in educationLevel" :key="item.value" :label="item.label"
                            :value="item.value"></el-option>
                    </el-select>
                </el-form-item>
                <span v-else>
                    <el-tag size="small">{{ empInfo.education && educationLevel[empInfo.education].label }}</el-tag>
                </span>

            </el-descriptions-item>
            <el-descriptions-item label="毕业院校">
                <el-form-item prop="school" v-if="isEdit">
                    <el-input v-model="empInfo.school" placeholder="请输入毕业院校"></el-input>
                </el-form-item>
                <span v-else>
                    {{ empInfo.school }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="专业">
                <el-form-item prop="major" v-if="isEdit">
                    <el-input v-model="empInfo.major" placeholder="请输入专业"></el-input>
                </el-form-item>
                <span v-else>
                    {{ empInfo.major }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="籍贯">
                <el-form-item prop="region" v-if="isEdit">
                    <el-cascader v-model="empInfo.region" :options="pcaTextArr">
                    </el-cascader>
                </el-form-item>
                <span v-else>
                    {{ empInfo.province }}-{{ empInfo.city }}-{{ empInfo.county }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="详细通信地址">
                <el-form-item prop="adddress" v-if="isEdit">
                    <el-input v-model="empInfo.address" placeholder="请输入专业"></el-input>
                </el-form-item>
                <span v-else>
                    {{ empInfo.address }}
                </span>
            </el-descriptions-item>
            <el-descriptions-item label="入职日期">
                {{ empInfo.create_time }}
            </el-descriptions-item>
            <el-descriptions-item label="资料更新日期">
                {{ empInfo.update_time }}
            </el-descriptions-item>
            <el-descriptions-item label="操作">
                <template v-if="isEdit">
                    <el-button @click="submit" type="primary" plain>
                        保存
                    </el-button>
                    <el-button @click="isEdit = false" type="info" plain>
                        取消
                    </el-button>
                </template>
                <el-button v-else @click="isEdit = true" type="primary">
                    编辑
                </el-button>

            </el-descriptions-item>
        </el-descriptions>
    </el-form>
</template>

<script setup>
import { pcaTextArr } from 'element-china-area-data'
import useDepartmentStore from '@/stores/department'
import usePositionStore from '@/stores/position'
import { storeToRefs } from 'pinia'
import { Plus } from '@element-plus/icons-vue'
import { educationLevel } from '@/utils/config'
import { getEmployee, updateEmployee } from '@/utils/api'
import { onMounted, ref, useTemplateRef } from 'vue'
import { ElMessage } from 'element-plus'
// 获取父组件传递的员工id
const { empId } = defineProps(['empId'])
const departmentStore = useDepartmentStore()
const positionStore = usePositionStore()
const { departmentList } = storeToRefs(departmentStore)
const { positionList } = storeToRefs(positionStore)
const { getDepartmentListAction } = departmentStore
const { getPositionListAction } = positionStore
getDepartmentListAction()
getPositionListAction()
const empForm = useTemplateRef('empForm')
const isEdit = ref(false)
// 请求员工详情数据
const empInfo = ref({})
const photoList = ref([])
onMounted(async () => {
    // 根据父组件传递的员工id获取员工资料
    const result = await getEmployee(empId)
    if (result.status === 200) {
        empInfo.value = result.data
        // 职位id
        empInfo.value.position_id = result.data.position?.id
        // 部门id
        empInfo.value.department_id = result.data.department?.id
        photoList.value = [{ url: result.data.photo }]
        // 省市区数据
        const { province, city, county } = result.data
        empInfo.value.region = [province, city, county]
    }
})
const photoChange = (file) => {
    empInfo.value.photo = file.raw
}
const rules = {
    name: [{ required: true, message: '请输入员工姓名' }],
    gender: [{ required: true, message: '请选择员工性别' }],
    phone: [{ pattern: /^1[3456789]\d{9}$/, required: true, message: '请输入合法手机号码' }],
    email: [{ type: 'email', required: true, message: '请输入合法电子邮箱' }],
    photo: [{ required: true, message: '请输选择照片' }],
    education: [{ required: true, message: '请输入学历' }],
    shcool: [{ required: true, message: '请输入学校' }],
    major: [{ required: true, message: '请输入专业' }],
    province: [{ required: true, message: '请输入省份' }],
    city: [{ required: true, message: '请选择城市' }],
    county: [{ required: true, message: '请选择区县' }],
    address: [{ required: true, message: '请输入详细通信地址' }],
    position_id: [{ required: true, message: '请选择员工职位' }],
    department_id: [{ required: true, message: '请选址员工部门' }],
    birtday: [{ required: true, message: '请选择员工出生日期' }],

}
const submit = () => {
    empForm.value.validate(async valid => {
        if (valid) {
            // empInfo.value => FormData
            const empFormData = new FormData()
            for (let key in empInfo.value) {
                if (!['id', 'user', 'work_no', 'region', 'department', 'position', 'create_time', 'update_time'].includes(key)) {
                    empFormData.append(key, empInfo.value[key])
                }
            }
            if (typeof empFormData.get('photo') === 'string') {
                empFormData.delete('photo')
            }
            const result = await updateEmployee(empInfo.value.id, empFormData)
            if (result.status === 200) {
                ElMessage.success('操作成功')
                isEdit.value = false
                // 更新empInfo
                empInfo.value = result.data
                const { province, city, county } = result.data
                empInfo.value.region = [province, city, county]
                empInfo.value.position_id = result.data.position.id
                empInfo.value.department_id = result.data.department.id
                empInfo.value.photo = result.data.photo
            }
        }
    })
}
</script>

<style></style>