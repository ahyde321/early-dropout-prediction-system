<template>
  <span
    v-if="risk"
    :class="badgeClass"
    class="inline-block text-xs font-semibold px-2 py-1 rounded capitalize"
  >
    {{ risk }} Risk
  </span>
  <span
    v-else
    class="inline-block text-xs font-medium px-2 py-1 rounded bg-gray-200 text-gray-600"
  >
    No Prediction
  </span>
</template>

<script setup>
import { computed, toRef } from 'vue'

const props = defineProps({
  risk: {
    type: String,
    required: false,
    default: null,
  },
})

const risk = toRef(props, 'risk')

const badgeClass = computed(() => {
  switch (risk.value) {
    case 'high':
      return 'bg-red-100 text-red-700'
    case 'moderate':
      return 'bg-yellow-100 text-yellow-700'
    case 'low':
      return 'bg-green-100 text-green-700'
    default:
      return 'bg-gray-200 text-gray-600'
  }
})
</script>
