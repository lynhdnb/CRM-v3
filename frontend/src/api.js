import axios from 'axios'

// Создаём инстанс axios с базовыми настройками
const api = axios.create({
  baseURL: '/api/v1', // Прокси Vite перенаправит на http://127.0.0.1:8000/api/v1
  headers: {
    'Content-Type': 'application/json'
  }
})

// Автоматически добавляем токен к каждому запросу
api.interceptors.request.use(config => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  
  // Добавляем контекст организации, если выбран
  const orgId = localStorage.getItem('current_organization_id')
  if (orgId) {
    config.headers['X-Organization-Id'] = orgId
  }
  
  return config
})

// Обработка ошибок ответа (опционально: редирект на логин при 401)
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api