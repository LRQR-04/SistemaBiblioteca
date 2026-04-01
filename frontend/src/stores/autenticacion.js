import { defineStore } from 'pinia'
import api from '../services/api'
import { jwtDecode } from 'jwt-decode'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('usuario')) || null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
  },

  actions: {
    async login(email, contrasenia) {
      const res = await api.post('/auth/login', { email, contrasenia })

      this.token = res.data.access_token
      const decoded = jwtDecode(this.token)

      this.user = decoded

      localStorage.setItem('token', this.token)
      localStorage.setItem('usuario', JSON.stringify(this.user))
    },

    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('token')
      localStorage.removeItem('usuario')
    },

    initAuth() {
      const token = localStorage.getItem('token')

      if (!token) return

      try {
        this.token = token

        const decoded = jwtDecode(token)
        this.user = decoded
      } catch (error) {
        this.logout()
      }
    },
  },
})
