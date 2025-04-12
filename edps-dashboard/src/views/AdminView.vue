<template>
    <div class="p-6 space-y-8">
      <h1 class="text-2xl font-bold text-gray-800">Admin Dashboard</h1>
  
      <!-- Invite/Register New User -->
      <section class="bg-white shadow-md rounded-lg p-4 border border-gray-200">
        <h2 class="text-lg font-semibold mb-4">Register New User</h2>
        <form @submit.prevent="registerUser" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <input v-model="newUser.first_name" type="text" placeholder="First Name" required class="input" />
          <input v-model="newUser.last_name" type="text" placeholder="Last Name" required class="input" />
          <input v-model="newUser.email" type="email" placeholder="Email" required class="input" />
          <input v-model="newUser.password" type="password" placeholder="Password" required class="input" />
          <select v-model="newUser.role" class="input">
            <option value="advisor">Advisor</option>
            <option value="admin">Admin</option>
          </select>
          <button type="submit" class="btn col-span-1 md:col-span-2">Register</button>
        </form>
      </section>
  
      <!-- User Management Table -->
      <section class="bg-white shadow-md rounded-lg p-4 border border-gray-200">
        <h2 class="text-lg font-semibold mb-4">Manage Users</h2>
        <table class="w-full text-left text-sm">
          <thead>
            <tr class="border-b">
              <th class="py-2 px-4">Name</th>
              <th class="py-2 px-4">Email</th>
              <th class="py-2 px-4">Role</th>
              <th class="py-2 px-4">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id" class="border-t">
              <td class="py-2 px-4">{{ user.first_name }} {{ user.last_name }}</td>
              <td class="py-2 px-4">{{ user.email }}</td>
              <td class="py-2 px-4">
                <select v-model="user.role" @change="updateRole(user)" class="input">
                  <option value="advisor">Advisor</option>
                  <option value="admin">Admin</option>
                </select>
              </td>
              <td class="py-2 px-4">
                <button @click="deactivateUser(user)" class="text-red-500 hover:underline text-sm">Deactivate</button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted } from 'vue'
  import api from '@/services/api'
  import { useToast } from 'vue-toastification'
  
  const toast = useToast()
  const users = ref([])
  const newUser = ref({
    first_name: '',
    last_name: '',
    email: '',
    password: '',
    role: 'advisor',
  })
  
  const fetchUsers = async () => {
    try {
      const res = await api.get('/admin/users')
      users.value = res.data
    } catch (err) {
      toast.error('Failed to load users')
    }
  }
  
  const updateRole = async (user) => {
    try {
      await api.post('/auth/set-role', {
        user_id: user.id,
        role: user.role,
      })
      toast.success(`Updated ${user.email} to ${user.role}`)
    } catch (err) {
      toast.error('Failed to update role')
    }
  }
  
  const deactivateUser = async (user) => {
    try {
      await api.post('/admin/deactivate', { user_id: user.id })
      toast.info(`Deactivated ${user.email}`)
      fetchUsers()
    } catch (err) {
      toast.error('Failed to deactivate user')
    }
  }
  
  const registerUser = async () => {
    try {
      await api.post('/auth/register', newUser.value)
      toast.success('User registered')
      newUser.value = { first_name: '', last_name: '', email: '', password: '', role: 'advisor' }
      fetchUsers()
    } catch (err) {
      toast.error('Failed to register user')
    }
  }
  
  onMounted(fetchUsers)
  </script>
  
  <style scoped>
  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-300;
  }
  .btn {
    @apply bg-sky-500 text-white py-2 px-4 rounded hover:bg-sky-600 transition;
  }
  </style>