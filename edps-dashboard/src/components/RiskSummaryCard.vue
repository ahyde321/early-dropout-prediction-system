<script setup>
import { toRefs } from 'vue'

const props = defineProps({
  label: String,
  value: Number,
  color: {
    type: String,
    default: 'gray',
  },
})

const { label, value, color } = toRefs(props)
</script>

<template>
  <div :class="`p-4 rounded-lg shadow bg-${color.value}-50 border border-${color.value}-200`">
    <p class="text-sm text-gray-600">{{ label }}</p>
    <p class="text-2xl font-bold text-gray-900">{{ value }}</p>
  </div>
</template>