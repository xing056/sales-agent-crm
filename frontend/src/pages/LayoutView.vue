<template>
  <div class="layout-container">
    <el-container>
      <el-aside width="200px">
        <h3 class="logo-text">销售业绩统计系统</h3>
        <el-menu router :default-active="$route.path" active-text-color="#FFF" :background-color="menuBg"
          :text-color="menuText" unique-opened>

          <!-- 工作台走前端硬编码：不动数据库菜单表，所有登录用户都能看到 -->
          <el-menu-item index="/dashboard">
            <el-icon>
              <Odometer />
            </el-icon>
            <span>工作台</span>
          </el-menu-item>

          <el-sub-menu :index="item.id + ''" v-for="item in currRole.nav_menu" :key="item.id">
            <template #title>
              <el-icon>
                <component :is="icons[item.icon]" />
              </el-icon>
              <span>{{ item.title }}</span>
            </template>
            <el-menu-item v-for="val in item.children" :key="val.id" :index="val.path">{{ val.title }}</el-menu-item>
          </el-sub-menu>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header>
          <!-- 明暗主题切换 -->
          <el-tooltip :content="isDark ? '切换到明亮' : '切换到暗黑'" placement="bottom">
            <el-button class="theme-btn" circle text @click="switchTheme">
              <el-icon :size="17">
                <Moon v-if="!isDark" />
                <Sunny v-else />
              </el-icon>
            </el-button>
          </el-tooltip>
          <el-dropdown>
            <span class="el-dropdown-link">
              {{ loginInfo.username }}【{{ currRole.name }}】
              <el-icon class="el-icon--right">
                <arrow-down />
              </el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="toggleRole(index)" v-for="(item, index) in loginInfo.role" :key="item.id">{{
                  item.name }}</el-dropdown-item>
                <el-dropdown-item divided @click="$router.push({ name: 'profile' })">个人资料</el-dropdown-item>
                <el-dropdown-item @click="followSystem">
                  主题：跟随系统{{ themeChoice === 'auto' ? '（当前）' : '' }}
                </el-dropdown-item>
                <el-dropdown-item divided @click="logout">
                  安全退出
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </el-header>
        <el-main>
          <!-- 二级路由出口 -->
          <router-view></router-view>
        </el-main>
      </el-container>
    </el-container>
    <!-- AI 助手：常驻在后台管理右下角，以当前登录人身份操作 -->
    <AgentDrawer />
  </div>
</template>
<script setup>
import { icons } from '../utils/config'
import { storeToRefs } from 'pinia'
import useUserStore from '../stores/user'
import AgentDrawer from '@/components/AgentDrawer.vue'
import { ArrowDown, Moon, Sunny, Odometer } from "@element-plus/icons-vue";
import { useRouter, useRoute } from "vue-router";
import { withConfirm } from '@/utils/util';
import { computed, ref, watch } from 'vue';
import { getChoice, getTheme, toggleTheme, useSystemTheme } from '@/utils/theme';
// 获取数据仓库对象
const userStore = useUserStore()
const { loginInfo, currRole } = storeToRefs(userStore)
const { toggleRole, reset } = userStore
const router = useRouter()
const route = useRoute()

/* ---------- 明暗主题 ---------- */
// isDark 只负责顶栏图标的显示；真正的选择（含"跟随系统"）由 theme.js 持久化
const isDark = ref(getTheme() === 'dark')
const themeChoice = ref(getChoice())
const switchTheme = () => {
  const next = toggleTheme()
  isDark.value = next === 'dark'
  themeChoice.value = next
}
// 点了「跟随系统」后，系统切暗色时页面会自己跟着变
const followSystem = () => {
  const next = useSystemTheme()
  isDark.value = next === 'dark'
  themeChoice.value = 'auto'
}
// 暗色下侧边栏不必再压那么黑，浅一档更有层次
const menuBg = computed(() => (isDark.value ? '#1d1e1f' : '#333'))
const menuText = computed(() => '#FFF')

const logout = () => {
  withConfirm(() => {
    // 重置user数据仓库中的数据
    reset()
    // 移除本地存储中的登录数据
    localStorage.removeItem('user')
    // 自动跳转到登录页面
    router.push({ name: "login" })
  })
};
watch(currRole, (nextState) => {
  if (nextState.link_url) {
    // 防止用户切换角色之后, 停留在权限之外的功能页面
    if (!nextState.link_url.includes(route.path)) {
      // 自动跳转到一个公开页面
      router.replace({ name: 'layout' })
    }
  }
})
</script>

<style scoped>
.logo-text {
  cursor: pointer;
  color: #fff;
  text-align: center;
  height: 60px;
  line-height: 60px;
}

.layout-container {
  height: 100vh;
  width: 100vw;
  background-color: var(--app-bg-page);
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #333;
}

.el-menu {
  border-right: 0;
}

.is-active {
  background-color: var(--el-color-primary);
}

.el-header {
  position: relative;
  background-color: var(--app-bg-card);
  /* 改成 flex 排列：主题切换按钮 + 用户下拉，不再靠绝对定位硬凑 */
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
}

.theme-btn {
  color: var(--el-text-color-regular);
}

.theme-btn:hover {
  color: var(--el-color-primary);
}

.el-dropdown {
  position: static;
  top: auto;
  right: auto;
}
</style>
