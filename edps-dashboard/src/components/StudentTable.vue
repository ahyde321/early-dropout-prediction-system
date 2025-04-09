<script setup>
import RiskBadge from './RiskBadge.vue'
import BasePagination from './BasePagination.vue'
import { ref, computed, toRef } from 'vue'

// Props
const props = defineProps({
  students: {
    type: Array,
    required: true,
  },
  loading: {
    type: Boolean,
    default: false,
  },
})

// Emits
const emit = defineEmits(['view-student'])

const students = toRef(props, 'students')
const loading = toRef(props, 'loading')

const search = ref('')
const currentPage = ref(1)
const itemsPerPage = 10

// Filtering
const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return (students.value || []).filter((s) =>
    [s.student_number, s.first_name, s.last_name].some((v) =>
      v?.toLowerCase?.().includes(q)
    )
  )
})

// Pagination
const paginated = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return filtered.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() =>
  Math.ceil(filtered.value.length / itemsPerPage)
)

// CSV Export
const exportCSV = () => {
  const rows = [
    ['Student Number', 'First Name', 'Last Name', 'Risk Score'],
    ...filtered.value.map(s => [
      s.student_number,
      s.first_name,
      s.last_name,
      s.risk_score,
    ])
  ]

  const csvContent = rows.map(r => r.join(',')).join('\n')
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' })
  const link = document.createElement('a')
  link.href = URL.createObjectURL(blob)
  link.setAttribute('download', 'students.csv')
  link.click()
}
</script>

<template>
  <div class="bg-white p-6 rounded-lg shadow border border-gray-200">
    <div class="flex justify-between items-center mb-4">
      <input
        v-model="search"
        placeholder="Search students..."
        class="w-full md:max-w-md p-2 border rounded shadow-sm"
      />
      <button
        class="ml-4 px-4 py-2 text-sm bg-blue-600 text-white rounded hover:bg-blue-700"
        @click="exportCSV"
      >
        Export CSV
      </button>
    </div>

    <!-- Loading Spinner -->
    <div v-if="loading" class="text-center py-12">
      <span class="animate-spin inline-block w-6 h-6 border-4 border-blue-300 border-t-transparent rounded-full"></span>
      <p class="mt-2 text-sm text-gray-600">Loading students...</p>
    </div>

    <!-- Table -->
    <div v-else-if="filtered.length" class="overflow-x-auto rounded border border-gray-200">
      <table class="min-w-full bg-white text-sm">
        <thead class="bg-gray-50 text-gray-600">
          <tr>
            <th class="px-4 py-3 text-center">Student #</th>
            <th class="px-4 py-3 text-center">Name</th>
            <th class="px-4 py-3 text-center">Risk</th>
            <th class="px-4 py-3 text-center">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr
            v-for="student in paginated"
            :key="student.student_number"
            class="border-t even:bg-gray-50 hover:bg-gray-100 transition"
          >
            <td class="px-4 py-2 text-center font-medium text-gray-800">
              {{ student.student_number }}
            </td>
            <td class="px-4 py-2 text-center text-gray-700">
              {{ student.first_name }} {{ student.last_name }}
            </td>
            <td class="px-4 py-2 text-center">
              <RiskBadge :score="student.risk_score" />
            </td>
            <td class="px-4 py-2 text-center">
              <button
                class="text-sm text-blue-600 hover:underline"
                @click="emit('view-student', student)"
              >
                View Details
              </button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Empty state -->
    <div v-else class="text-center text-gray-500 py-8">
      No matching students found.
    </div>

    <!-- Pagination -->
    <BasePagination
      v-if="totalPages > 1 && !loading"
      class="mt-6"
      :page="currentPage"
      :totalPages="totalPages"
      @update:page="currentPage = $event"
    />
  </div>
</template>
