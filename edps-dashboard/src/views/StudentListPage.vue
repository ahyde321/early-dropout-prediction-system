<template>
  <div class="p-6 space-y-6">
    <!-- Header -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-semibold text-gray-900">Students</h1>
        <p class="mt-1 text-sm text-gray-500">View and manage student records</p>
      </div>
      <div class="flex gap-3">
        <a 
          :href="`${baseURL.replace(/\/$/, '')}/api/download/students`" 
          class="inline-flex items-center gap-2 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-lg hover:bg-gray-50"
        >
          <Download class="w-4 h-4" />
          Export CSV
        </a>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex items-center justify-center h-64">
      <div class="flex flex-col items-center gap-2">
        <div class="w-8 h-8 border-4 border-blue-200 border-t-blue-600 rounded-full animate-spin"></div>
        <p class="text-sm text-gray-500">Loading students...</p>
      </div>
    </div>

    <!-- Error State -->
    <div v-else-if="!students.length" class="flex flex-col items-center justify-center h-64 text-center">
      <div class="text-gray-400">
        <div class="mb-2">No students found</div>
        <p class="text-sm">There might be an issue connecting to the server or no data is available.</p>
      </div>
    </div>

    <!-- Table -->
    <StudentTable 
      v-else 
      :students="students" 
      :initialRiskFilter="riskParam" 
    />
  </div>
</template>

<script setup>
import StudentTable from '@/components/StudentTable.vue'
import axios from 'axios'
import { Download } from 'lucide-vue-next'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

const students = ref([])
const loading = ref(true)
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/'

const route = useRoute()
const riskParam = route.query.risk ?? '' // "high", "moderate", or "low"

onMounted(async () => {
  try {
    const { data } = await axios.get(`${baseURL.replace(/\/$/, '')}/api/students/list`)
    students.value = data
  } catch (error) {
    console.error('Failed to fetch students:', error)
    students.value = []
  } finally {
    loading.value = false
  }
})
</script>
