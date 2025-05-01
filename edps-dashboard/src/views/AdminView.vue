<template>
    <div class="p-6 space-y-8 bg-gradient-to-b from-gray-50 to-white min-h-screen">
      <h1 class="text-3xl font-bold text-gray-800 bg-white p-4 rounded-xl shadow-sm">Admin Dashboard</h1>
  
      <!-- Invite/Register New User -->
      <section class="bg-white shadow-lg rounded-xl p-6 border border-gray-200 hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z" />
          </svg>
          Register New User
        </h2>
        <form @submit.prevent="registerUser" class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
            <input v-model="newUser.first_name" type="text" placeholder="First Name" required class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
            <input v-model="newUser.last_name" type="text" placeholder="Last Name" required class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
            <input v-model="newUser.email" type="email" placeholder="Email" required class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Password</label>
            <input v-model="newUser.password" type="password" placeholder="Password" required class="input" />
          </div>
          <div>
            <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
            <select v-model="newUser.role" class="input">
              <option value="advisor">Advisor</option>
              <option value="admin">Admin</option>
            </select>
          </div>
          <div class="md:col-span-2 flex justify-end">
            <button type="submit" class="btn-primary">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Register User
            </button>
          </div>
        </form>
      </section>
  
      <!-- User Management Table -->
      <section class="bg-white shadow-lg rounded-xl p-6 border border-gray-200 hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-xl font-semibold mb-4 text-gray-700 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" />
          </svg>
          Manage Users
        </h2>
        <div class="overflow-x-auto">
          <table class="w-full text-left text-sm">
            <thead>
              <tr class="border-b bg-gradient-to-r from-gray-50 to-gray-100">
                <th class="py-3 px-4 font-medium text-gray-700">Name</th>
                <th class="py-3 px-4 font-medium text-gray-700">Email</th>
                <th class="py-3 px-4 font-medium text-gray-700">Role</th>
                <th class="py-3 px-4 font-medium text-gray-700 text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in users" :key="user.id" class="border-t hover:bg-gray-50 transition-colors">
                <td class="py-3 px-4 font-medium text-gray-800">{{ user.first_name }} {{ user.last_name }}</td>
                <td class="py-3 px-4 text-gray-600">{{ user.email }}</td>
                <td class="py-3 px-4">
                  <span :class="{
                    'px-3 py-1.5 rounded-full text-xs font-medium shadow-sm': true,
                    'bg-blue-100 text-blue-800': user.role === 'admin',
                    'bg-green-100 text-green-800': user.role === 'advisor'
                  }">
                    {{ user.role }}
                  </span>
                </td>
                <td class="py-3 px-4">
                  <div class="flex justify-center gap-2">
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
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

      <!-- Edit User Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl">
          <h3 class="text-xl font-semibold mb-4 text-gray-700 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
            </svg>
            Edit User
          </h3>
          <form @submit.prevent="saveEdit" class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">First Name</label>
              <input v-model="editingUser.first_name" type="text" class="input" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
              <input v-model="editingUser.last_name" type="text" class="input" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Email</label>
              <input v-model="editingUser.email" type="email" class="input" required />
            </div>
            <div>
              <label class="block text-sm font-medium text-gray-700 mb-1">Role</label>
              <select v-model="editingUser.role" class="input">
                <option value="advisor">Advisor</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            <div class="flex justify-end gap-2">
              <button type="button" @click="showEditModal = false" class="btn-secondary">Cancel</button>
              <button type="submit" class="btn-primary">Save Changes</button>
            </div>
          </form>
        </div>
      </div>

      <!-- Delete Confirmation Modal -->
      <div v-if="showDeleteModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl">
          <h3 class="text-xl font-semibold mb-4 text-gray-700 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Confirm Delete
          </h3>
          <p class="text-gray-600 mb-4">Are you sure you want to delete {{ userToDelete?.email }}? This action cannot be undone.</p>
          <div class="flex justify-end gap-2">
            <button @click="showDeleteModal = false" class="btn-secondary">Cancel</button>
            <button @click="confirmDeleteAction" class="btn-danger">Delete</button>
          </div>
        </div>
      </div>

      <!-- Wipe Operations Section -->
      <section class="bg-white shadow-lg rounded-xl p-6 border border-gray-200 hover:shadow-xl transition-shadow duration-300">
        <h2 class="text-xl font-semibold mb-6 text-gray-700 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
          </svg>
          Wipe Operations
        </h2>
        <div class="space-y-6">
          <div class="bg-red-50 p-4 rounded-lg border border-red-100 hover:bg-red-100 transition-colors duration-200">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0">
                <button @click="showWipePredictionsModal = true" class="btn-danger whitespace-nowrap px-4 py-2.5 text-sm font-medium shadow-sm hover:shadow-md transition-all duration-200 w-48">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Wipe All Predictions
                </button>
              </div>
              <div>
                <h3 class="font-medium text-gray-800 mb-1">Delete All Predictions</h3>
                <p class="text-gray-600 text-sm">Permanently remove all risk prediction records from the database. This action cannot be undone.</p>
              </div>
            </div>
          </div>

          <div class="bg-red-50 p-4 rounded-lg border border-red-100 hover:bg-red-100 transition-colors duration-200">
            <div class="flex items-start gap-4">
              <div class="flex-shrink-0">
                <button @click="showWipeStudentsModal = true" class="btn-danger whitespace-nowrap px-4 py-2.5 text-sm font-medium shadow-sm hover:shadow-md transition-all duration-200 w-48">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 inline-block" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  Wipe All Students
                </button>
              </div>
              <div>
                <h3 class="font-medium text-gray-800 mb-1">Delete All Students</h3>
                <p class="text-gray-600 text-sm">Permanently remove all student records from the database. This action cannot be undone. Note: You must wipe predictions first.</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Wipe Students Confirmation Modal -->
      <div v-if="showWipeStudentsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl">
          <h3 class="text-xl font-semibold mb-4 text-gray-700 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Confirm Wipe Students
          </h3>
          <p class="text-gray-600 mb-4">Are you sure you want to delete ALL student records? This action cannot be undone and will permanently remove all student data from the database.</p>
          <div class="flex justify-end gap-2">
            <button @click="showWipeStudentsModal = false" class="btn-secondary">Cancel</button>
            <button @click="wipeStudents" class="btn-danger">Wipe Students</button>
          </div>
        </div>
      </div>

      <!-- Wipe Predictions Confirmation Modal -->
      <div v-if="showWipePredictionsModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div class="bg-white rounded-xl p-6 max-w-md w-full shadow-2xl">
          <h3 class="text-xl font-semibold mb-4 text-gray-700 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-red-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
            </svg>
            Confirm Wipe Predictions
          </h3>
          <p class="text-gray-600 mb-4">Are you sure you want to delete ALL prediction records? This action cannot be undone and will permanently remove all risk prediction data from the database.</p>
          <div class="flex justify-end gap-2">
            <button @click="showWipePredictionsModal = false" class="btn-secondary">Cancel</button>
            <button @click="wipePredictions" class="btn-danger">Wipe Predictions</button>
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
  const showWipeStudentsModal = ref(false)
  const showWipePredictionsModal = ref(false)
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

  const wipeStudents = async () => {
    try {
      await api.delete('/dev/wipe-students')
      toast.success('All student records have been deleted')
      showWipeStudentsModal.value = false
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to wipe student records')
    }
  }

  const wipePredictions = async () => {
    try {
      await api.delete('/dev/wipe-predictions')
      toast.success('All prediction records have been deleted')
      showWipePredictionsModal.value = false
    } catch (err) {
      toast.error(err.response?.data?.detail || 'Failed to wipe prediction records')
    }
  }
  
  const registerUser = async () => {
    try {
      await api.post('/auth/register', newUser.value)
      toast.success('User registered')
      newUser.value = { first_name: '', last_name: '', email: '', password: '', role: 'advisor' }
      fetchUsers()
    } catch (err) {
      if (err.response?.status === 422 && err.response?.data?.detail) {
        const errors = err.response.data.detail.map(e => e.msg).join(', ')
        toast.error(`Validation error: ${errors}`)
      } else {
        toast.error('Failed to register user')
      }
    }
  }
  
  onMounted(fetchUsers)
  </script>
  
  <style scoped>
  .input {
    @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-300 transition-colors;
  }
  .btn-primary {
    @apply bg-gradient-to-r from-sky-500 to-sky-600 text-white py-2 px-4 rounded hover:from-sky-600 hover:to-sky-700 transition-all shadow-sm flex items-center;
  }
  .btn-secondary {
    @apply bg-gray-200 text-gray-700 py-2 px-4 rounded hover:bg-gray-300 transition-all shadow-sm;
  }
  .btn-danger {
    @apply bg-gradient-to-r from-red-500 to-red-600 text-white py-2 px-4 rounded hover:from-red-600 hover:to-red-700 transition-all shadow-sm;
  }
  .action-btn {
    @apply flex items-center gap-1.5 px-3 py-1.5 rounded-md text-sm font-medium transition-all shadow-sm;
  }
  .edit-btn {
    @apply text-blue-600 hover:bg-blue-50 hover:text-blue-700;
  }
  .delete-btn {
    @apply text-red-600 hover:bg-red-50 hover:text-red-700;
  }
  </style>