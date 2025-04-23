// src/services/api.js
import axios from 'axios'
import { useAuthStore } from '@/stores/authStore'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL + '/api',
  headers: {
    'Content-Type': 'application/json',
  },
  withCredentials: true,  // Important for CORS with credentials
})

// Attach token to every request if available
api.interceptors.request.use((config) => {
  const auth = useAuthStore()
  if (auth?.token) {
    config.headers.Authorization = `Bearer ${auth.token}`
  }
  
  // Special handling for login endpoint
  if (config.url === '/auth/login') {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded'
  }
  
  return config
})

export default api
