<template>
  <div class="bg-gradient-to-br from-white to-yellow-50 p-6 rounded-3xl shadow-md border border-yellow-200">
    <!-- Header -->
    <div class="flex items-center gap-3 mb-4">
      <div class="bg-yellow-100 text-yellow-600 p-2 rounded-full ring-2 ring-yellow-300 shadow-inner">
        <NotebookPen class="w-5 h-5" />
      </div>
      <div>
        <h2 class="text-sm text-gray-500 uppercase font-semibold tracking-wide">
          Advisor Alert
        </h2>
        <h3 class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent">
          Students Requiring Review
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
          <div>
            <p class="font-semibold text-gray-800">
              {{ s.first_name }} {{ s.last_name }}
              <span class="text-sm text-yellow-600 font-medium ml-2">
                – {{ s.reason }}
              </span>
            </p>
          </div>
        </li>
      </RouterLink>
    </ul>

    <!-- Empty State -->
    <p v-else class="text-sm text-gray-500">No outstanding reviews found.</p>
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
