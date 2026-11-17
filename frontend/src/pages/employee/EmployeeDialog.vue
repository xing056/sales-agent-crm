<template>
    <el-dialog @close="restHandler" :title="title" v-model="visible">
        <el-form label-width="80px" label-position="left" :rules="rules" ref="empForm" :model="formData">
            <el-form-item prop="department_id" label="选择部门">
                <el-tree-select :disabled="department_id > 0" check-strictly :props="{ value: 'id', label: 'name' }"
                    v-model="formData.department_id" :data="departmentList"></el-tree-select>
            </el-form-item>
            <el-form-item prop="position_id" label="选择职位">
                <el-select v-model="formData.position_id">
                    <el-option :label="item.name" :value="item.id" v-for="item in positionList"
                        :key="item.id"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="photo" label="照片">
                <el-upload ref="uploadRef" :on-change="photoChange" action="#" list-type="picture-card"
                    :auto-upload="false" :limit="1" :on-exceed="() => ElMessage.warning('此处只能选择一张照片')">
                    <el-icon>
                        <Plus />
                    </el-icon>
                </el-upload>
            </el-form-item>
            <el-form-item prop="name" label="姓名">
                <el-input @change="nameChange" v-model.trim="formData.name" placeholder="请输入员工姓名"></el-input>
            </el-form-item>
            <el-form-item prop="phone" label="联系电话">
                <el-input v-model.trim="formData.phone" placeholder="请输入联系电话"></el-input>
            </el-form-item>
            <el-form-item prop="email" label="电子邮箱">
                <el-input v-model.trim="formData.email" placeholder="请输入电子邮箱"></el-input>
            </el-form-item>
            <el-form-item label="性别" prop="gender">
                <el-radio-group v-model.trim="formData.gender">
                    <el-radio label="男" value="male"></el-radio>
                    <el-radio label="女" value="female"></el-radio>
                </el-radio-group>
            </el-form-item>
            <el-form-item prop="birthday" label="出生日期">
                {{ formData.birthday }}
                <el-date-picker value-format="YYYY-MM-DD" v-model.trim="formData.birthday" placeholder="请选择出生日期" />
            </el-form-item>
            <el-form-item label="学历" prop="education">
                <el-select v-model.trim="formData.education">
                    <el-option :label="item.label" :value="item.value" v-for="item in educationLevel"
                        :key="item.value"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item prop="school" label="毕业院校">
                <el-input v-model.trim="formData.school" placeholder="请输入毕业院校" />
            </el-form-item>
            <el-form-item prop="major" label="专业">
                <el-input v-model.trim="formData.major" placeholder="请输入专业" />
            </el-form-item>
            <el-form-item label="请选择地区" prop="region">
                <!-- 结合el-cascader组件 -->
                <el-cascader @change="regionChange" :options="pcaTextArr" v-model="formData.region"></el-cascader>
            </el-form-item>
            <el-form-item prop="address" label="详细地址">
                <el-input v-model.trim="formData.address" placeholder="请输入详细地址具体到门牌号"></el-input>
            </el-form-item>
            <el-form-item prop="isCreateUser" label="创建账号">
                <el-switch v-model="isCreateUser"></el-switch>
            </el-form-item>
            <template v-if="isCreateUser">
                <el-form-item prop="role_ids" label="角色">
                    <el-select multiple v-model="formData.role_ids">
                        <el-option v-for="item in roleList" :key="item.id" :value="item.id"
                            :label="item.name"></el-option>
                    </el-select>
                </el-form-item>
                <el-form-item prop="username" label="用户名">
                    <el-input v-model.trim="formData.username" placeholder="请输入用户名"></el-input>
                </el-form-item>
                <el-form-item prop="password" label="密码">
                    <el-input v-model.trim="formData.password" placeholder="请输入登录密码"></el-input>
                </el-form-item>
            </template>
        </el-form>
        <template #footer>
            <el-button @click="restHandler">取消</el-button>
            <el-button @click="submit" type="primary">确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { createUser, createEmployee } from '@/utils/api'
