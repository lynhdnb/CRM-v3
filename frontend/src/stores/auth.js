import { defineStore } from 'pinia'
import api from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('access_token') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    currentUser: (state) => state.user
  },

  actions: {
    async login(email, password) {
      const formData = new FormData()
      formData.append('username', email)
      formData.append('password', password)

      const response = await api.post('/auth/login', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })

      this.token = response.data.access_token
      localStorage.setItem('access_token', response.data.access_token)

      await this.fetchUser()
      return response.data
    },

    async register(userData) {
      const response = await api.post('/auth/register', userData)
      return response.data
    },

    async fetchUser() {
      if (!this.token) return

      try {
        const response = await api.get('/auth/me')
        this.user = response.data
      } catch (error) {
        this.logout()
        throw error
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
    }
  }
})
