<template>
    <el-card>
        <h3>商品管理</h3>
        <div class="actions">
            <el-button type="primary" @click="dialog.visible = true">新增商品</el-button>
            <el-button type="primary" @click="createOrder">创建订单</el-button>
        </div>
        <el-divider></el-divider>
        <el-table @selection-change="checkedProductChange" :data="productList">
            <!-- 表格每一个前添加一个复选框 -->
            <el-table-column type="selection" min-width="60"></el-table-column>
            <el-table-column prop="id" label="序号" min-width="60"></el-table-column>
            <el-table-column prop="category.name" label="商品分类" min-width="80"></el-table-column>
            <el-table-column prop="name" label="商品名称" min-width="80"></el-table-column>
            <el-table-column prop="price" label="商品价格" min-width="80"></el-table-column>
            <el-table-column prop="cover" label="商品封面图" min-width="120">
                <template v-slot="props">
                    <el-image v-if="props.row.cover" fit="cover" :src="props.row.cover"
                        style="width: 120px;height: 120px;"></el-image>
                </template>
            </el-table-column>
            <el-table-column prop="stock_num" label="商品库存" min-width="80"></el-table-column>
            <el-table-column prop="sale_num" label="商品销量" min-width="80"></el-table-column>
            <el-table-column prop="commission_rate" label="商品佣金比例" min-width="80"></el-table-column>
            <el-table-column prop="status" label="商品状态" min-width="80">
                <template v-slot="props">
                    <el-tag :type="props.row.status ? 'primary' : 'danger'">
                        {{ props.row.status ? '在售' : '下架' }}
                    </el-tag>
                </template>
            </el-table-column>
            <el-table-column fixed="right" label="操作" min-width="120">
                <template v-slot="props">
                    <el-space wrap>
                        <el-button @click="edit(props.row)" size="small" plain type="primary">编辑</el-button>
                        <el-button @click="del(props.row.id)" size="small" plain type="danger">删除</el-button>
                    </el-space>
                </template>
            </el-table-column>
        </el-table>
        <br>
        <el-pagination @current-change="pageChange" :page-size="size" :total="productCount"
            layout="total,prev,pager,next,jumper" background></el-pagination>
    </el-card>
    <ProductDialog ref="dialog" @updateProductData="updateProductData" />
</template>

<script setup>
import { useRouter } from 'vue-router'
import useCartStore from '@/stores/cart'
import ProductDialog from './ProductDialog.vue'
import { usePager } from '@/utils/hooks'
import { storeToRefs } from 'pinia'
import useProductStore from '@/stores/product'
import { ElNotification } from 'element-plus'
import { useTemplateRef, ref } from 'vue'
import { withConfirm } from '@/utils/util'
import { removeProduct } from '@/utils/api'
const productStore = useProductStore()
const { productList, productCount } = storeToRefs(productStore)
const { getGoodsListAction } = productStore
const { page, size } = usePager()
const dialog = useTemplateRef('dialog')
getGoodsListAction({ page: page.value, size: size.value })
const pageChange = (num) => {
    page.value = num
    getGoodsListAction({ page: page.value, size: size.value })
}
const updateProductData = () => {
    getGoodsListAction({ page: page.value, size: size.value })
}
const edit = (row) => {
    dialog.value.openUpdateForm(row)
}
const del = (id) => {
    withConfirm(async () => {
        return await removeProduct(id)
    }, () => {
        getGoodsListAction({ page: page.value, size: size.value })
    })
}
const cartStore = useCartStore()
const { bulkAddCartProduct } = cartStore
const { cartList } = storeToRefs(cartStore)
const router = useRouter()
// 用户选择商品
const checkedProductList = ref([])
const checkedProductChange = (rows) => {
    checkedProductList.value = rows
}
// 创建订单
const createOrder = () => {
    if (checkedProductList.value.length === 0 && cartList.value.length === 0) {
        return ElNotification.info('请选择商品')
    }
    if (checkedProductList.value.length > 0) {
        // 批量添加商品到购物车列表中
        bulkAddCartProduct(checkedProductList.value)
        ElNotification.success('添加商品成功')
    }

    // 自动跳转到创建订单页面
    router.push({ name: "orderCreate" })
}
</script>

<style></style>