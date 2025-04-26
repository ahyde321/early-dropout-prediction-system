<template>
  <div class="p-6 md:p-10 space-y-8 bg-gradient-to-b from-gray-50 to-white min-h-screen">
    <!-- Header -->
    <div class="bg-white p-6 md:p-8 rounded-2xl shadow-lg">
      <h1 class="text-3xl md:text-4xl font-extrabold bg-gradient-to-r from-sky-600 to-blue-800 bg-clip-text text-transparent">
        Settings
      </h1>
      <p class="text-gray-500 mt-2">Configure your account and application preferences</p>
    </div>

    <!-- Settings Categories -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6 md:gap-8">
      <!-- Account Settings -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center gap-4 mb-6">
          <div class="p-3 bg-blue-50 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-blue-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
          </div>
          <h2 class="text-xl md:text-2xl font-bold text-gray-800">Account</h2>
        </div>
        
        <div class="space-y-6">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Name</label>
            <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-4">
              <input 
                type="text" 
                v-model="accountSettings.firstName" 
                placeholder="First Name"
                class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
              />
              <input 
                type="text" 
                v-model="accountSettings.lastName" 
                placeholder="Last Name"
                class="flex-1 px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
              />
            </div>
          </div>
          
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Email</label>
            <input 
              type="email" 
              v-model="accountSettings.email" 
              placeholder="Email Address"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 transition-shadow"
            />
          </div>
          
          <div class="pt-4">
            <button 
              @click="saveAccountSettings"
              class="w-full bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 hover:from-blue-700 hover:to-blue-800 transition-colors shadow-sm hover:shadow"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Save Account Changes
            </button>
          </div>
        </div>
      </div>
      
      <!-- Security Settings -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center gap-4 mb-6">
          <div class="p-3 bg-green-50 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-green-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h2 class="text-xl md:text-2xl font-bold text-gray-800">Security</h2>
        </div>
        
        <div class="space-y-6">
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Current Password</label>
            <input 
              type="password" 
              v-model="securitySettings.currentPassword" 
              placeholder="Current Password"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 transition-shadow"
            />
          </div>
          
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">New Password</label>
            <input 
              type="password" 
              v-model="securitySettings.newPassword" 
              placeholder="New Password"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 transition-shadow"
            />
          </div>
          
          <div class="space-y-2">
            <label class="block text-sm font-medium text-gray-700">Confirm New Password</label>
            <input 
              type="password" 
              v-model="securitySettings.confirmPassword" 
              placeholder="Confirm New Password"
              class="w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500 transition-shadow"
            />
          </div>
          
          <div class="pt-4">
            <button 
              @click="changePassword"
              class="w-full bg-gradient-to-r from-green-600 to-green-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 hover:from-green-700 hover:to-green-800 transition-colors shadow-sm hover:shadow"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 7a2 2 0 012 2m4 0a6 6 0 01-7.743 5.743L11 17H9v2H7v2H4a1 1 0 01-1-1v-2.586a1 1 0 01.293-.707l5.964-5.964A6 6 0 1121 9z" />
              </svg>
              Change Password
            </button>
          </div>
        </div>
      </div>
      
      <!-- Notification Settings -->
      <div class="bg-white border border-gray-200 rounded-2xl p-6 md:p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
        <div class="flex items-center gap-4 mb-6">
          <div class="p-3 bg-purple-50 rounded-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-purple-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
            </svg>
          </div>
          <h2 class="text-xl md:text-2xl font-bold text-gray-800">Notifications</h2>
        </div>
        
        <div class="space-y-6">
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-medium text-gray-900">Email Notifications</h3>
              <p class="text-xs text-gray-500">Receive emails about student risk changes</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notificationSettings.emailEnabled" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:translate-x-[-100%] after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-medium text-gray-900">High Risk Alerts</h3>
              <p class="text-xs text-gray-500">Get alerts when students become high risk</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notificationSettings.highRiskAlerts" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:translate-x-[-100%] after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>
          
          <div class="flex items-center justify-between">
            <div>
              <h3 class="text-sm font-medium text-gray-900">System Updates</h3>
              <p class="text-xs text-gray-500">Get notified about system updates</p>
            </div>
            <label class="relative inline-flex items-center cursor-pointer">
              <input type="checkbox" v-model="notificationSettings.systemUpdates" class="sr-only peer">
              <div class="w-11 h-6 bg-gray-200 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-purple-300 rounded-full peer peer-checked:after:translate-x-full rtl:peer-checked:after:translate-x-[-100%] after:content-[''] after:absolute after:top-[2px] after:start-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-purple-600"></div>
            </label>
          </div>
          
          <div class="pt-4">
            <button 
              @click="saveNotificationSettings"
              class="w-full bg-gradient-to-r from-purple-600 to-purple-700 text-white px-6 py-3 rounded-lg font-semibold flex items-center justify-center gap-2 hover:from-purple-700 hover:to-purple-800 transition-colors shadow-sm hover:shadow"
            >
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
              </svg>
              Save Notification Settings
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/authStore'
import { onMounted, ref } from 'vue'
import { useToast } from 'vue-toastification'

