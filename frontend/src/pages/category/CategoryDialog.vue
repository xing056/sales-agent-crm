<template>
    <el-dialog @close="reset" :title="title" v-model="visible">
        <el-form :model="formData" label-width="80px" label-position="right" :rules="rules" ref="categoryForm">
            <el-form-item prop="parent" label="上级分类">
                <el-tree-select v-model="formData.parent" :props="{ value: 'id', label: 'name' }"
                    :data="categoryList"></el-tree-select>
            </el-form-item>
            <el-form-item label="分类名称" prop="name">
                <el-input v-model.trim="formData.name" placeholder="请输入分类名称"></el-input>
            </el-form-item>
            <el-form-item label="分类图片" prop="cover">
                <el-upload :file-list="fileList" ref="upload" action="#" list-type="picture-card" :auto-upload="false"
                    :limit="1" :on-exceed="() => ElMessage.warnig('此处只能选择一张图片')" :on-change="imgChange">
                    <el-icon>
                        <Plus />
                    </el-icon>
                </el-upload>
            </el-form-item>
            <el-form-item label="分类状态" prop="status">
                {{ formData.status }}
                <el-radio-group v-model="formData.status">
                    <el-radio label="启用" :value="true"></el-radio>
                    <el-radio label="禁用" :value="false"></el-radio>
                </el-radio-group>
            </el-form-item>
        </el-form>
        <template #footer>
            <el-space wrap>
                <el-button @click="reset">取消</el-button>
                <el-button @click="submit" type="primary">确认提交</el-button>
            </el-space>
        </template>
    </el-dialog>
</template>

<script setup>
import { storeToRefs } from 'pinia'
import useCategoryStore from '@/stores/category';
import { Plus } from '@element-plus/icons-vue'
import { useDialog } from '@/utils/hooks'
import { useTemplateRef, ref } from 'vue';
import { ElMessage } from 'element-plus';
import { createCategory, updateCategory } from '@/utils/api'
const categoryStore = useCategoryStore()
const { categoryList } = storeToRefs(categoryStore)
const { getCategoryListAction } = categoryStore
getCategoryListAction()
const upload = useTemplateRef('upload')
const categoryForm = useTemplateRef('categoryForm')
const formInitData = {
    parent: '',
    name: '',
    status: '',
    cover: ''
}
const { pk, title, visible, reset, formData } = useDialog({ formInitData, title: '新增分类', formRef: categoryForm })
const rules = {
    name: [{ required: true, message: '请输入分类名称' }],
    status: [{ required: true, message: '请选择分类状态' }],
}
const imgChange = (file) => {
    formData.value.cover = file.raw
}
// 图上上传组件默认要展示的图片数据
const fileList = ref([])
const openUpdateForm = ({ id, parent, name, status, cover }) => {
    pk.value = id
    formData.value = { name, parent, status }
    if (cover) {
        fileList.value = [{ url: cover }]
    }
    title.value = '更新分类'
    visible.value = true
}
const submit = () => {
    categoryForm.value.validate(async valid => {
        if (valid) {
            let result
            // 将 {} =>  FormData
            const fd = new FormData()
            for (let key in formData.value) {
                if (formData.value[key]) {
                    fd.append(key, formData.value[key])
                }
            }
            if (pk.value > 0) {
                // 更新
                result = await updateCategory(pk.value, fd)
            } else {
                // 新增
                result = await createCategory(fd)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                reset()
                // 移除图片上传组件中用户选择的图片
                upload.value.clearFiles()
                // 更新分类列表
                getCategoryListAction()
            }
        }
    })
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>