<template>
  <div v-if="totalPages > 0" class="flex justify-center items-center space-x-2 mt-4">
    <button
      class="px-3 py-1 rounded border bg-white shadow hover:bg-gray-50"
      :disabled="page === 1"
      @click="$emit('update:page', page - 1)"
    >
      Prev
    </button>

    <span class="text-sm text-gray-700">
      Page {{ page }} of {{ totalPages }}
    </span>

    <button
      class="px-3 py-1 rounded border bg-white shadow hover:bg-gray-50"
      :disabled="page === totalPages"
      @click="$emit('update:page', page + 1)"
    >
      Next
    </button>
  </div>
</template>

<script setup>
import { toRefs } from 'vue'

const props = defineProps({
  page: Number,
  totalPages: Number,
})

// extract reactive values to use cleanly in template
const { page, totalPages } = toRefs(props)
</script>
