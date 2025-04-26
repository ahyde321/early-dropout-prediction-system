<template>
  <header class="relative bg-white border-b border-gray-100 shadow-sm z-10">
    <div class="px-4 sm:px-6 lg:px-8 w-full">
      <div class="flex justify-between items-center h-16 mx-auto max-w-full">
        <!-- Logo in the left corner with margin -->
        <div class="flex-shrink-0 flex items-center ml-2 sm:ml-4">
          <router-link to="/" class="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600 flex items-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 mr-2 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10.394 2.08a1 1 0 00-.788 0l-7 3a1 1 0 000 1.84L5.25 8.051a.999.999 0 01.356-.257l4-1.714a1 1 0 11.788 1.838L7.667 9.088l1.94.831a1 1 0 00.787 0l7-3a1 1 0 000-1.838l-7-3zM3.31 9.397L5 10.12v4.102a8.969 8.969 0 00-1.05-.174 1 1 0 01-.89-.89 11.115 11.115 0 01.25-3.762zM9.3 16.573A9.026 9.026 0 007 14.935v-3.957l1.818.78a3 3 0 002.364 0l5.508-2.361a11.026 11.026 0 01.25 3.762 1 1 0 01-.89.89 8.968 8.968 0 00-5.35 2.524 1 1 0 01-1.4 0zM6 18a1 1 0 001-1v-2.065a8.935 8.935 0 00-2-.712V17a1 1 0 001 1z" />
            </svg>
            <span class="hidden sm:inline">Early Dropout Prediction System</span>
            <span class="sm:hidden">EDPS</span>
          </router-link>
        </div>

        <!-- Right aligned elements with margin -->
        <div class="flex items-center space-x-4 sm:space-x-6 mr-2 sm:mr-4">
          <!-- Notification Bell -->
          <div class="relative notification-menu">
            <button 
              @click="toggleNotifications" 
              class="relative inline-flex items-center p-2 border border-transparent rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              
              <!-- Notification Badge -->
              <span 
                v-if="unreadNotifications.length > 0" 
                class="absolute -top-1 -right-1 inline-flex items-center justify-center px-2 py-1 text-xs font-bold leading-none text-white transform translate-x-1/2 -translate-y-1/2 bg-red-500 rounded-full"
              >
                {{ unreadNotifications.length }}
              </span>
            </button>
            
            <!-- Notifications Dropdown -->
            <div 
              v-if="showNotifications" 
              class="origin-top-right absolute right-0 mt-2 w-96 rounded-xl shadow-lg bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10 max-h-96 overflow-y-auto"
            >
              <div class="p-3 border-b border-gray-100 flex justify-between items-center">
                <h3 class="text-sm font-semibold text-gray-700">Notifications</h3>
                <div class="flex space-x-3">
                  <button 
                    v-if="unreadNotifications.length > 0"
                    @click="markAllAsRead" 
                    class="text-xs text-blue-600 hover:text-blue-800"
                  >
                    Mark all as read
                  </button>
                  <button 
                    v-if="notifications.length > 0"
                    @click="clearAllNotifications" 
                    class="text-xs text-red-600 hover:text-red-800"
                  >
                    Clear all
                  </button>
                </div>
              </div>
              
              <div v-if="notifications.length === 0" class="p-4 text-center text-gray-500 text-sm">
                No notifications yet
              </div>
              
              <div v-else>
                <a 
                  v-for="notification in notifications" 
                  :key="notification.id" 
                  class="block p-4 hover:bg-gray-50 transition-colors duration-150 relative"
                  :class="{ 'bg-blue-50': !notification.read }"
                >
                  <div class="flex items-start pr-8">
                    <div class="flex-shrink-0 mr-3">
                      <div class="w-8 h-8 rounded-full bg-blue-100 text-blue-500 flex items-center justify-center">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                        </svg>
                      </div>
                    </div>
                    <div @click.prevent="handleNotification(notification)" class="cursor-pointer flex-grow">
                      <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
                      <p class="text-xs text-gray-500 mt-1">{{ notification.message }}</p>
                      <p class="text-xs text-gray-400 mt-1">{{ formatDate(notification.timestamp) }}</p>
                    </div>
                    <button 
                      @click.stop="deleteNotification(notification)" 
                      class="absolute top-4 right-4 text-gray-400 hover:text-red-500 transition-colors"
                      title="Delete notification"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                      </svg>
                    </button>
                  </div>
                </a>
              </div>
            </div>
          </div>
          
          <!-- Refresh Button -->
          <button 
            @click="refreshData" 
            class="relative inline-flex items-center p-2 border border-transparent rounded-full bg-blue-50 text-blue-600 hover:bg-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
            :class="{ 'animate-spin': isRefreshing }"
          >
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
          </button>

          <!-- User Account Dropdown -->
          <div class="relative user-menu">
            <div>
              <button 
                @click="toggleUserMenu" 
                type="button" 
                class="flex items-center space-x-3 bg-white rounded-full py-1.5 px-3 shadow-sm border border-gray-100 hover:border-gray-200 hover:shadow-md transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <div class="flex-shrink-0 h-8 w-8 rounded-full bg-gradient-to-r from-blue-400 to-purple-500 flex items-center justify-center text-white text-sm font-bold uppercase">
                  {{ userInitials }}
                </div>
                <div class="hidden sm:block text-left">
                  <div class="text-sm font-medium text-gray-700">{{ nameDisplay }}</div>
                  <div v-if="user.role" class="text-xs text-gray-500">{{ user.role }}</div>
                </div>
                <svg class="h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd" />
                </svg>
              </button>
            </div>

            <div 
              v-if="showUserMenu" 
              class="origin-top-right absolute right-0 mt-2 w-48 rounded-xl shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none z-10"
            >
              <div class="block px-4 py-2 text-xs text-gray-400 border-b border-gray-100">
                Manage Account
              </div>
              <router-link 
                v-if="userIsAdmin" 
                to="/admin" 
                class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-50 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-gray-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-6-3a2 2 0 11-4 0 2 2 0 014 0zm-2 4a5 5 0 00-4.546 2.916A5.986 5.986 0 0010 16a5.986 5.986 0 004.546-2.084A5 5 0 0010 11z" clip-rule="evenodd" />
                </svg>
                Admin Panel
              </router-link>
              <a 
                href="#" 
                @click.prevent="logout" 
                class="block px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 001 1h12a1 1 0 001-1V7.414l-5.293-5.293A1 1 0 0010 2H3zm9 2a1 1 0 00-1-1H3.5a.5.5 0 00-.5.5v11a.5.5 0 00.5.5h11a.5.5 0 00.5-.5V6a1 1 0 00-1-1H12z" clip-rule="evenodd" />
                </svg>
                Logout
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuth } from '@/composables/useAuth';
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue';
import { useRouter } from 'vue-router';
import { useToast } from 'vue-toastification';

