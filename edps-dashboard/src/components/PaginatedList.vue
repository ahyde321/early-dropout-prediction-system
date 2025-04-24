<template>
  <div class="space-y-2">
    <h4 class="text-sm font-medium text-gray-700 mb-2">{{ label }}</h4>
    <div class="border rounded-lg overflow-hidden">
      <div class="divide-y divide-gray-200">
        <div
          v-for="(item, index) in paginatedItems"
          :key="index"
          class="p-3 bg-white hover:bg-gray-50"
        >
          <div class="flex justify-between items-center">
            <div class="text-sm text-gray-900">
              {{ item.student_number || 'N/A' }}
            </div>
            <div class="text-sm text-gray-500">
              {{ item.reason || item.error }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="totalPages > 1" class="flex justify-between items-center pt-2">
      <div class="text-sm text-gray-500">
        Showing {{ startIndex + 1 }}-{{ Math.min(endIndex, items.length) }} of {{ items.length }}
      </div>
      <div class="flex gap-1">
        <button
          @click="currentPage--"
          :disabled="currentPage === 1"
          class="px-2 py-1 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Previous
        </button>
        <button
          @click="currentPage++"
          :disabled="currentPage === totalPages"
          class="px-2 py-1 text-xs font-medium text-gray-700 bg-white border border-gray-300 rounded hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
        >
          Next
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true
  },
  label: {
    type: String,
    required: true
  },
  itemsPerPage: {
    type: Number,
    default: 5
  }
})

const currentPage = ref(1)

const totalPages = computed(() => 
  Math.ceil(props.items.length / props.itemsPerPage)
)

const startIndex = computed(() => 
  (currentPage.value - 1) * props.itemsPerPage
)

const endIndex = computed(() => 
  startIndex.value + props.itemsPerPage
)

const paginatedItems = computed(() => 
  props.items.slice(startIndex.value, endIndex.value)
)
</script> 