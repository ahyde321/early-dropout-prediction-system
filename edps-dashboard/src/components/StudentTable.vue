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
    <div v-else-if="sorted.length" class="overflow-x-auto rounded border border-gray-200">
      <table class="min-w-full bg-white text-sm">
        <thead class="bg-gray-50 text-gray-600">
          <tr>
            <th
              class="px-4 py-3 text-center cursor-pointer hover:underline"
              @click="toggleSort('student_number')"
            >
              Student #
              <span v-if="sortBy === 'student_number'">
                {{ sortAsc ? '▲' : '▼' }}
              </span>
            </th>
            <th
              class="px-4 py-3 text-center cursor-pointer hover:underline"
              @click="toggleSort('name')"
            >
              Name
              <span v-if="sortBy === 'name'">
                {{ sortAsc ? '▲' : '▼' }}
              </span>
            </th>
            <th
              class="px-4 py-3 text-center cursor-pointer hover:underline"
              @click="toggleSort('risk_level')"
            >
              Risk
              <span v-if="sortBy === 'risk_level'">
                {{ sortAsc ? '▲' : '▼' }}
              </span>
            </th>
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
              <RiskBadge :risk="student.risk_level" />
            </td>
            <td class="px-4 py-2 text-center">
              <RouterLink
                :to="`/students/${student.student_number}`"
                class="text-sm text-blue-600 hover:underline"
              >
                View Details
              </RouterLink>
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

<script setup>
import { ref, computed, toRef } from 'vue'
import { RouterLink } from 'vue-router'
import RiskBadge from './RiskBadge.vue'
import BasePagination from './BasePagination.vue'

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

const students = toRef(props, 'students')
const loading = toRef(props, 'loading')

const search = ref('')
const currentPage = ref(1)
const itemsPerPage = 10
const sortBy = ref('student_number')
const sortAsc = ref(true)

const riskOrder = {
  high: 3,
  moderate: 2,
  low: 1,
  null: 0,
  undefined: 0,
}

const filtered = computed(() => {
  const q = search.value.toLowerCase()
  return (students.value || []).filter((s) => {
    const studentName = `${s.first_name} ${s.last_name}`.toLowerCase()
    return (
      s.student_number?.toLowerCase().includes(q) ||
      studentName.includes(q)
    )
  })
})

const sorted = computed(() => {
  const list = [...filtered.value]
  list.sort((a, b) => {
    let aVal = a[sortBy.value]
    let bVal = b[sortBy.value]

    if (sortBy.value === 'name') {
      aVal = `${a.first_name} ${a.last_name}`.toLowerCase()
      bVal = `${b.first_name} ${b.last_name}`.toLowerCase()
    }

    if (sortBy.value === 'risk_level') {
      aVal = riskOrder[a.risk_level] ?? 0
      bVal = riskOrder[b.risk_level] ?? 0
    }

    if (typeof aVal === 'string' && typeof bVal === 'string') {
      return sortAsc.value ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal)
    }
    return sortAsc.value ? aVal - bVal : bVal - aVal
  })
  return list
})

const paginated = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  return sorted.value.slice(start, start + itemsPerPage)
})

const totalPages = computed(() =>
  Math.ceil(sorted.value.length / itemsPerPage)
)

const toggleSort = (field) => {
  if (sortBy.value === field) {
    sortAsc.value = !sortAsc.value
  } else {
    sortBy.value = field
    sortAsc.value = true
  }
}

const exportCSV = () => {
  const rows = [
    ['Student Number', 'First Name', 'Last Name', 'Risk Level'],
    ...filtered.value.map(s => [
      s.student_number,
      s.first_name,
      s.last_name,
      s.risk_level || 'N/A',
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