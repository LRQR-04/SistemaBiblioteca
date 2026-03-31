import { defineStore } from 'pinia'
import api from '../services/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),

  actions: {
    async login(email, password) {
      const res = await api.post('/auth/login', { email, password })

      this.token = res.data.access_token
      localStorage.setItem('token', this.token)
    },

    logout() {
      this.token = null
      localStorage.removeItem('token')
    },
  },
})