const router = useRouter()
const toast = useToast()
const { user, logout: authLogout } = useAuth()

const showUserMenu = ref(false)
const isRefreshing = ref(false)
const showNotifications = ref(false)
const notifications = ref([
  {
    id: 1,
    title: 'Student risk update',
    message: 'John Doe has been flagged as high risk',
    timestamp: new Date(Date.now() - 3600000), // 1 hour ago
    read: false,
    link: '/students/1'
  },
  {
    id: 2,
    title: 'New prediction',
    message: 'Jane Smith has a new risk prediction',
    timestamp: new Date(Date.now() - 86400000), // 1 day ago
    read: false,
    link: '/students/2'
  },
  {
    id: 3,
    title: 'System update',
    message: 'Dashboard has been updated to version 2.1',
    timestamp: new Date(Date.now() - 259200000), // 3 days ago
    read: true,
    link: null
  }
])

const unreadNotifications = computed(() => {
  return notifications.value.filter(n => !n.read)
})

const userIsAdmin = computed(() => {
  return user.value?.role === 'admin'
})

const nameDisplay = computed(() => {
  if (!user.value) return 'Loading...'
  return `${user.value.first_name} ${user.value.last_name}`
})

const userInitials = computed(() => {
  if (!user.value) return 'U'
  return (user.value.first_name?.charAt(0) || '') + (user.value.last_name?.charAt(0) || '')
})

const toggleUserMenu = () => {
  showUserMenu.value = !showUserMenu.value
  if (showUserMenu.value) {
    showNotifications.value = false
  }
}

const toggleNotifications = () => {
  showNotifications.value = !showNotifications.value
  if (showNotifications.value) {
    showUserMenu.value = false
  }
}

const refreshData = async () => {
  isRefreshing.value = true
  
  try {
    // Trigger a page refresh
    window.location.reload()
  } catch (error) {
    toast.error('Failed to refresh data')
    isRefreshing.value = false
  }
}

const logout = async () => {
  try {
    await authLogout()
    showUserMenu.value = false
    router.push('/login')
    toast.success('Successfully logged out')
  } catch (error) {
    toast.error('Failed to log out')
  }
}

const formatDate = (date) => {
  const now = new Date()
  const diff = now - new Date(date)
  
  // Less than a day
  if (diff < 86400000) {
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  }
  
  // Less than a week
  if (diff < 604800000) {
    const days = Math.floor(diff / 86400000)
    return `${days} ${days === 1 ? 'day' : 'days'} ago`
  }
  
  // More than a week
  return new Date(date).toLocaleDateString()
}

const handleNotification = (notification) => {
  // Mark as read
  notification.read = true
  
  // Navigate to link if present
  if (notification.link) {
    router.push(notification.link)
    showNotifications.value = false
  }
}

const markAllAsRead = () => {
  notifications.value.forEach(notification => {
    notification.read = true
  })
  toast.success('All notifications marked as read')
}

const deleteNotification = (notification) => {
  const index = notifications.value.findIndex(n => n.id === notification.id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
    toast.success('Notification deleted')
  }
}

const clearAllNotifications = () => {
  notifications.value = []
  toast.success('All notifications cleared')
}

// Close menus when clicking outside
const closeMenuOnOutsideClick = (event) => {
  const userMenu = document.querySelector('.user-menu')
  const notificationMenu = document.querySelector('.notification-menu')
  
  if (userMenu && !userMenu.contains(event.target)) {
    showUserMenu.value = false
  }
  
  if (notificationMenu && !notificationMenu.contains(event.target)) {
    showNotifications.value = false
  }
}

// Add event listener for outside clicks
onMounted(() => {
  document.addEventListener('click', closeMenuOnOutsideClick)
})

// Clean up event listener
onBeforeUnmount(() => {
  document.removeEventListener('click', closeMenuOnOutsideClick)
})

// Watch for menu changes
watch([showUserMenu, showNotifications], ([isUserMenuOpen, isNotificationsOpen]) => {
  if (isUserMenuOpen) {
    showNotifications.value = false
  }
  if (isNotificationsOpen) {
    showUserMenu.value = false
  }
})
</script>

<style scoped>
.user-menu, .notification-menu {
  position: relative;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.animate-spin {
  animation: spin 1s linear infinite;
}
</style>