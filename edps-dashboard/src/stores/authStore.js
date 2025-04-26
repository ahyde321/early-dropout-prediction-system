import api from '@/services/api'
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || sessionStorage.getItem('token') || '',
    user: null,
    refreshTimer: null,
  }),

  getters: {
    isAuthenticated: (state) => !!state.token,
    roles: (state) => state.user?.role || '',
    isAdmin: (state) => state.user?.role === 'admin',
    isAdvisor: (state) => state.user?.role === 'advisor',
  },

  actions: {
    async login(email, password, remember = false, toast) {
      try {
        const form = new URLSearchParams()
        form.append('username', email)
        form.append('password', password)

        const res = await api.post('/auth/login', form, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        })

        const token = res.data.access_token
        this.setToken(token, remember)

        await this.fetchMe()
        toast.success('Logged in successfully')
      } catch (err) {
        this.logout()
        throw new Error('Invalid credentials')
      }
    },

    setToken(token, remember) {
      this.token = token
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`

      const payload = JSON.parse(atob(token.split('.')[1]))
      const expiry = payload.exp * 1000

      if (remember) {
        localStorage.setItem('token', token)
        localStorage.setItem('token_expiry', expiry)
      } else {
        sessionStorage.setItem('token', token)
        sessionStorage.setItem('token_expiry', expiry)
      }

      const timeUntilRefresh = expiry - Date.now() - 60000
      if (timeUntilRefresh > 0) {
        this.refreshTimer = setTimeout(this.refreshToken, timeUntilRefresh)
      }
    },

    async refreshToken() {
      try {
        const res = await api.post('/auth/refresh')
        const token = res.data.access_token

        const remember = !!localStorage.getItem('token')
        this.setToken(token, remember)
      } catch (err) {
        console.error('❌ Token refresh failed', err)
        this.logout()
      }
    },

    async fetchMe() {
      try {
        const res = await api.get('/auth/me')
        this.user = res.data
      } catch (err) {
        console.error('❌ Failed to fetch user profile', err)
        this.logout()
      }
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem('token')
      sessionStorage.removeItem('token')
      localStorage.removeItem('token_expiry')
      sessionStorage.removeItem('token_expiry')
      delete api.defaults.headers.common['Authorization']
      if (this.refreshTimer) clearTimeout(this.refreshTimer)
    },

    checkTokenExpiration() {
      const expiry = localStorage.getItem('token_expiry') || sessionStorage.getItem('token_expiry')
      if (expiry && Date.now() > parseInt(expiry)) {
        this.logout()
      }
    },

    async tryAutoLogin() {
      const token = localStorage.getItem('token') || sessionStorage.getItem('token')
      const expiry = localStorage.getItem('token_expiry') || sessionStorage.getItem('token_expiry')
      if (!token || !expiry) return

      if (Date.now() > parseInt(expiry)) {
        // Attempt token refresh
        await this.refreshToken()
      } else {
        this.setToken(token, !!localStorage.getItem('token'))
        await this.fetchMe()
      }
    },

    updateUser(userData) {
      this.user = userData
      localStorage.setItem('user', JSON.stringify(userData))
    },
  }
})