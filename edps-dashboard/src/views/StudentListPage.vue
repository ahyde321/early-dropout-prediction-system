<template>
  <div class="p-6">
    <h2 class="text-2xl font-semibold mb-4">Student List</h2>
    <StudentTable :students="students" />
  </div>
</template>

<script setup>
import StudentTable from '@/components/StudentTable.vue'
import { ref, onMounted } from 'vue'
import axios from 'axios'

const students = ref([])

onMounted(async () => {
  const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
  const { data } = await axios.get(`${baseURL}api/students/list`)
  students.value = data
})
</script>
