<template>
  <div class="home">
    <h1>CRM System for Educational Institutions</h1>
    <p>Welcome to our CRM platform</p>
    <div class="actions">
      <router-link to="/login" class="btn btn-primary">Login</router-link>
      <router-link to="/register" class="btn btn-secondary">Register</router-link>
    </div>
  </div>
</template>

<script setup>
</script>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  text-align: center;
  padding: 2rem;
}

h1 {
  color: #333;
  margin-bottom: 1rem;
}

p {
  color: #666;
  margin-bottom: 2rem;
}

.actions {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 0.75rem 1.5rem;
  border-radius: 4px;
  text-decoration: none;
  font-weight: 500;
  transition: all 0.3s;
}

.btn-primary {
  background-color: #4CAF50;
  color: white;
}

.btn-primary:hover {
  background-color: #45a049;
}

.btn-secondary {
  background-color: #2196F3;
  color: white;
}

.btn-secondary:hover {
  background-color: #1976D2;
}
</style>