import useDepartmentStore from '@/stores/department';
import usePositionStore from '@/stores/position';
import useRoleStore from '@/stores/role';
import { storeToRefs } from 'pinia'
import { educationLevel } from '@/utils/config'
import { pcaTextArr } from 'element-china-area-data'
import { useDialog } from '@/utils/hooks'
import { useTemplateRef, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { Plus } from '@element-plus/icons-vue'
import { getSpell } from '@/utils/api'
import { inject } from 'vue'
// 获取祖先组件通过provide共享的数据
const department_id = inject('department_id', null)
console.log(department_id, 'department_id');
const uploadRef = useTemplateRef('uploadRef')
// 获取相关的数据仓库对象
const roleStore = useRoleStore()
const departmentStore = useDepartmentStore()
const positionStore = usePositionStore()
const { getDepartmentListAction } = departmentStore
const { getPositionListAction } = positionStore
const { getRoleListAction } = roleStore
const { departmentList } = storeToRefs(departmentStore)
const { positionList } = storeToRefs(positionStore)
const { roleList } = storeToRefs(roleStore)
// 请求部门数据和职位数据
getDepartmentListAction()
getPositionListAction()
getRoleListAction()

// 是否创建账号
const isCreateUser = ref(true)
const empForm = useTemplateRef('empForm')
const formInitData = {
    department_id, position_id: '',
    name: '', phone: '', email: '',
    photo: null, gender: '', birthday: '',
    provicne: '', city: '', county: '', address: '',
    education: '', school: '', major: '',
    // 保存cascader组件的选择结果
    region: [],
    username: '', password: '', role_ids: []
}
const { title, visible, formData, reset } = useDialog({ formInitData, title: '新增员工', formRef: empForm })
const rules = {
    department_id: [{ required: true, message: '请选择部门' }],
    position_id: [{ required: true, message: '请选择职位' }],
    photo: [{ required: true, message: '请选择照片' }],
    name: [{ required: true, message: '请输入员工姓名' }],
    gender: [{ required: true, message: '请输选择性别' }],
    phone: [{ required: true, message: '请输入联系电话' }],
    email: [{ required: true, message: '请输入电子邮箱' }],
    birthday: [{ required: true, message: '请选择出生日期' }],
    region: [{ required: true, message: '请选择籍贯' }],
    address: [{ required: true, message: '请输入详细地址' }],
    education: [{ required: true, message: '请选择学历' }],
    school: [{ required: true, message: '请输入毕业院校' }],
    major: [{ required: true, message: '请输入专业' }],
    username: [{ required: true, message: '请输入用户名' }],
    password: [{ required: true, message: '请输入登录密码' }],
    role_ids: [{ required: true, message: '请选择用户角色' }],
}
const regionChange = (region) => {
    const [province, city, county] = region
    formData.value.province = province
    formData.value.city = city
    formData.value.county = county
    console.log(province, city, county, 'province, city, county');

}
// file: 系统参数, 文件对象
const photoChange = (file) => {
    // console.log(file, 'file');
    // 获取原始图片对象更新到表单数据中
    formData.value.photo = file.raw
}

const nameChange = async () => {
    if (isCreateUser.value) {
        // 请求数据接口, 获取对应的汉语拼音
        const result = await getSpell(formData.value.name)
        if (result.status === 200) {
            formData.value.username = result.data.data.spell.join('')
        }
    }
}
const restHandler = () => {
    // 移除upload组件中之前选择的图片
    uploadRef.value.clearFiles()
    reset()
}
// 获取最新的员工列表: 通知父组件
const emit = defineEmits(['updateEmployee'])
const submit = () => {
    empForm.value.validate(async valid => {
        if (valid) {
            // 创建员工数据: 需要提交FormData, 因为表单数据中包含文件对象
            const empFormData = new FormData()
            if (isCreateUser.value) {
                // 创建账号数据
                const { username, password, role_ids } = formData.value
                const result = await createUser({ username, password, role_ids })
                if (result.status == 201) {
                    // 获取新增账号id
                    empFormData.append('user_id', result.data.id)
                }
            }
            for (let key in formData.value) {
                if (!['username', 'password', 'role_ids', 'region'].includes(key)) {
                    empFormData.append(key, formData.value[key])
                }
            }
            const result = await createEmployee(empFormData)
            if (result.status === 201) {
                ElMessage.success('操作成功')
                // 重置数据
                restHandler()
                emit("updateEmployee")
            }
        }
    })
}
defineExpose({
    visible
})
</script>

<style></style>