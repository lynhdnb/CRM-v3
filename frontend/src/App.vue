<template>
  <el-container style="height: 100vh;">
    <!-- Сайдбар показывается только если пользователь авторизован -->
    <el-aside width="220px" v-if="isLoggedIn">
      <div class="logo">CRM Edu</div>
      <el-menu router :default-active="$route.path" class="el-menu-vertical">
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>Главная</span>
        </el-menu-item>
        <el-menu-item index="/courses">
          <el-icon><Reading /></el-icon>
          <span>Курсы</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header style="padding: 0;">
        <div class="header-content">
          <h2 style="margin: 0;">{{ isLoggedIn ? 'Администратор' : 'Вход в систему' }}</h2>
          <el-button v-if="isLoggedIn" type="danger" @click="logout">Выйти</el-button>
        </div>
      </el-header>

      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { HomeFilled, Reading } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

// Реактивная переменная вместо computed
const isLoggedIn = ref(!!localStorage.getItem('access_token'))

// Функция синхронизации состояния с localStorage
const syncAuthState = () => {
  isLoggedIn.value = !!localStorage.getItem('access_token')
}

// Следим за изменением маршрута (логин/дашборд/курсы)
watch(() => route.path, syncAuthState)
onMounted(syncAuthState)

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('current_organization_id')
  syncAuthState() // Мгновенно скрываем сайдбар
  router.push('/login')
}
</script>

<style scoped>
.logo {
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  background-color: #409eff;
  color: white;
}
.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  background-color: #fff;
  border-bottom: 1px solid #dcdfe6;
}
.el-menu-vertical:not(.el-menu--collapse) {
  width: 220px;
  min-height: 400px;
}
</style>