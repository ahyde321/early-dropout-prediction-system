<template>
    <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-white to-gray-100 p-6">
      <div class="w-full max-w-sm bg-white rounded-2xl shadow-md p-6 border border-gray-200">
        <h1 class="text-xl font-bold text-center text-gray-800 mb-4">Login to EDPS</h1>
  
        <form @submit.prevent="handleLogin" class="space-y-4">
          <div>
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input
              v-model="email"
              type="email"
              class="mt-1 w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-sky-300 focus:outline-none shadow-sm"
              required
            />
          </div>
  
          <div>
            <label class="block text-sm font-medium text-gray-700">Password</label>
            <input
              v-model="password"
              type="password"
              class="mt-1 w-full px-4 py-2 border rounded-md focus:ring-2 focus:ring-sky-300 focus:outline-none shadow-sm"
              required
            />
          </div>
  
          <div class="flex items-center justify-between">
            <label class="flex items-center gap-2 text-sm text-gray-600">
              <input type="checkbox" v-model="rememberMe" class="rounded" />
              Remember me
            </label>
          </div>
  
          <button
            type="submit"
            class="w-full bg-sky-500 text-white py-2 rounded-md hover:bg-sky-600 transition"
            :disabled="loading"
          >
            <span v-if="loading">Logging in...</span>
            <span v-else>Login</span>
          </button>
  
          <p v-if="error" class="text-sm text-red-500 text-center pt-2">{{ error }}</p>
        </form>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import { useRouter } from 'vue-router'
  import { useAuthStore } from '@/stores/authStore'
  import { useToast } from 'vue-toastification'
  
  const email = ref('')
  const password = ref('')
  const rememberMe = ref(true)
  const error = ref('')
  const loading = ref(false)
  
  const router = useRouter()
  const auth = useAuthStore()
  const toast = useToast()
  
  const handleLogin = async () => {
    error.value = ''
    loading.value = true
    try {
        await auth.login(email.value, password.value, rememberMe.value, toast)
        console.log("✅ Login success, navigating to Home")
        await router.push('/')
    } catch (err) {
        console.error('Login error:', err)
        error.value = 'Invalid credentials'
        toast.error('Login failed: Invalid credentials')
    } finally {
        loading.value = false
    }
  }

  </script>
  