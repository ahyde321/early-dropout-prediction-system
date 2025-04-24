<template>
  <aside class="w-64 h-full bg-white border-r border-gray-200 flex flex-col shadow-sm">
    <!-- Header -->
    <div class="p-6">
      <div class="flex items-center gap-3 mb-2">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-blue-500 via-blue-600 to-blue-700 flex items-center justify-center text-white shadow-lg shadow-blue-200 ring-4 ring-blue-50">
          <GraduationCap size="20" strokeWidth={1.5} />
        </div>
        <div>
          <h1 class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent tracking-tight">
            EDPS
          </h1>
          <p class="text-sm font-medium text-gray-500">
            {{ auth.isAdmin ? 'Admin' : 'Advisor' }} Portal
          </p>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 px-3">
      <!-- Main Navigation -->
      <div class="space-y-1">
        <div class="mb-2 px-3">
          <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Main</h2>
        </div>
        
        <RouterLink
          to="/"
          class="nav-link group"
          :class="isActiveExact('/')"
        >
          <LayoutDashboard
            size="18"
            :class="isActiveExact('/') ? 'text-blue-600' : 'text-gray-500 group-hover:text-blue-600'"
          />
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink
          to="/students"
          class="nav-link group"
          :class="isActive('/students')"
        >
          <Users
            size="18"
            :class="isActive('/students') ? 'text-blue-600' : 'text-gray-500 group-hover:text-blue-600'"
          />
          <span>Students</span>
        </RouterLink>

        <RouterLink
          to="/upload"
          class="nav-link group"
          :class="isActive('/upload')"
        >
          <Upload
            size="18"
            :class="isActive('/upload') ? 'text-blue-600' : 'text-gray-500 group-hover:text-blue-600'"
          />
          <span>Upload CSV</span>
        </RouterLink>
      </div>

      <!-- Admin Section -->
      <template v-if="auth.isAdmin">
        <div class="my-6">
          <div class="h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent opacity-75"></div>
        </div>
        <div class="space-y-1">
          <div class="mb-2 px-3">
            <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Administration</h2>
          </div>
          <RouterLink
            to="/admin"
            class="nav-link group"
            :class="isActive('/admin')"
          >
            <ShieldCheck
              size="18"
              :class="isActive('/admin') ? 'text-blue-600' : 'text-gray-500 group-hover:text-blue-600'"
            />
            <span>Admin Panel</span>
          </RouterLink>
        </div>
      </template>
    </nav>

    <!-- Footer: Settings & Logout -->
    <div class="p-3 border-t border-gray-100 space-y-1 bg-gray-50/50">
      <div class="mb-2 px-3">
        <h2 class="text-xs font-semibold text-gray-400 uppercase tracking-wider">Account</h2>
      </div>
      <RouterLink
        to="/settings"
        class="nav-link group"
        :class="isActive('/settings')"
      >
        <Settings
          size="18"
          :class="isActive('/settings') ? 'text-blue-600' : 'text-gray-500 group-hover:text-blue-600'"
        />
        <span>Settings</span>
      </RouterLink>

      <button
        @click="handleLogout"
        class="nav-link group w-full"
      >
        <LogOut
          size="18"
          class="text-gray-500 group-hover:text-red-600 transition-colors"
        />
        <span class="group-hover:text-red-600 transition-colors">Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/authStore'
import { useToast } from 'vue-toastification'
import {
  GraduationCap,
  LayoutDashboard,
  Users,
  Upload,
  ShieldCheck,
  Settings,
  LogOut
} from 'lucide-vue-next'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const isActive = (path) => {
  return route.path.startsWith(path)
    ? 'bg-blue-50/80 text-blue-700 font-medium'
    : ''
}

const isActiveExact = (path) => {
  return route.path === path
    ? 'bg-blue-50/80 text-blue-700 font-medium'
    : ''
}

const handleLogout = () => {
  auth.logout()
  toast.info('Logged out')
  router.push('/login')
}
</script>

<style scoped>
.nav-link {
  @apply flex items-center gap-3 px-3 py-2 text-sm text-gray-600 rounded-lg transition-all duration-200;
  @apply hover:bg-blue-50/60 hover:text-blue-700;
}
</style>