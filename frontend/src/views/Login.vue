<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <h2 style="text-align: center; margin: 0;">Вход в CRM</h2>
      </template>
      
      <el-form @submit.prevent="handleLogin" v-loading="loading">
        <el-form-item>
          <el-input 
            v-model="form.email" 
            placeholder="Email" 
            :prefix-icon="Message"
            autocomplete="username"
          />
        </el-form-item>
        
        <el-form-item>
          <el-input 
            v-model="form.password" 
            placeholder="Пароль" 
            type="password" 
            :prefix-icon="Lock"
            autocomplete="current-password"
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        
        <el-button type="primary" native-type="submit" style="width: 100%">
          Войти
        </el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Message, Lock } from '@element-plus/icons-vue'
import api from '../api'

const router = useRouter()
const loading = ref(false)

const form = reactive({
  email: 'test@example.com',
  password: 'newPass789'
})

const handleLogin = async () => {
  loading.value = true
  try {
    // Используем централизованный api-клиент
    const response = await api.post('/auth/login', form)
    
    // Сохраняем токен
    localStorage.setItem('access_token', response.data.access_token)
    
    // Очищаем старый контекст организации при новом входе
    localStorage.removeItem('current_organization_id')
    
    ElMessage.success('Вы успешно вошли')
    router.push('/dashboard')
  } catch (error) {
    const msg = error.response?.data?.detail || 'Ошибка соединения с сервером'
    ElMessage.error(msg)
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f2f5;
}
.login-card {
  width: 400px;
}
</style>