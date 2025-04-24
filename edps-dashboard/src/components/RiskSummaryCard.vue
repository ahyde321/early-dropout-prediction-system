<template>
  <component
    :is="to ? 'RouterLink' : 'div'"
    :to="to"
    class="block cursor-pointer hover:scale-[1.02] transition-transform duration-300"
  >
    <div
      :class="cardClasses"
      class="flex items-center justify-between gap-6 relative z-10 overflow-hidden"
    >
      <!-- Left Text Block -->
      <div class="relative">
        <p class="text-sm font-medium text-gray-600 mb-1">{{ label }}</p>
        <p
          class="text-4xl font-extrabold tracking-tight"
          :class="{
            'text-sky-600': color === 'blue',
            'text-rose-600': color === 'red',
            'text-amber-600': color === 'yellow',
            'text-emerald-600': color === 'green',
            'text-gray-800': color === 'gray'
          }"
        >
          {{ displayValue }}
        </p>
      </div>

      <!-- Icon Bubble -->
      <div class="relative">
        <div
          class="w-12 h-12 rounded-full flex items-center justify-center shadow-inner ring-2"
          :class="{
            'bg-sky-100 text-sky-600 ring-sky-200': color === 'blue',
            'bg-rose-100 text-rose-600 ring-rose-200': color === 'red',
            'bg-amber-100 text-amber-600 ring-amber-200': color === 'yellow',
            'bg-emerald-100 text-emerald-600 ring-emerald-200': color === 'green',
            'bg-gray-100 text-gray-600 ring-gray-200': color === 'gray'
          }"
        >
          <component :is="iconComponent" class="w-5 h-5" />
        </div>
      </div>
    </div>
  </component>
</template>

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
    validator: val =>
      ['blue', 'red', 'yellow', 'green', 'gray'].includes(val)
  },
  trend: { type: Number, default: null },
  to: { type: String, default: null }
})

const { label, value, color, to } = toRefs(props)

const cardClasses = computed(() => {
  const styles = {
    blue: 'bg-sky-50 border-sky-200 ring-sky-100 shadow-sky-100/50',
    red: 'bg-rose-50 border-rose-200 ring-rose-100 shadow-rose-100/50',
    yellow: 'bg-amber-50 border-amber-200 ring-amber-100 shadow-amber-100/50',
    green: 'bg-emerald-50 border-emerald-200 ring-emerald-100 shadow-emerald-100/50',
    gray: 'bg-gray-50 border-gray-200 ring-gray-100 shadow-gray-100/50'
  }
  return `${styles[color.value] || styles.gray} border p-5 rounded-2xl shadow-md group hover:ring-2 transition-all duration-300 ease-in-out`
})

const iconComponent = computed(() => {
  switch (color.value) {
    case 'red':
      return AlertCircle
    case 'yellow':
      return TriangleAlert
    case 'green':
      return CheckCircle
    case 'blue':
      return BarChart2
    default:
      return Info
  }
})

const displayValue = ref(0)
const animateCounter = () => {
  const duration = 1000
  const startTime = performance.now()
  const start = displayValue.value
  const end = value.value
  const step = now => {
    const progress = Math.min((now - startTime) / duration, 1)
    const easeOutQuart = 1 - Math.pow(1 - progress, 4)
    displayValue.value = Math.floor(easeOutQuart * (end - start) + start)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}
watch(value, animateCounter, { immediate: true })
</script>
