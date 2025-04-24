<template>
  <div class="bg-gradient-to-br from-orange-50/80 to-orange-50/40 p-5 rounded-2xl shadow-lg border border-orange-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">
    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-orange-100 to-orange-50 text-orange-600">
          <ArrowUpRight class="w-3.5 h-3.5" />
        </div>
        <h3 class="text-sm font-semibold text-gray-900">
          Biggest Score Increases
        </h3>
      </div>
      <p class="text-xs text-gray-500 ml-[38px]">Risk Shift</p>
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
          class="p-2.5 bg-white/60 backdrop-blur-sm rounded-xl border border-orange-100/30 flex justify-between items-center transition duration-200 hover:shadow-md hover:scale-[1.01] hover:bg-white"
        >
          <!-- Student Info -->
          <div>
            <p class="font-medium text-gray-800 text-sm">
              {{ s.first_name }} {{ s.last_name }}
              <span class="text-xs text-gray-500 font-normal ml-2">
                {{ s.previous_score.toFixed(2) }} → {{ s.current_score.toFixed(2) }}
              </span>
            </p>
          </div>

          <!-- Increase Badge -->
          <span
            class="ml-3 inline-flex items-center bg-orange-100 text-orange-600 text-xs font-semibold px-2 py-0.5 rounded-full"
          >
            +{{ s.increase.toFixed(2) }}
          </span>
        </li>
      </RouterLink>
    </ul>

    <!-- Empty State -->
    <p v-else class="text-xs text-gray-500 ml-[38px]">No significant increases found.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ArrowUpRight } from 'lucide-vue-next'
import api from '@/services/api'

const students = ref([])

const fetchIncreases = async () => {
  try {
    const { data } = await api.get('/insights/risk-increase')
    students.value = data
  } catch (err) {
    console.error('Failed to fetch risk increases:', err)
  }
}

onMounted(fetchIncreases)
</script>
