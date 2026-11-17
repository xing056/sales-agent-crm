<template>
    <el-dialog @close="reset" :title="title" v-model="visible" fullscreen>
        <el-form :rules="rules" ref="productForm" :model="formData">
            <el-form-item label="商品分类" prop="category_id">
                <el-tree-select v-model="formData.category_id" :data="categoryList"
                    :props="{ value: 'id', label: 'name' }"></el-tree-select>
            </el-form-item>
            <el-form-item label="商品名称" prop="name">
                <el-input v-model.trim="formData.name" placeholder="请输入商品名称"></el-input>
            </el-form-item>
            <el-form-item label="商品封面" prop="cover">
                <el-upload :file-list="imgList" ref="upload" :on-change="coverChange" :auto-upload="false"
                    list-type="picture-card" :limit="1" :on-exceed="() => ElMessage.warning('此处只能选择一张图片')">
                    <el-icon>
                        <Plus />
                    </el-icon>
                </el-upload>
            </el-form-item>
            <el-form-item label="商品价格" prop="price">
                <el-input v-model.trim="formData.price" placeholder="请输入商品价格"></el-input>
            </el-form-item>
            <el-form-item label="佣金比例" prop="commission_rate">
                <el-input v-model.trim="formData.commission_rate" placeholder="请输入商品佣金比例"></el-input>
            </el-form-item>
            <el-form-item label="商品库存" prop="stock_num">
                <el-input v-model.trim="formData.stock_num" placeholder="请输入商品价格"></el-input>
            </el-form-item>
            <el-form-item label="商品销量" prop="sale_num">
                <el-input v-model.trim="formData.sale_num" placeholder="请输入商品价格"></el-input>
            </el-form-item>
            <el-form-item label="商品状态" prop="status">
                <el-switch v-model="formData.status"></el-switch>
            </el-form-item>
            <el-form-item label="商品介绍" prop="description">
                <div style="border: 1px solid #ccc">
                    <Toolbar style="border-bottom: 1px solid #ccc" :editor="editorRef" :defaultConfig="toolbarConfig"
                        mode="default" />
                    <Editor style="height: 300px; overflow-y: hidden;" v-model="formData.description"
                        :defaultConfig="editorConfig" @onCreated="handleCreated" />
                </div>
            </el-form-item>

        </el-form>
        <template #footer>
            <el-button @click="reset">取消</el-button>
            <el-button @click="submit" type="primary">确认提交</el-button>
        </template>
    </el-dialog>
</template>

<script setup>
import { createProduct, updateProduct } from '@/utils/api'
import '@wangeditor/editor/dist/css/style.css' // 引入 css
import { onBeforeUnmount, ref, resolveDynamicComponent, shallowRef } from 'vue'
import { Editor, Toolbar } from '@wangeditor/editor-for-vue'
import { storeToRefs } from 'pinia'
import useCategoryStore from '@/stores/category';
import useUserStore from '@/stores/user';
import { Plus } from '@element-plus/icons-vue'
import { useDialog } from '@/utils/hooks'
import { ElMessage } from 'element-plus'
import { useTemplateRef } from 'vue'
const upload = useTemplateRef('upload')
// 编辑器实例，必须用 shallowRef
const editorRef = shallowRef()
// 上传接口已改为需要登录，编辑器发的请求不走 axios 拦截器，这里手动带上令牌
const userStore = useUserStore()
const authHeaders = () => ({ Authorization: `Bearer ${userStore.accessToken}` })

// 内容 HTML
const toolbarConfig = {}
const editorConfig = {
    placeholder: '请输入内容...',
    MENU_CONF: {
        uploadImage: {
            // 设置提交图片的参数名, 需要和后端数据接口保持一致
            fieldName: 'image',
            // 图片大小如果小于该临界值,则将图转换为base64
            maxFileSize: 1 * 1024 * 1024, // 1M
            // 图片上传接口地址
            server: "/api/common/upload_image/",
            // 请求头里带上登录凭证，否则后端会返回 401
            headers: authHeaders(),
            allowedFileTypes: ['image/*']
        }
    }
}

// 组件销毁时，也及时销毁编辑器
onBeforeUnmount(() => {
    const editor = editorRef.value
    if (editor == null) return
    editor.destroy()
})

const handleCreated = (editor) => {
    editorRef.value = editor // 记录 editor 实例，重要！
}


const categoryStore = useCategoryStore()
const { categoryList } = storeToRefs(categoryStore)
const { getCategoryListAction } = categoryStore
getCategoryListAction()
const productForm = useTemplateRef('productForm')
const formInitData = {
    category_id: '',
    name: "",
    price: '',
    stock_num: '',
    sale_nul: '',
    commission_rate: '',
    cover: '',
    description: '',
    status: true
}
const { pk, visible, title, formData, reset } = useDialog({ formInitData, title: '新增商品', formRef: productForm })
const coverChange = (file) => {
    formData.value.cover = file.raw
}
const rules = {
    category_id: [{ required: true, message: '请选择商品分类' }],
    name: [{ required: true, message: '请输入商品名称' }],
    price: [{ pattern: /^\d+(\.)?\d+$/, required: true, message: '请输入商品价格' }],
    commission_rate: [{ pattern: /^\d+\.\d+$/, required: true, message: '请输入商品佣金比例' }],
    cover: [{ required: true, message: '请选择商品封面图' }],
    stock_num: [{ pattern: /^\d+$/, required: true, message: '请输入商品库存数量' }],
    sale_num: [{ pattern: /^\d+$/, required: true, message: '请输入商品销量' }],
    status: [{ required: true, message: '请选择商品状态' }],
    description: [{ required: true, message: '请输入商品详细描述' }],
}
const emit = defineEmits(['updateProductData'])
const submit = () => {
    productForm.value.validate(async valid => {
        if (valid) {
            const fd = new FormData()
            for (let key in formData.value) {
                if (![undefined,'',null].includes(formData.value[key])) {
                    fd.append(key, formData.value[key])
                }
            }
            // 检查参数cover, 如果参数类型为字符串, 就将其从fd中删除
            if (typeof formData.value.cover === 'string') {
                fd.delete('cover')
            }
            let result
            if (pk.value > 0) {
                result = await updateProduct(pk.value, fd)
            } else {
                result = await createProduct(fd)
            }
            if ([200, 201].includes(result.status)) {
                ElMessage.success('操作成功')
                reset()
                upload.value.clearFiles()
                // 更新商品列表
                emit('updateProductData')
            }
        }
    })
}
const imgList = ref([])
const openUpdateForm = ({ id, name, category_id, price, stock_num, sale_num, commission_rate, cover, status, description }) => {
    pk.value = id
    formData.value = {
        name, category_id, price, stock_num, sale_num, commission_rate, cover, status, description
    }
    if (cover) {
        imgList.value = [{ url: cover }]
    }
    title.value = '更新商品数据'
    visible.value = true
}
defineExpose({
    visible, openUpdateForm
})
</script>

<style></style>