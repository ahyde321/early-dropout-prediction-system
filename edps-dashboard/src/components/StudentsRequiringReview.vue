<template>
  <div class="bg-gradient-to-br from-yellow-50/80 to-yellow-50/40 p-5 rounded-2xl shadow-lg border border-yellow-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">
    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-yellow-100 to-yellow-50 text-yellow-600">
          <NotebookPen class="w-3.5 h-3.5" />
        </div>
        <h3 class="text-sm font-semibold text-gray-900">
          Students Requiring Review
        </h3>
      </div>
      <p class="text-xs text-gray-500 ml-[38px]">Advisor Alert</p>
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
          class="p-2.5 bg-white/60 backdrop-blur-sm rounded-xl border border-yellow-100/30 flex justify-between items-center transition duration-200 hover:shadow-md hover:scale-[1.01] hover:bg-white"
        >
          <div>
            <p class="font-medium text-gray-800 text-sm">
              {{ s.first_name }} {{ s.last_name }}
              <span class="text-xs text-yellow-600 font-medium ml-2">
                – {{ s.reason }}
              </span>
            </p>
          </div>
        </li>
      </RouterLink>
    </ul>

    <!-- Empty State -->
    <p v-else class="text-xs text-gray-500 ml-[38px]">No outstanding reviews found.</p>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { NotebookPen } from 'lucide-vue-next'

const students = ref([
  {
    student_number: '40342',
    first_name: 'Evan',
    last_name: 'Nolan',
    reason: 'No advisor notes in last 30 days'
  },
  {
    student_number: '40309',
    first_name: 'Leila',
    last_name: 'Akhtar',
    reason: 'Missing follow-up on flagged score'
  },
  {
    student_number: '40281',
    first_name: 'Jack',
    last_name: 'Murphy',
    reason: 'High risk without action logged'
  }
])
</script>
