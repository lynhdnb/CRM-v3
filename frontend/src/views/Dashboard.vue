<template>
  <div class="dashboard">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>Доступные организации</span>
          <div class="header-actions">
            <el-tag v-if="currentOrgId" type="success" effect="dark" size="large">
              Активная: {{ currentOrgName }}
            </el-tag>
            <el-button 
              v-if="currentOrgId" 
              type="warning" 
              plain 
              size="small" 
              @click="clearSelection"
            >
              Сбросить выбор
            </el-button>
          </div>
        </div>
      </template>

      <el-table 
        :data="organizations" 
        v-loading="loading" 
        style="width: 100%"
        highlight-current-row
        @current-change="handleRowSelect"
      >
        <el-table-column prop="name" label="Название" width="220" />
        <el-table-column prop="slug" label="URL-идентификатор" width="180" />
        <el-table-column prop="city" label="Город" width="120" />
        <el-table-column prop="timezone" label="Часовой пояс" width="180" />
        <el-table-column label="Статус" width="120">
          <template #default="{ row }">
            <el-tag :type="currentOrgId === row.id ? 'success' : 'info'" effect="plain">
              {{ currentOrgId === row.id ? 'Активна' : 'Неактивна' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="Действия" width="140">
          <template #default="{ row }">
            <el-button 
              :type="currentOrgId === row.id ? 'success' : 'primary'"
              size="small"
              @click="selectOrganization(row)"
              :disabled="currentOrgId === row.id"
            >
              {{ currentOrgId === row.id ? 'Выбрана' : 'Работать' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div v-if="!loading && organizations.length === 0" class="empty-state">
        <el-empty description="У вас нет доступа к организациям" />
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const organizations = ref([])
const loading = ref(false)
const currentOrgId = ref(localStorage.getItem('current_organization_id') || null)

const currentOrgName = computed(() => {
  const org = organizations.value.find(o => o.id === currentOrgId.value)
  return org ? org.name : '—'
})

const fetchOrganizations = async () => {
  loading.value = true
  try {
    const response = await api.get('/organizations/')
    organizations.value = response.data
  } catch (error) {
    ElMessage.error('Не удалось загрузить список организаций')
    console.error(error)
  } finally {
    loading.value = false
  }
}

const selectOrganization = (org) => {
  currentOrgId.value = org.id
  localStorage.setItem('current_organization_id', org.id)
  ElMessage.success(`Контекст переключён на "${org.name}"`)
}

const clearSelection = () => {
  currentOrgId.value = null
  localStorage.removeItem('current_organization_id')
  ElMessage.info('Выбор организации сброшен')
}

const handleRowSelect = (row) => {
  if (row) selectOrganization(row)
}

onMounted(() => {
  fetchOrganizations()
})
</script>

<style scoped>
.dashboard { padding: 20px; }
.card-header { 
  display: flex; 
  justify-content: space-between; 
  align-items: center; 
  flex-wrap: wrap;
  gap: 10px;
}
.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}
.empty-state { padding: 40px 0; text-align: center; }
</style>