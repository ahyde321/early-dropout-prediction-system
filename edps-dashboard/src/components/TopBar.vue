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
                v-if="unreadCount > 0" 
                class="absolute -top-1 -right-1 w-4 h-4 bg-red-600 text-white text-xs flex items-center justify-center rounded-full font-medium"
              >
                {{ unreadCount }}
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
                v-if="unreadCount > 0"
                @click="markAllAsRead"
                class="text-xs text-blue-700 hover:text-blue-800"
              >
                Mark all as read
              </button>
            </div>

            <div class="max-h-96 overflow-y-auto">
              <template v-if="notifications.length">
                <div
                  v-for="notification in notifications"
                  :key="notification.id"
                  class="px-4 py-3 hover:bg-gray-50/80 border-b border-gray-200 last:border-0"
                  :class="{ 'bg-blue-50/80': !notification.read }"
                >
                  <div class="flex items-start gap-3">
                    <div 
                      class="p-1 rounded-full"
                      :class="notificationTypeStyles[notification.type] || 'bg-gray-100 text-gray-700'"
                    >
                      <component 
                        :is="notificationIcons[notification.type] || Info" 
                        size="14" 
                      />
                    </div>
                    <div>
                      <p class="text-sm text-gray-900 font-medium">{{ notification.title || 'Notification' }}</p>
                      <p class="text-xs text-gray-600 mt-0.5">{{ notification.message || '' }}</p>
                      <div class="flex items-center gap-2 mt-2">
                        <span class="text-xs text-gray-500">{{ formatTime(notification.timestamp || notification.created_at) }}</span>
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
          <p class="text-sm font-medium text-gray-900">{{ userFullName }}</p>
          <p class="text-xs text-gray-600">{{ userRole }}</p>
        </div>
        <div class="w-8 h-8 rounded-full bg-blue-700 flex items-center justify-center text-white shadow-sm font-semibold text-sm">
          {{ userInitials }}
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import api from '@/services/api'
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
const notifications = ref([])

// Notification types and styles
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

const userFullName = computed(() => {
  if (!auth.user) return 'User'
  return `${auth.user.first_name} ${auth.user.last_name}`
})

const userRole = computed(() => {
  if (!auth.user) return 'User'
  return auth.user.role === 'admin' ? 'Administrator' : 'Advisor'
})

const userInitials = computed(() => {
  if (!auth.user) return 'U'
  return `${auth.user.first_name[0]}${auth.user.last_name[0]}`.toUpperCase()
})

const unreadCount = computed(() => {
  if (!notifications.value || !Array.isArray(notifications.value)) {
    return 0;
  }
  return notifications.value.filter(n => n && !n.read).length;
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

const markAsRead = async (id) => {
  try {
    await api.patch(`/notifications/${id}/read`)
    const notification = notifications.value.find(n => n.id === id)
    if (notification) {
      notification.read = true
    }
  } catch (error) {
    console.error('Failed to mark notification as read:', error)
    toast.error('Failed to mark notification as read')
  }
}

const markAllAsRead = async () => {
  try {
    await api.patch('/notifications/read-all')
    notifications.value.forEach(notification => {
      notification.read = true
    })
  } catch (error) {
    console.error('Failed to mark all notifications as read:', error)
    toast.error('Failed to mark all notifications as read')
  }
}

const formatTime = (timestamp) => {
  if (!timestamp) return 'Unknown time';
  
  try {
    const date = new Date(timestamp);
    // Check if date is valid
    if (isNaN(date.getTime())) {
      return 'Invalid date';
    }
    
    if (isToday(date)) {
      return `Today at ${format(date, 'h:mm a')}`;
    } else if (isYesterday(date)) {
      return `Yesterday at ${format(date, 'h:mm a')}`;
    } else {
      return format(date, 'MMM d, yyyy');
    }
  } catch (error) {
    console.error('Date formatting error:', error);
    return 'Invalid date';
  }
}

const fetchNotifications = async () => {
  try {
    const { data } = await api.get('/notifications');
    console.log('Raw notifications data:', data);
    
    // Process the notifications to ensure they have all required fields
    notifications.value = data.map(notification => ({
      ...notification,
      // Ensure all required properties exist
      id: notification.id,
      title: notification.title || 'No Title',
      message: notification.message || 'No Message',
      type: notification.type || 'info',
      read: Boolean(notification.read),
      created_at: notification.created_at || new Date().toISOString(),
      // Add a timestamp property if it doesn't exist (for compatibility with the UI)
      timestamp: notification.created_at || new Date().toISOString()
    }));
    
    console.log('Processed notifications:', notifications.value);
  } catch (error) {
    console.error('Failed to fetch notifications:', error);
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
  fetchNotifications()
  // Set up polling for new notifications
  const pollInterval = setInterval(fetchNotifications, 30000) // Poll every 30 seconds
  onUnmounted(() => {
    document.removeEventListener('click', handleClickOutside)
    clearInterval(pollInterval)
  })
})

// Event emitter
const emit = defineEmits(['refresh'])
</script>

<style scoped>
/* Add any additional styles here */
</style>