<template>
  <div class="bg-white rounded-lg border border-gray-200">
    <!-- Table Header -->
    <div class="flex items-center justify-between p-4 border-b border-gray-200">
      <div class="flex gap-2 items-center">
        <h3 class="text-sm font-semibold text-gray-900">Student Records</h3>
        <span class="px-2 py-0.5 text-xs font-medium text-blue-600 bg-blue-50 rounded-full">
          {{ students.length }} total
        </span>
      </div>
      <div class="flex gap-2">
        <input 
          type="text"
          placeholder="Search students..."
          v-model="searchQuery"
          class="px-3 py-1.5 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 bg-white w-64"
        />
      </div>
    </div>

    <!-- Table Content -->
    <div class="overflow-x-auto">
      <table class="w-full">
        <thead>
          <tr class="border-b border-gray-200">
            <th 
              v-for="header in headers" 
              :key="header.key"
              class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider cursor-pointer hover:bg-gray-50 transition-colors"
              @click="sortBy(header.key)"
            >
              <div class="flex items-center gap-1">
                {{ header.label }}
                <template v-if="sortKey === header.key">
                  <ChevronUp v-if="sortOrder === 'asc'" class="w-3.5 h-3.5 text-blue-600" />
                  <ChevronDown v-else class="w-3.5 h-3.5 text-blue-600" />
                </template>
              </div>
            </th>
          </tr>
        </thead>
        <tbody class="divide-y divide-gray-200">
          <tr v-for="student in paginatedStudents" :key="student.student_number" class="hover:bg-gray-50 transition-colors">
            <td class="px-6 py-3.5 text-sm font-medium text-gray-900">
              {{ student.student_number }}
            </td>
            <td class="px-6 py-3.5 text-sm text-gray-900">
              {{ student.first_name }} {{ student.last_name }}
            </td>
            <td class="px-6 py-3.5">
              <div class="flex items-center gap-1.5">
                <div 
                  class="w-1.5 h-1.5 rounded-full"
                  :class="{
                    'bg-emerald-500': student.risk_level === 'low',
                    'bg-amber-500': student.risk_level === 'moderate',
                    'bg-rose-500': student.risk_level === 'high',
                    'bg-gray-300': !student.risk_level
                  }"
                ></div>
                <span class="text-sm capitalize" :class="{
                  'text-emerald-700': student.risk_level === 'low',
                  'text-amber-700': student.risk_level === 'moderate',
                  'text-rose-700': student.risk_level === 'high',
                  'text-gray-500': !student.risk_level
                }">
                  {{ student.risk_level || 'Not assessed' }}
                </span>
              </div>
            </td>
            <td class="px-6 py-3.5 text-sm text-gray-900">
              {{ student.risk_score ? (student.risk_score * 100).toFixed(1) + '%' : 'N/A' }}
            </td>
            <td class="px-6 py-3.5 text-right">
              <RouterLink 
                :to="'/students/' + student.student_number"
                class="text-sm text-blue-600 hover:text-blue-700 font-medium"
              >
                View Profile
              </RouterLink>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination -->
    <div class="flex items-center justify-between px-6 py-3 border-t border-gray-200">
      <div class="flex items-center text-sm text-gray-500">
        Showing {{ paginationStart + 1 }}-{{ Math.min(paginationEnd, sortedAndFilteredStudents.length) }} of {{ sortedAndFilteredStudents.length }}
      </div>
      <div class="flex items-center gap-1.5">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-2.5 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Previous
        </button>
        <div class="flex items-center">
          <template v-for="page in displayedPages" :key="page">
            <button
              v-if="page !== '...'"
              @click="currentPage = page"
              :class="[
                'px-2.5 py-1.5 text-xs font-medium rounded-md transition-colors mx-0.5',
                currentPage === page
                  ? 'bg-blue-50 text-blue-600 border border-blue-100'
                  : 'text-gray-700 hover:bg-gray-50 border border-transparent'
              ]"
            >
              {{ page }}
            </button>
            <span v-else class="px-1 text-gray-400">...</span>
          </template>
        </div>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-2.5 py-1.5 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ChevronUp, ChevronDown } from 'lucide-vue-next'

const props = defineProps({
  students: {
    type: Array,
    required: true
  }
})

const headers = [
  { key: 'student_number', label: 'Student ID' },
  { key: 'name', label: 'Full Name' },
  { key: 'risk_level', label: 'Risk Level' },
  { key: 'risk_score', label: 'Risk Score' },
  { key: 'actions', label: '' }
]

const searchQuery = ref('')
const sortKey = ref('student_number')
const sortOrder = ref('asc')
const currentPage = ref(1)
const itemsPerPage = 10

const sortBy = (key) => {
  if (sortKey.value === key) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
  } else {
    sortKey.value = key
    sortOrder.value = 'asc'
  }
  currentPage.value = 1 // Reset to first page when sorting
}

const sortedAndFilteredStudents = computed(() => {
  let filtered = props.students

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(student => 
      student.student_number.toLowerCase().includes(query) ||
      student.first_name.toLowerCase().includes(query) ||
      student.last_name.toLowerCase().includes(query) ||
      (student.risk_level || '').toLowerCase().includes(query)
    )
  }

  // Apply sorting
  return filtered.sort((a, b) => {
    let aVal, bVal

    switch (sortKey.value) {
      case 'name':
        aVal = `${a.first_name} ${a.last_name}`
        bVal = `${b.first_name} ${b.last_name}`
        break
      case 'risk_score':
        aVal = a.risk_score || 0
        bVal = b.risk_score || 0
        break
      default:
        aVal = a[sortKey.value]
        bVal = b[sortKey.value]
    }

    if (sortOrder.value === 'desc') {
      [aVal, bVal] = [bVal, aVal]
    }

    return aVal > bVal ? 1 : aVal < bVal ? -1 : 0
  })
})

// Pagination computeds
const totalPages = computed(() => 
  Math.max(1, Math.ceil(sortedAndFilteredStudents.value.length / itemsPerPage))
)

const paginationStart = computed(() => (currentPage.value - 1) * itemsPerPage)
const paginationEnd = computed(() => paginationStart.value + itemsPerPage)

const paginatedStudents = computed(() => 
  sortedAndFilteredStudents.value.slice(paginationStart.value, paginationEnd.value)
)

// Watch for changes that should reset pagination
watch([searchQuery], () => {
  currentPage.value = 1
})

// Calculate displayed page numbers
const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []

  if (total <= 7) {
    // Show all pages if 7 or fewer
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    // Always show first page
    pages.push(1)
    
    if (current > 3) {
      pages.push('...')
    }

    // Show pages around current page
    for (let i = Math.max(2, current - 1); i <= Math.min(current + 1, total - 1); i++) {
      pages.push(i)
    }

    if (current < total - 2) {
      pages.push('...')
    }

    // Always show last page
    pages.push(total)
  }

  return pages
})
</script>