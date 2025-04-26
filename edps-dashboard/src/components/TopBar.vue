<template>
  <header class="bg-white border-b border-gray-200 px-6 py-3 flex items-center justify-between">
    <!-- Left Section: Title and Breadcrumb -->
    <div class="flex items-center space-x-6">
      <h1 class="text-lg font-semibold text-gray-900">
        Early Dropout Prediction System
      </h1>

      <nav class="flex items-center space-x-2 text-sm text-gray-500">
        <span>{{ currentSection }}</span>
        <ChevronRight v-if="subSection" class="w-4 h-4" />
        <span v-if="subSection" class="text-gray-900 font-medium">{{ subSection }}</span>
      </nav>
    </div>

    <!-- Right Section: Actions and User Info -->
    <div class="flex items-center space-x-6">
      <!-- Quick Actions -->
      <div class="flex items-center space-x-2">
        <button 
          class="p-2 text-gray-500 hover:text-blue-700 hover:bg-blue-50/80 rounded-lg transition-colors relative"
          @click="refreshDashboard"
          :disabled="isRefreshing"
          :class="{ 'cursor-not-allowed opacity-50': isRefreshing }"
        >
          <RefreshCw size="18" :class="{ 'animate-spin': isRefreshing }" />
          <span v-if="refreshError" class="absolute -top-2 -right-2 w-2 h-2 bg-red-600 rounded-full"></span>
        </button>

        <!-- Notifications Button & Dropdown -->
        <div class="relative">
          <button 
            class="p-2 text-gray-500 hover:text-blue-700 hover:bg-blue-50/80 rounded-lg transition-colors"
            @click="toggleNotifications"
            ref="notificationTrigger"
          >
            <div class="relative">
              <Bell size="18" />
              <span 
                v-if="notifications.unread.length" 
                class="absolute -top-1 -right-1 w-4 h-4 bg-red-600 text-white text-xs flex items-center justify-center rounded-full font-medium"
              >
                {{ notifications.unread.length }}
              </span>
            </div>
          </button>

          <!-- Notifications Panel -->
          <div
            v-if="showNotifications"
            class="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border border-gray-200 py-2 z-50"
            ref="notificationPanel"
          >
            <div class="px-4 py-2 border-b border-gray-200 flex justify-between items-center">
              <h3 class="font-medium text-gray-900">Notifications</h3>
              <button 
                v-if="notifications.unread.length"
                @click="markAllAsRead"
                class="text-xs text-blue-700 hover:text-blue-800"
              >
                Mark all as read
              </button>
            </div>

            <div class="max-h-96 overflow-y-auto">
              <template v-if="allNotifications.length">
                <div
                  v-for="notification in allNotifications"
                  :key="notification.id"
                  class="px-4 py-3 hover:bg-gray-50/80 border-b border-gray-200 last:border-0"
                  :class="{ 'bg-blue-50/80': !notification.read }"
                >
                  <div class="flex items-start gap-3">
                    <div 
                      class="p-1 rounded-full"
                      :class="notificationTypeStyles[notification.type]"
                    >
                      <component :is="notificationIcons[notification.type]" size="14" />
                    </div>
                    <div>
                      <p class="text-sm text-gray-900 font-medium">{{ notification.title }}</p>
                      <p class="text-xs text-gray-600 mt-0.5">{{ notification.message }}</p>
                      <div class="flex items-center gap-2 mt-2">
                        <span class="text-xs text-gray-500">{{ formatTime(notification.timestamp) }}</span>
                        <button 
                          v-if="!notification.read"
                          @click="markAsRead(notification.id)"
                          class="text-xs text-blue-700 hover:text-blue-800"
                        >
                          Mark as read
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
              <div v-else class="px-4 py-6 text-center text-gray-500 text-sm">
                No notifications
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- User Info -->
      <div class="flex items-center space-x-3">
        <div class="text-right">
          <p class="text-sm font-medium text-gray-900">{{ auth.user?.name || 'User' }}</p>
          <p class="text-xs text-gray-600">{{ auth.isAdmin ? 'Administrator' : 'Advisor' }}</p>
        </div>
        <div class="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center text-white shadow-sm font-semibold text-sm">
          {{ userInitials }}
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import { format, isToday, isYesterday } from 'date-fns'
import { AlertTriangle, Bell, CheckCircle, ChevronRight, Info, RefreshCw } from 'lucide-vue-next'
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

