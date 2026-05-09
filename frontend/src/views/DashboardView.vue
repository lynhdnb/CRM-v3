<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <button @click="handleLogout" class="btn btn-logout">Logout</button>
    </header>
    
    <div class="dashboard-content" v-if="user">
      <div class="welcome-card">
        <h2>Welcome, {{ user.first_name }} {{ user.last_name }}!</h2>
        <p>Email: {{ user.email }}</p>
        <p>Role: {{ user.role }}</p>
      </div>
      
      <div class="features-grid">
        <div class="feature-card">
          <h3>📚 Courses</h3>
          <p>Manage your courses and learning materials</p>
        </div>
        <div class="feature-card">
          <h3>📅 Schedule</h3>
          <p>View your lesson schedule and attendance</p>
        </div>
        <div class="feature-card">
          <h3>💰 Finance</h3>
          <p>Track payments and transactions</p>
        </div>
        <div class="feature-card">
          <h3>👥 Groups</h3>
          <p>Join and manage study groups</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.currentUser)

onMounted(async () => {
  if (!authStore.user && authStore.token) {
    try {
      await authStore.fetchUser()
    } catch (error) {
      console.error('Failed to fetch user:', error)
    }
  }
})

const handleLogout = () => {
  authStore.logout()
  router.push('/login')
}
</script>

<style scoped>
.dashboard {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.dashboard-header {
  background: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.dashboard-header h1 {
  color: #333;
  margin: 0;
}

.btn-logout {
  padding: 0.5rem 1.5rem;
  background-color: #f44336;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
  transition: background-color 0.3s;
}

.btn-logout:hover {
  background-color: #d32f2f;
}

.dashboard-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.welcome-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.welcome-card h2 {
  color: #333;
  margin-bottom: 1rem;
}

.welcome-card p {
  color: #666;
  margin: 0.5rem 0;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1.5rem;
}

.feature-card {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
}

.feature-card h3 {
  color: #333;
  margin-bottom: 1rem;
  font-size: 1.5rem;
}

.feature-card p {
  color: #666;
}
</style>
