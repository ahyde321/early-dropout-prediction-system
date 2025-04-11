<script setup>
import { toRefs, computed } from 'vue'
import { AlertCircle, BarChart2, Shield } from 'lucide-vue-next'


const props = defineProps({
  label: String,
  value: Number,
  color: {
    type: String,
    default: 'gray',
  },
})

const { label, value, color } = toRefs(props)

const cardClasses = computed(() => {
  const bg = {
    blue: 'bg-blue-50 border-blue-200',
    red: 'bg-red-50 border-red-200',
    yellow: 'bg-yellow-50 border-yellow-200',
    gray: 'bg-gray-50 border-gray-200',
    green: 'bg-green-50 border-green-200',
  }
  return `p-4 rounded-lg shadow ${bg[color.value] || bg.gray} border`
})

const iconComponent = computed(() => {
  if (color.value === 'red') return AlertCircle
  if (color.value === 'blue') return BarChart2
  if (color.value === 'yellow') return Shield
  return BarChart2
})
</script>

<template>
  <div :class="cardClasses" class="flex items-center justify-between">
    <div>
      <p class="text-sm text-gray-600">{{ label }}</p>
      <p class="text-2xl font-bold text-gray-900">{{ value }}</p>
    </div>
    <component :is="iconComponent" class="w-8 h-8 text-gray-600" />
  </div>
</template>