const route = useRoute()
const auth = useAuthStore()
const toast = useToast()

// State
const isRefreshing = ref(false)
const refreshError = ref(false)
const showNotifications = ref(false)
const notificationTrigger = ref(null)
const notificationPanel = ref(null)

// Notifications System
const notifications = ref({
  unread: [
    {
      id: 1,
      type: 'alert',
      title: 'High Risk Alert',
      message: '3 students have moved to high risk category',
      timestamp: new Date(Date.now() - 1000 * 60 * 30), // 30 minutes ago
      read: false
    },
    {
      id: 2,
      type: 'info',
      title: 'New Data Available',
      message: 'Latest student performance data has been processed',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 2), // 2 hours ago
      read: false
    }
  ],
  read: [
    {
      id: 3,
      type: 'success',
      title: 'Upload Successful',
      message: 'Student data has been successfully uploaded',
      timestamp: new Date(Date.now() - 1000 * 60 * 60 * 24), // 1 day ago
      read: true
    }
  ]
})

const notificationTypeStyles = {
  alert: 'bg-amber-100 text-amber-700',
  info: 'bg-blue-100 text-blue-700',
  success: 'bg-green-100 text-green-700'
}

const notificationIcons = {
  alert: AlertTriangle,
  info: Info,
  success: CheckCircle
}

// Computed
const currentSection = computed(() => {
  const pathMap = {
    '/': 'Dashboard',
    '/students': 'Students',
    '/upload': 'Upload Data',
    '/admin': 'Administration',
    '/settings': 'Settings'
  }
  return pathMap[route.path.split('/').slice(0, 2).join('/')] || 'Dashboard'
})

const subSection = computed(() => {
  if (route.name === 'StudentDetails') {
    return 'Student Details'
  }
  return ''
})

const userInitials = computed(() => {
  const name = auth.user?.name || 'User Name'
  return name
    .split(' ')
    .map(n => n[0])
    .join('')
    .toUpperCase()
    .slice(0, 2)
})

const allNotifications = computed(() => {
  return [...notifications.value.unread, ...notifications.value.read]
    .sort((a, b) => b.timestamp - a.timestamp)
})

// Methods
const refreshDashboard = async () => {
  if (isRefreshing.value) return

  isRefreshing.value = true
  refreshError.value = false
  
  try {
    // Emit refresh event to parent
    emit('refresh')
    await new Promise(resolve => setTimeout(resolve, 1000)) // Simulated delay
    toast.success('Dashboard refreshed successfully')
  } catch (error) {
    console.error('Failed to refresh dashboard:', error)
    refreshError.value = true
    toast.error('Failed to refresh dashboard')
  } finally {
    isRefreshing.value = false
  }
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
}

const markAsRead = (id) => {
  const notification = notifications.value.unread.find(n => n.id === id)
  if (notification) {
    notification.read = true
    notifications.value.read.push(notification)
    notifications.value.unread = notifications.value.unread.filter(n => n.id !== id)
  }
}

const markAllAsRead = () => {
  notifications.value.unread.forEach(notification => {
    notification.read = true
    notifications.value.read.push(notification)
  })
  notifications.value.unread = []
}

const formatTime = (timestamp) => {
  if (isToday(timestamp)) {
    return `Today at ${format(timestamp, 'h:mm a')}`
  } else if (isYesterday(timestamp)) {
    return `Yesterday at ${format(timestamp, 'h:mm a')}`
  } else {
    return format(timestamp, 'MMM d, yyyy')
  }
}

// Click outside handler for notifications panel
const handleClickOutside = (event) => {
  if (
    showNotifications.value &&
    !notificationTrigger.value?.contains(event.target) &&
    !notificationPanel.value?.contains(event.target)
  ) {
    showNotifications.value = false
  }
}

// Lifecycle hooks
onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})

// Event emitter
const emit = defineEmits(['refresh'])
</script>

<style scoped>
/* Add any additional styles here */
</style>