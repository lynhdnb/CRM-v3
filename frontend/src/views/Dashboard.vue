<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Панель управления</span>
              <el-tag type="success">Система активна</el-tag>
            </div>
          </template>
          <p>Зарегистрировано организаций: <strong>{{ organizations.length }}</strong></p>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>Список организаций</span>
              <el-button type="primary" size="small" @click="fetchOrgs">Обновить</el-button>
            </div>
          </template>
          
          <el-table :data="organizations" style="width: 100%" v-loading="loading">
            <el-table-column prop="name" label="Название" width="180" />
            <el-table-column prop="slug" label="Slug" width="150" />
            <el-table-column prop="city" label="Город" width="120" />
            <el-table-column prop="timezone" label="Часовой пояс" width="180" />
            <el-table-column prop="created_at" label="Дата создания" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const organizations = ref([])
const loading = ref(false)

const fetchOrgs = async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('access_token')
    if (!token) {
      ElMessage.warning('Нет токена доступа')
      return
    }

    const response = await axios.get('/api/v1/organizations/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    organizations.value = response.data
  } catch (error) {
    ElMessage.error('Ошибка загрузки данных')
    console.error(error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchOrgs()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.dashboard {
  padding: 10px;
}
</style>