￼

<script setup>
import { toRefs, computed, ref, watch } from 'vue'
import {
  AlertCircle,
  BarChart2,
  TriangleAlert,
  CheckCircle,
  Info
} from 'lucide-vue-next'

const props = defineProps({
  label: { type: String, required: true },
  value: { type: Number, required: true },
  color: {
    type: String,
    default: 'gray',
    validator: val => ['blue', 'red', 'yellow', 'green', 'gray'].includes(val)
  },
  trend: {
    type: Number,
    default: null
  },
  to: { type: String, default: null }
})

const { label, value, color, trend, to } = toRefs(props)

const tooltipText = computed(() => {
  if (trend.value !== null) {
    const symbol = trend.value > 0 ? '↑' : trend.value < 0 ? '↓' : '→'
    const abs = Math.abs(trend.value)
    return `${symbol} ${abs} students`
  }
  return null
})

const cardClasses = computed(() => {
  const bg = {
    blue: 'from-blue-50 via-blue-100 to-blue-50 border-blue-200 ring-blue-200 shadow-blue-100/50',
    red: 'from-red-50 via-red-100 to-red-50 border-red-200 ring-red-300 shadow-red-100/50 animate-pulse-soft',
    yellow: 'from-yellow-50 via-yellow-100 to-yellow-50 border-yellow-200 ring-yellow-200 shadow-yellow-100/50',
    green: 'from-green-50 via-green-100 to-green-50 border-green-200 ring-green-200 shadow-green-100/50',
    gray: 'from-gray-50 via-gray-100 to-gray-50 border-gray-200 ring-gray-200 shadow-gray-100/50'
  }
  return `bg-gradient-to-br ${bg[color.value] || bg.gray} border p-5 rounded-2xl shadow-lg group hover:ring-2 transition-all duration-300 ease-in-out`
})

const iconComponent = computed(() => {
  switch (color.value) {
    case 'red': return AlertCircle
    case 'yellow': return TriangleAlert
    case 'green': return CheckCircle
    case 'blue': return BarChart2
    default: return Info
  }
})

const displayValue = ref(0)
const animateCounter = () => {
  const duration = 1000
  const startTime = performance.now()
  const start = displayValue.value
  const end = value.value
  const step = (now) => {
    const progress = Math.min((now - startTime) / duration, 1)
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)
    displayValue.value = Math.floor(easeOutQuart * (end - start) + start)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}
watch(value, animateCounter, { immediate: true })
</script>

<template>
  <component :is="to ? 'RouterLink' : 'div'" :to="to" class="block cursor-pointer hover:scale-[1.02] transition-transform duration-300">
    <div
      :class="cardClasses"
      class="flex items-center justify-between gap-6 relative z-10 overflow-hidden"
    >
      <div class="relative">
        <p class="text-sm font-medium text-gray-600 mb-1">{{ label }}</p>
        <p class="text-4xl font-bold tracking-tight" :class="{
          'text-blue-600': color === 'blue',
          'text-red-600': color === 'red',
          'text-yellow-600': color === 'yellow',
          'text-green-600': color === 'green',
          'text-gray-900': color === 'gray'
        }">
          {{ displayValue }}
        </p>
      </div>

      <div class="relative">
        <component
          :is="iconComponent"
          class="w-10 h-10 transition-transform duration-300 group-hover:scale-110"
          :class="{
            'text-blue-500': color === 'blue',
            'text-red-500': color === 'red',
            'text-yellow-500': color === 'yellow',
            'text-green-500': color === 'green',
            'text-gray-500': color === 'gray'
          }"
        />
      </div>
    </div>
  </component>
</template>

<style scoped>
@keyframes pulse-soft {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.4);
  }
  50% {
    box-shadow: 0 0 0 12px rgba(248, 113, 113, 0);
  }
}

.animate-pulse-soft {
  animation: pulse-soft 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}
</style>