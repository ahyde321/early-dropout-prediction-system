<template>
  <div class="bg-gradient-to-br from-white to-orange-50 p-6 rounded-3xl shadow-md border border-orange-200">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-4">
      <div class="bg-orange-100 text-orange-600 p-2 rounded-full ring-2 ring-orange-300 shadow-inner">
        <ArrowUpRight class="w-5 h-5" />
      </div>
      <div>
        <h2 class="text-sm text-gray-500 uppercase font-semibold tracking-wide">
          Risk Shift
        </h2>
        <h3 class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
          Biggest Score Increases
        </h3>
      </div>
    </div>

    <!-- Student List -->
    <ul class="space-y-3" v-if="students.length">
      <RouterLink
        v-for="s in students"
        :key="s.student_number"
        :to="`/students/${s.student_number}`"
        class="block"
      >
        <li
          class="p-3 bg-white rounded-xl border border-gray-100 flex justify-between items-center transition duration-200 cursor-pointer hover:shadow-md hover:scale-[1.01]"
        >
          <!-- Student Info -->
          <div>
            <p class="font-semibold text-gray-800">
              {{ s.first_name }} {{ s.last_name }}
              <span class="text-sm text-gray-500 font-normal ml-2">
                {{ s.previous_score.toFixed(2) }} → {{ s.current_score.toFixed(2) }}
              </span>
            </p>
          </div>

          <!-- Increase Badge -->
          <span
            class="ml-4 inline-block bg-orange-100 text-orange-600 text-xs font-semibold px-2.5 py-0.5 rounded-full shadow-sm"
          >
            +{{ s.increase.toFixed(2) }}
          </span>
        </li>
      </RouterLink>
    </ul>

    <!-- Empty State -->
    <p v-else class="text-sm text-gray-500">No significant increases found.</p>
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
    console.error('❌ Failed to fetch risk increases:', err)
  }
}

onMounted(fetchIncreases)
</script>
