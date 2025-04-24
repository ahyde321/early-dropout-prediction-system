<template>
  <div class="bg-gradient-to-br from-red-50/80 to-red-50/40 p-5 rounded-2xl shadow-lg border border-red-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">
    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-red-100 to-red-50 text-red-600">
          <AlertTriangle class="w-3.5 h-3.5" />
        </div>
        <h3 class="text-sm font-semibold text-gray-900">
          Students to Watch
        </h3>
      </div>
      <p class="text-xs text-gray-500 ml-[38px]">Highest Risk</p>
    </div>

    <!-- Student List -->
    <ul class="space-y-2" v-if="students.length">
      <RouterLink
        v-for="s in students"
        :key="s.student_number"
        :to="`/students/${s.student_number}`"
        class="block"
      >
        <li
          class="p-2.5 bg-white/60 backdrop-blur-sm rounded-xl border border-red-100/30 flex justify-between items-center transition duration-200 hover:shadow-md hover:scale-[1.01] hover:bg-white"
        >
          <!-- Student Info -->
          <div>
            <p class="font-medium text-gray-800 text-sm">
              {{ s.first_name }} {{ s.last_name }}
            </p>
          </div>

          <!-- Risk Score -->
          <span
            class="ml-3 inline-flex items-center bg-red-100 text-red-600 text-xs font-semibold px-2 py-0.5 rounded-full"
          >
            {{ s.risk_score.toFixed(2) }}
          </span>
        </li>
      </RouterLink>
    </ul>

    <!-- Empty state -->
    <p v-else class="text-xs text-gray-500 ml-[38px]">No high-risk students found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { AlertTriangle } from 'lucide-vue-next'
import api from '@/services/api'

const students = ref([])

const fetchHighRiskStudents = async () => {
  try {
    const { data } = await api.get('/students/list')
    students.value = data
      .filter(s => s.risk_level === 'high' && typeof s.risk_score === 'number')
      .sort((a, b) => b.risk_score - a.risk_score)
      .slice(0, 5)
  } catch (error) {
    console.error('Failed to fetch students:', error)
  }
}

onMounted(fetchHighRiskStudents)
</script>