const auth = useAuthStore()
const toast = useToast()

// Settings data
const accountSettings = ref({
  firstName: '',
  lastName: '',
  email: ''
})

const securitySettings = ref({
  currentPassword: '',
  newPassword: '',
  confirmPassword: ''
})

const notificationSettings = ref({
  emailEnabled: true,
  highRiskAlerts: true,
  systemUpdates: false
})

// Load user data
onMounted(() => {
  if (auth.user) {
    accountSettings.value.firstName = auth.user.first_name
    accountSettings.value.lastName = auth.user.last_name
    accountSettings.value.email = auth.user.email
  }
  
  // Load notification settings (could come from API)
  loadSettings()
})

async function loadSettings() {
  try {
    // This is just a placeholder - implement actual API call if needed
    // const response = await api.get('/api/settings')
    // notificationSettings.value = response.data.notifications
  } catch (error) {
    console.error('Failed to load settings:', error)
  }
}

async function saveAccountSettings() {
  try {
    const payload = {
      first_name: accountSettings.value.firstName,
      last_name: accountSettings.value.lastName,
      email: accountSettings.value.email
    }
    
    // This is a placeholder - implement actual API call
    // await api.patch('/api/users/profile', payload)
    
    // Update local auth store
    auth.updateUser({
      ...auth.user,
      first_name: accountSettings.value.firstName,
      last_name: accountSettings.value.lastName,
      email: accountSettings.value.email
    })
    
    toast.success('Account settings saved successfully')
  } catch (error) {
    console.error('Failed to save account settings:', error)
    toast.error('Failed to save account settings')
  }
}

async function changePassword() {
  try {
    // Validate passwords
    if (!securitySettings.value.currentPassword) {
      return toast.error('Current password is required')
    }
    
    if (!securitySettings.value.newPassword) {
      return toast.error('New password is required')
    }
    
    if (securitySettings.value.newPassword !== securitySettings.value.confirmPassword) {
      return toast.error('New passwords do not match')
    }
    
    // This is a placeholder - implement actual API call
    // await api.post('/api/users/change-password', {
    //   current_password: securitySettings.value.currentPassword,
    //   new_password: securitySettings.value.newPassword
    // })
    
    // Clear form
    securitySettings.value.currentPassword = ''
    securitySettings.value.newPassword = ''
    securitySettings.value.confirmPassword = ''
    
    toast.success('Password changed successfully')
  } catch (error) {
    console.error('Failed to change password:', error)
    toast.error('Failed to change password')
  }
}

async function saveNotificationSettings() {
  try {
    // This is a placeholder - implement actual API call
    // await api.patch('/api/settings/notifications', notificationSettings.value)
    
    toast.success('Notification settings saved successfully')
  } catch (error) {
    console.error('Failed to save notification settings:', error)
    toast.error('Failed to save notification settings')
  }
}
</script> 