<template>
  <el-container style="height: 100vh;">
    <!-- Боковое меню (скрыто на странице логина) -->
    <el-aside width="220px" v-if="$route.name !== 'Login'">
      <div class="logo">CRM Edu</div>
      <el-menu router default-active="/dashboard" class="el-menu-vertical">
        <el-menu-item index="/dashboard">
          <el-icon><HomeFilled /></el-icon>
          <span>Главная</span>
        </el-menu-item>
        <el-menu-item index="/organizations">
          <el-icon><OfficeBuilding /></el-icon>
          <span>Организации</span>
        </el-menu-item>
        <el-menu-item index="/courses">
          <el-icon><Reading /></el-icon>
          <span>Курсы</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <!-- Шапка -->
      <el-header style="padding: 0;">
        <div class="header-content">
          <h2 style="margin: 0;">Администратор</h2>
          <el-button v-if="$route.name !== 'Login'" type="danger" @click="logout">Выйти</el-button>
        </div>
      </el-header>

      <!-- Основной контент -->
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { HomeFilled, OfficeBuilding, Reading } from '@element-plus/icons-vue'
import router from './router'

const logout = () => {
  localStorage.removeItem('access_token')
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
</style>