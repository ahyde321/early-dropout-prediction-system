<template>
  <div class="overflow-hidden bg-white shadow-sm rounded-lg border border-gray-200">
    <!-- Table Header -->
    <div class="p-4 flex justify-between items-center">
      <div class="flex items-center">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-500" viewBox="0 0 20 20" fill="currentColor">
          <path d="M9 6a3 3 0 11-6 0 3 3 0 016 0zM17 6a3 3 0 11-6 0 3 3 0 016 0zM12.93 17c.046-.327.07-.66.07-1a6.97 6.97 0 00-1.5-4.33A5 5 0 0119 16v1h-6.07zM6 11a5 5 0 015 5v1H1v-1a5 5 0 015-5z" />
        </svg>
        <h3 class="text-lg font-medium text-gray-700">Students</h3>
      </div>
      
      <!-- Search & Filter Controls -->
      <div class="flex items-center space-x-2">
        <div class="relative">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search students..."
            class="pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
          >
          <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <svg class="h-4 w-4 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M8 4a4 4 0 100 8 4 4 0 000-8zM2 8a6 6 0 1110.89 3.476l4.817 4.817a1 1 0 01-1.414 1.414l-4.816-4.816A6 6 0 012 8z" clip-rule="evenodd" />
            </svg>
          </div>
        </div>
        
        <select
          v-model="sortKey"
          @change="sortStudents"
          class="py-2 pl-3 pr-8 border border-gray-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-all duration-200"
        >
          <option value="student_number">Student Number</option>
          <option value="name">Name</option>
          <option value="risk_score">Risk Score</option>
        </select>
        
        <button
          @click="toggleSortOrder"
          class="p-2 bg-white border border-gray-300 rounded-lg flex items-center justify-center focus:outline-none focus:ring-2 focus:ring-blue-500 hover:bg-gray-50 transition-all duration-200"
          :title="sortOrder === 'asc' ? 'Sort descending' : 'Sort ascending'"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="h-4 w-4 text-gray-500"
            :class="{ 'transform rotate-180': sortOrder === 'desc' }"
            viewBox="0 0 20 20" 
            fill="currentColor"
          >
            <path fill-rule="evenodd" d="M5.293 7.707a1 1 0 010-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 01-1.414 1.414L10 4.414l-3.293 3.293a1 1 0 01-1.414 0zM10 15.586l-3.293-3.293a1 1 0 011.414-1.414L10 13.586l2.293-2.293a1 1 0 011.414 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    
    <!-- Table Content -->
    <div class="overflow-x-auto">
      <table class="min-w-full divide-y divide-gray-200">
        <thead class="bg-gray-50">
          <tr>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Student Number
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Name
            </th>
            <th class="py-3 px-4 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              Risk Level
            </th>
            <th class="py-3 px-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Risk Score
            </th>
            <th class="py-3 px-4 text-center text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody class="bg-white divide-y divide-gray-200">
          <tr 
            v-for="(student, index) in paginatedStudents" 
            :key="student.student_number" 
            class="hover:bg-gray-50 transition-colors duration-150"
          >
            <td class="py-3 px-4 whitespace-nowrap">
              <span class="font-medium text-gray-900">{{ student.student_number }}</span>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="text-gray-900 font-medium">{{ student.first_name }} {{ student.last_name }}</div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap text-center">
              <span 
                v-if="student.risk_level === 'high'"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700"
              >
                <span class="h-2 w-2 mr-1.5 rounded-full bg-red-500"></span>
                High
              </span>
              <span 
                v-else-if="student.risk_level === 'moderate'"
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-yellow-100 text-yellow-700"
                >
                <span class="h-2 w-2 mr-1.5 rounded-full bg-yellow-500"></span>
                Moderate
              </span>
              <span 
                v-else
                class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700"
              >
                <span class="h-2 w-2 mr-1.5 rounded-full bg-green-500"></span>
                Low
              </span>
            </td>
            <td class="py-3 px-4 whitespace-nowrap">
              <div class="flex items-center">
                <div class="w-32 bg-gray-200 rounded-full h-2 mr-3">
                  <div 
                    class="h-2 rounded-full" 
                    :class="{
                      'bg-red-500': student.risk_level === 'high',
                      'bg-yellow-400': student.risk_level === 'moderate',
                      'bg-green-500': student.risk_level === 'low'
                    }"
                    :style="{ width: `${student.risk_score * 100}%` }"
                  ></div>
                </div>
                <span class="text-sm font-medium">{{ student.risk_score.toFixed(1) }}</span>
              </div>
            </td>
            <td class="py-3 px-4 whitespace-nowrap text-center">
              <router-link 
                :to="{ name: 'StudentProfile', params: { student_number: student.student_number }}"
                class="inline-flex items-center justify-center px-3 py-1.5 rounded-md bg-blue-600 text-white text-sm font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-1" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
                  <path fill-rule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clip-rule="evenodd" />
                </svg>
                View
              </router-link>
            </td>
          </tr>
          <tr v-if="paginatedStudents.length === 0">
            <td colspan="5" class="py-8 text-center text-gray-500">
              <div class="flex flex-col items-center justify-center">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 text-gray-400 mb-3" viewBox="0 0 20 20" fill="currentColor">
                  <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                </svg>
                <p>No students found</p>
                <p class="text-sm mt-1">Try adjusting your search or filters</p>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    
    <!-- Pagination Controls -->
    <div class="py-3 px-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
      <div class="flex items-center">
        <span class="text-sm text-gray-700">
          Showing <span class="font-medium">{{ startIndex + 1 }}</span> to <span class="font-medium">{{ endIndex }}</span> of <span class="font-medium">{{ filteredStudents.length }}</span> results
        </span>
      </div>
      <div class="flex items-center space-x-2">
        <select
          v-model="studentsPerPage"
          class="py-1.5 pl-2 pr-8 border border-gray-300 rounded-md text-sm bg-white focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="10">10 per page</option>
          <option value="25">25 per page</option>
          <option value="50">50 per page</option>
          <option value="100">100 per page</option>
        </select>
        
        <div class="flex space-x-1">
          <button
            @click="changePage(currentPage - 1)"
            :disabled="currentPage === 1"
            class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M12.707 5.293a1 1 0 010 1.414L9.414 10l3.293 3.293a1 1 0 01-1.414 1.414l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
          
          <div 
            v-for="page in visiblePageNumbers" 
            :key="page"
            class="inline-flex"
          >
            <button
              v-if="page !== '...'"
              @click="changePage(page)"
              class="px-3 py-1.5 border text-sm font-medium rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
              :class="page === currentPage ? 'border-blue-500 bg-blue-50 text-blue-700' : 'border-gray-300 bg-white text-gray-700 hover:bg-gray-50'"
            >
              {{ page }}
            </button>
            <span
              v-else
              class="px-3 py-1.5 border border-gray-300 text-sm text-gray-700 rounded-md bg-white"
            >
              {{ page }}
            </span>
          </div>
          
          <button
            @click="changePage(currentPage + 1)"
            :disabled="currentPage >= totalPages"
            class="inline-flex items-center px-2.5 py-1.5 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
          >
            <svg class="h-4 w-4" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
              <path fill-rule="evenodd" d="M7.293 14.707a1 1 0 010-1.414L10.586 10 7.293 6.707a1 1 0 011.414-1.414l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414 0z" clip-rule="evenodd" />
            </svg>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  students: {
    type: Array,
    required: true
  }
})

