<template>
  <aside class="w-64 h-full bg-gradient-to-b from-gray-50 to-white border-r border-gray-200 flex flex-col shadow-md">
    <!-- Header with gradient -->
    <div class="p-6 bg-gradient-to-r from-blue-600 to-purple-600 text-white">
      <div class="flex items-center gap-3 mb-1">
        <div class="w-10 h-10 rounded-xl bg-white/20 backdrop-blur-sm flex items-center justify-center text-white shadow-lg">
          <GraduationCap size="22" />
        </div>
        <div>
          <h1 class="text-xl font-bold tracking-tight">
            EDPS
          </h1>
          <p class="text-sm font-medium text-white/80">
            {{ auth.isAdmin ? 'Admin' : 'Advisor' }} Portal
          </p>
        </div>
      </div>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 p-4 space-y-6 overflow-y-auto">
      <!-- Main Navigation -->
      <div>
        <div class="mb-3 px-3">
          <h2 class="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-2 text-blue-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h7" />
            </svg>
            Main Navigation
          </h2>
        </div>
        
        <RouterLink
          to="/"
          class="nav-link group"
          :class="isActiveExact('/')"
          title="Dashboard"
        >
          <div class="icon-wrapper" :class="isActiveExact('/') ? 'icon-active' : ''">
            <LayoutDashboard size="18" />
          </div>
          <span>Dashboard</span>
        </RouterLink>

        <RouterLink
          to="/students"
          class="nav-link group"
          :class="isActive('/students')"
          title="Students"
        >
          <div class="icon-wrapper" :class="isActive('/students') ? 'icon-active' : ''">
            <Users size="18" />
          </div>
          <span>Students</span>
        </RouterLink>

        <RouterLink
          to="/predictions"
          class="nav-link group"
          :class="isActive('/predictions')"
          title="Predictions"
        >
          <div class="icon-wrapper" :class="isActive('/predictions') ? 'icon-active' : ''">
            <BarChart2 size="18" />
          </div>
          <span>Predictions</span>
        </RouterLink>

        <RouterLink
          to="/upload"
          class="nav-link group"
          :class="isActive('/upload')"
          title="Upload"
        >
          <div class="icon-wrapper" :class="isActive('/upload') ? 'icon-active' : ''">
            <Upload size="18" />
          </div>
          <span>Upload</span>
        </RouterLink>
      </div>

      <!-- Admin Section -->
      <template v-if="auth.isAdmin">
        <div>
          <div class="h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent my-2"></div>
        </div>
        <div>
          <div class="mb-3 px-3">
            <h2 class="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-2 text-purple-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              Administration
            </h2>
          </div>
          
          <RouterLink
            to="/admin"
            class="nav-link group"
            :class="isActive('/admin')"
            title="Admin Panel"
          >
            <div class="icon-wrapper" :class="isActive('/admin') ? 'icon-active' : ''">
              <ShieldCheck size="18" />
            </div>
            <span>Admin Panel</span>
          </RouterLink>
        </div>
      </template>
    </nav>

    <!-- Footer: Settings & Logout -->
    <div class="p-4 border-t border-gray-200 space-y-2 bg-gray-50">
      <div class="mb-2 px-3">
        <h2 class="text-xs font-bold text-gray-500 uppercase tracking-wider flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5 mr-2 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
          </svg>
          Account
        </h2>
      </div>
      
      <RouterLink
        to="/settings"
        class="nav-link group"
        :class="isActive('/settings')"
        title="Settings"
      >
        <div class="icon-wrapper" :class="isActive('/settings') ? 'icon-active' : ''">
          <Settings size="18" />
        </div>
        <span>Settings</span>
      </RouterLink>

      <button
        @click="handleLogout"
        class="nav-link group w-full hover:bg-red-50"
        title="Logout"
      >
        <div class="icon-wrapper logout">
          <LogOut size="18" />
        </div>
        <span>Logout</span>
      </button>
    </div>
  </aside>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import {
    BarChart2,
    GraduationCap,
    LayoutDashboard,
    LogOut,
    Settings,
    ShieldCheck,
    Upload,
    Users
} from 'lucide-vue-next'
import { useRoute, useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const toast = useToast()

const isActive = (path) => {
  return route.path.startsWith(path)
    ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 font-medium shadow-sm'
    : ''
}

const isActiveExact = (path) => {
  return route.path === path
    ? 'bg-gradient-to-r from-blue-50 to-indigo-50 text-blue-700 font-medium shadow-sm'
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
  @apply flex items-center gap-3 px-3 py-2.5 text-sm text-gray-700 rounded-lg transition-all duration-200;
  @apply hover:bg-blue-50/70 hover:text-blue-700;
}

.icon-wrapper {
  @apply p-1.5 rounded-md bg-gray-100 text-gray-500 transition-all duration-200;
  @apply group-hover:bg-blue-100 group-hover:text-blue-600;
}

.icon-active {
  @apply bg-blue-100 text-blue-600;
}

.logout {
  @apply group-hover:bg-red-100 group-hover:text-red-600;
}

/* Improved scrollbar */
nav::-webkit-scrollbar {
  width: 4px;
}

nav::-webkit-scrollbar-track {
  background: transparent;
}

nav::-webkit-scrollbar-thumb {
  background: #e5e7eb;
  border-radius: 2px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: #d1d5db;
}
</style>