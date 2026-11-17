<template>
  <div class="login-container">
    <el-card class="login-card">
      <h2>销售业绩统计系统</h2>
      <el-divider></el-divider>
      <el-form ref="ruleFormRef" style="max-width: 600px" :model="formData" status-icon :rules="rules"
        label-width="auto" size="large">
        <el-form-item prop="username">
          <el-input placeholder="请输入登录账号" v-model="formData.username" autocomplete="off" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="formData.password" type="password" autocomplete="off" show-password
            placeholder="请输入账号密码" />
        </el-form-item>

        <el-form-item>
          <el-button round style="width: 100%" type="primary" @click="submitForm(ruleFormRef)">
            确认登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus';
import useUserStore from '../stores/user'
import { reactive, ref } from "vue";
// 获取路由对象
const router = useRouter()
const ruleFormRef = ref();
// 获取数据仓库对象
const userStore = useUserStore()
const { loginAction } = userStore
// 表单数据
const formData = reactive({
  username: "",
  password: "",
});
// 验证规则
const rules = reactive({
  username: [{ required: true, message: "请输入登录账号", trigger: "blur" }],
  password: [{ required: true, message: "请输入账号密码", trigger: "blur" }],
});

const submitForm = (formEl) => {
  if (!formEl) return;
  formEl.validate(async (valid) => {
    if (valid) {
      // 提交表单
      const result = await loginAction(formData)
      if (result) {
        // 登录成功
        ElMessage.success('登录成功')
        // 自动跳转
        router.push('/')
      }
    }
  });
}
</script>
<style scoped>
.login-container {
  height: 100vh;
  width: 100vw;
  background-color: rgba(0, 0, 0, 0.1);
}

.login-card {
  width: 500px;
  position: fixed;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
</style>