// Pagination state
const currentPage = ref(1)
const studentsPerPage = ref(10)
const searchQuery = ref('')
const sortKey = ref('student_number')
const sortOrder = ref('asc')

// Computed properties for filtering and pagination
const filteredStudents = computed(() => {
  let result = [...props.students]
  
  // Apply search filtering
  if (searchQuery.value && searchQuery.value.trim() !== '') {
    const query = searchQuery.value.toLowerCase().trim()
    result = result.filter(student => (
      student.student_number.toString().includes(query) ||
      student.first_name.toLowerCase().includes(query) ||
      student.last_name.toLowerCase().includes(query) ||
      `${student.first_name} ${student.last_name}`.toLowerCase().includes(query) ||
      student.risk_level.toLowerCase().includes(query)
    ))
  }
  
  // Apply sorting
  result.sort((a, b) => {
    if (sortKey.value === 'name') {
      const nameA = `${a.first_name} ${a.last_name}`.toLowerCase()
      const nameB = `${b.first_name} ${b.last_name}`.toLowerCase()
      return sortOrder.value === 'asc'
        ? nameA.localeCompare(nameB)
        : nameB.localeCompare(nameA)
    }
    
    if (sortKey.value === 'student_number') {
      return sortOrder.value === 'asc'
        ? a.student_number.localeCompare(b.student_number)
        : b.student_number.localeCompare(a.student_number)
    }
    
    if (sortKey.value === 'risk_score') {
      return sortOrder.value === 'asc'
        ? a.risk_score - b.risk_score
        : b.risk_score - a.risk_score
    }
    
    return 0
  })
  
  return result
})

const totalPages = computed(() => {
  return Math.max(1, Math.ceil(filteredStudents.value.length / studentsPerPage.value))
})

const startIndex = computed(() => {
  return (currentPage.value - 1) * studentsPerPage.value
})

const endIndex = computed(() => {
  return Math.min(startIndex.value + studentsPerPage.value, filteredStudents.value.length)
})

const paginatedStudents = computed(() => {
  return filteredStudents.value.slice(startIndex.value, endIndex.value)
})

// Pagination display logic
const visiblePageNumbers = computed(() => {
  if (totalPages.value <= 7) {
    return Array.from({ length: totalPages.value }, (_, i) => i + 1)
  }
  
  const pages = []
  
  if (currentPage.value <= 3) {
    // Near start
    for (let i = 1; i <= 5; i++) {
      pages.push(i)
    }
    pages.push('...')
    pages.push(totalPages.value)
  } else if (currentPage.value >= totalPages.value - 2) {
    // Near end
    pages.push(1)
    pages.push('...')
    for (let i = totalPages.value - 4; i <= totalPages.value; i++) {
      pages.push(i)
    }
  } else {
    // Middle
    pages.push(1)
    pages.push('...')
    for (let i = currentPage.value - 1; i <= currentPage.value + 1; i++) {
      pages.push(i)
    }
    pages.push('...')
    pages.push(totalPages.value)
  }
  
  return pages
})

// Methods
function changePage(page) {
  if (page >= 1 && page <= totalPages.value) {
    currentPage.value = page
  }
}

function sortStudents() {
  // Sorting is handled through computed property
}

function toggleSortOrder() {
  sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'
}

function clearSearch() {
  searchQuery.value = ''
  currentPage.value = 1
}

// Reset to page 1 when filter, sort or items per page changes
watch([searchQuery, sortKey, sortOrder, studentsPerPage], () => {
  currentPage.value = 1
})
</script>