<template>
  <div class="courses-page">
    <!-- Предупреждение, если организация не выбрана -->
    <el-alert 
      v-if="!currentOrgId" 
      title="Контекст не выбран" 
      description="Перейдите на главную страницу и выберите организацию, чтобы видеть её курсы." 
      type="warning" 
      show-icon 
      :closable="false"
      style="margin-bottom: 20px;"
    />

    <el-card v-else>
      <template #header>
        <div class="card-header">
          <span>Курсы организации</span>
          <div class="actions">
            <el-button type="primary" size="small" @click="openCreateDialog">+ Создать курс</el-button>
            <el-button type="info" plain size="small" @click="fetchCourses" :loading="loading">Обновить</el-button>
          </div>
        </div>
      </template>

      <el-table :data="courses" v-loading="loading" style="width: 100%">
        <el-table-column prop="id" label="ID" width="200" />
        <el-table-column prop="name" label="Название курса" />
        <el-table-column prop="description" label="Описание" show-overflow-tooltip />
      </el-table>

      <div v-if="!loading && courses.length === 0" class="empty-state">
        <el-empty description="В этой организации пока нет курсов" />
      </div>
    </el-card>

    <!-- Диалог создания курса -->
    <el-dialog v-model="dialogVisible" title="Новый курс" width="500px">
      <el-form :model="form" label-width="100px">
        <el-form-item label="Название" required>
          <el-input v-model="form.name" placeholder="Например: Основы диджеинга" />
        </el-form-item>
        <el-form-item label="Описание">
          <el-input v-model="form.description" type="textarea" rows="3" placeholder="Краткое описание программы" />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="dialogVisible = false">Отмена</el-button>
          <el-button type="primary" @click="submitCourse" :loading="submitting">Создать</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import api from '../api'

const courses = ref([])
const loading = ref(false)
const currentOrgId = ref(localStorage.getItem('current_organization_id'))

// Состояние диалога и формы
const dialogVisible = ref(false)
const submitting = ref(false)
const form = reactive({
  name: '',
  description: ''
})

const fetchCourses = async () => {
  if (!currentOrgId.value) return

  loading.value = true
  try {
    // api.get автоматически добавит заголовок X-Organization-Id
    const response = await api.get('/courses/')
    courses.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки курсов:', error)
    if (error.response?.status === 403) ElMessage.error('Нет доступа к курсам')
    else ElMessage.error('Не удалось загрузить курсы')
  } finally {
    loading.value = false
  }
}

const openCreateDialog = () => {
  form.name = ''
  form.description = ''
  dialogVisible.value = true
}

const submitCourse = async () => {
  if (!form.name) {
    ElMessage.warning('Введите название курса')
    return
  }
  
  submitting.value = true
  try {
    // 🔧 Исправлено: отправляем 'title' вместо 'name', как требует модель БД
    const payload = {
      title: form.name,  // <-- ключ соответствует полю в models.py
      description: form.description,
      organization_id: currentOrgId.value
    }
    
    await api.post('/courses/', payload)
    
    ElMessage.success('Курс успешно создан')
    dialogVisible.value = false
    fetchCourses()
  } catch (error) {
    console.error('Ошибка создания:', error)
    const msg = error.response?.data?.detail || 'Ошибка при создании курса'
    ElMessage.error(msg)
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.courses-page { padding: 20px; }
.card-header { display: flex; justify-content: space-between; align-items: center; }
.actions { display: flex; gap: 10px; }
.empty-state { padding: 40px 0; text-align: center; }
</style>