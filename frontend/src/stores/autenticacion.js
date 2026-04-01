import { defineStore } from 'pinia'
import api from '../services/api'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),

  actions: {
    async login(email, contrasenia) {
      const res = await api.post('/auth/login', { email, contrasenia })

      this.token = res.data.access_token
      localStorage.setItem('token', this.token)
      this.user = jwtDecode(this.token)
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
    },
  },
})
