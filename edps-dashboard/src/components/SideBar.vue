<template>
  <aside class="w-64 h-full bg-white shadow-lg flex flex-col justify-between">
    <!-- Header -->
    <div>
      <div class="p-6 border-b border-gray-200">
        <h1 class="text-2xl font-bold text-gray-800">EDPS</h1>
        <p class="text-sm text-gray-500">
          {{ auth.isAdmin ? 'Admin' : 'Advisor' }} Dashboard
        </p>
      </div>

      <!-- Navigation -->
      <nav class="flex flex-col gap-1 p-4 text-gray-700">
        <RouterLink
          to="/"
          class="sidebar-link"
          :class="isActiveExact('/')"
        >
          🏠 Dashboard
        </RouterLink>

        <RouterLink
          to="/students"
          class="sidebar-link"
          :class="isActive('/students')"
        >
          👥 Students
        </RouterLink>

        <RouterLink
          to="/upload"
          class="sidebar-link"
          :class="isActive('/upload')"
        >
          📤 Upload CSV
        </RouterLink>

        <!-- Admin-only -->
        <RouterLink
          v-if="auth.isAdmin"
          to="/admin"
          class="sidebar-link text-red-600 hover:bg-red-50"
          :class="isActive('/admin')"
        >
          🔐 Admin Panel
        </RouterLink>
      </nav>
    </div>

    <!-- Footer: Settings & Logout -->
    <div class="p-4 border-t border-gray-200 flex flex-col gap-2">
      <RouterLink
        to="/settings"
        class="sidebar-link"
        :class="isActive('/settings')"
      >
        ⚙️ Settings
      </RouterLink>

      <button
        @click="handleLogout"
        class="sidebar-link text-left text-sm text-gray-600 hover:bg-gray-100 hover:text-red-600 transition"
      >
        🚪 Logout
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const isActive = (path) => {
  return route.path.startsWith(path)
    ? 'bg-blue-100 font-semibold text-blue-700'
    : ''
}

const isActiveExact = (path) => {
  return route.path === path
    ? 'bg-blue-100 font-semibold text-blue-700'
    : ''
}

const handleLogout = () => {
  auth.logout()
  toast.info('Logged out')
  router.push('/login')
}
</script>

<style scoped>
.sidebar-link {
  @apply block px-4 py-2 rounded text-sm transition hover:bg-blue-50 hover:text-blue-700;
}
</style>
