<template>
    <el-card>
        <h3>商品分类</h3>
        <div class="actions">
            <el-button @click="dialog.visible = true" type="primary" plain>新增分类</el-button>
        </div>
        <el-divider></el-divider>
        <el-table row-key="id" :data="categoryList">
            <el-table-column prop="id" label="序号" min-width="80"></el-table-column>
            <el-table-column prop="name" label="名称" min-width="100"></el-table-column>
            <el-table-column prop="cover" label="图片" min-width="100">
                <template v-slot="props">
                    <el-image v-if="props.row.cover" fit="cover" :src="props.row.cover"
                        style="width: 100px;"></el-image>
                </template>
            </el-table-column>
            <el-table-column prop="status" label="状态" min-width="100">
                <template v-slot="props">
                    <el-tag :type="props.row.status ? 'primary' : 'danger'">
                        {{ props.row.status ? '启用' : '禁用' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column label="操作" min-width="100">
                <template v-slot="props">
                    <el-space wrap>
                        <el-button type="primary" size="small" plain>商品</el-button>
                        <el-button @click="edit(props.row)" type="primary" size="small" plain>编辑</el-button>
                        <el-button @click="del(props.row.id)" type="danger" size="small" plain>删除</el-button>
                    </el-space>
                </template>
            </el-table-column>
        </el-table>
    </el-card>
    <CategoryDialog ref="dialog" />
</template>

<script setup>
import { removeCategory } from '@/utils/api';
import CategoryDialog from './CategoryDialog.vue'
import useCategoryStore from '@/stores/category';
import { withConfirm } from '@/utils/util';
import { storeToRefs } from 'pinia'
import { useTemplateRef } from 'vue';
const dialog = useTemplateRef('dialog')
const categoryStore = useCategoryStore()
const { categoryList } = storeToRefs(categoryStore)
const { getCategoryListAction } = categoryStore
//请求分类列表数据
getCategoryListAction()
const edit = (row) => {
    dialog.value.openUpdateForm(row)
}
const del = (id) => {
    withConfirm(async () => {
        return await removeCategory(id)
    }, () => {
        getCategoryListAction()
    })
}
</script>

<style></style>