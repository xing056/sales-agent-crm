<template>
    <el-card>
        <h1>404-您访问的页面不存在</h1>
        <el-divider></el-divider>
        <div class="actions">
            <el-button type="primary" @click="$router.push({ name: 'layout' })">返回管理后台首页</el-button>
        </div>
    </el-card>
</template>

<script>

</script>

<style></style>