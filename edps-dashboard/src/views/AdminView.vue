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
                <span :class="{
                  'px-2 py-1 rounded-full text-xs font-medium': true,
                  'bg-blue-100 text-blue-800': user.role === 'admin',
                  'bg-green-100 text-green-800': user.role === 'advisor'
                }">
                  {{ user.role }}
                </span>
              </td>
              <td class="py-2 px-4 flex items-center gap-2">
                <button @click="confirmDelete(user)" class="action-btn delete-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Delete
                </button>
                <button @click="startEdit(user)" class="action-btn edit-btn">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                  </svg>
                  Edit
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </section>

      <!-- Edit User Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
          <h3 class="text-lg font-semibold mb-4">Edit User</h3>
          <form @submit.prevent="saveEdit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700">First Name</label>
              <input v-model="editingUser.first_name" type="text" class="input" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Last Name</label>
              <input v-model="editingUser.last_name" type="text" class="input" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Email</label>
              <input v-model="editingUser.email" type="email" class="input" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700">Role</label>
              <select v-model="editingUser.role" class="input">
                <option value="advisor">Advisor</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="flex justify-end gap-2">
              <button type="button" @click="showEditModal = false" class="btn-secondary">Cancel</button>
              <button type="submit" class="btn">Save Changes</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
        <div class="bg-white rounded-lg p-6 max-w-md w-full">
          <h3 class="text-lg font-semibold mb-4">Confirm Delete</h3>
          <p class="text-gray-600 mb-4">Are you sure you want to delete {{ userToDelete?.email }}? This action cannot be undone.</p>
          <div class="flex justify-end gap-2">
            <button @click="showDeleteModal = false" class="btn-secondary">Cancel</button>
            <button @click="confirmDeleteAction" class="btn-danger">Delete</button>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import api from '@/services/api'
import { onMounted, ref } from 'vue'
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

  const showEditModal = ref(false)
  const showDeleteModal = ref(false)
  const editingUser = ref(null)
  const userToDelete = ref(null)
  
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

  const startEdit = (user) => {
    editingUser.value = { ...user }
    showEditModal.value = true
  }

  const saveEdit = async () => {
    try {
      await api.put('/admin/user/edit', {
        user_id: editingUser.value.id,
        first_name: editingUser.value.first_name,
        last_name: editingUser.value.last_name,
        email: editingUser.value.email,
        role: editingUser.value.role
      })
      toast.success('User updated successfully')
      showEditModal.value = false
      fetchUsers()
    } catch (err) {
      toast.error('Failed to update user')
    }
  }

  const confirmDelete = (user) => {
    userToDelete.value = user
    showDeleteModal.value = true
  }

  const confirmDeleteAction = async () => {
    try {
      await api.delete(`/admin/user/delete/${userToDelete.value.id}`)
      toast.success(`Deleted ${userToDelete.value.email}`)
      showDeleteModal.value = false
      fetchUsers()
    } catch (err) {
      toast.error('Failed to delete user')
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
  .btn-secondary {
    @apply bg-gray-200 text-gray-700 py-2 px-4 rounded hover:bg-gray-300 transition;
  }
  .btn-danger {
    @apply bg-red-500 text-white py-2 px-4 rounded hover:bg-red-600 transition;
  }
  .action-btn {
    @apply flex items-center gap-1 px-3 py-1.5 rounded-md text-sm font-medium transition-colors;
  }
  .edit-btn {
    @apply text-blue-600 hover:bg-blue-50;
  }
  .delete-btn {
    @apply text-red-600 hover:bg-red-50;
  }
  </style>