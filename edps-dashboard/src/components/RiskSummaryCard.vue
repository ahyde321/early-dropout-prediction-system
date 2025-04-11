<script setup>
import {
  toRefs,
  computed,
  ref,
  watch,
  onMounted,
  nextTick
} from 'vue'
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

const isHovered = ref(false)
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
    blue: 'from-blue-100 to-blue-50 border-blue-200 ring-blue-200 shadow-blue-100',
    red: 'from-red-100 to-red-50 border-red-200 ring-red-300 shadow-red-100 animate-pulse-soft',
    yellow: 'from-yellow-100 to-yellow-50 border-yellow-200 ring-yellow-200 shadow-yellow-100',
    green: 'from-green-100 to-green-50 border-green-200 ring-green-200 shadow-green-100',
    gray: 'from-gray-100 to-gray-50 border-gray-200 ring-gray-200 shadow-gray-100'
  }
  return `bg-gradient-to-br ${bg[color.value] || bg.gray} border p-4 rounded-2xl shadow-md group hover:ring-2 transition-all`
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
  const duration = 600
  const startTime = performance.now()
  const start = displayValue.value
  const end = value.value
  const step = (now) => {
    const progress = Math.min((now - startTime) / duration, 1)
    displayValue.value = Math.floor(progress * (end - start) + start)
    if (progress < 1) requestAnimationFrame(step)
  }
  requestAnimationFrame(step)
}
watch(value, animateCounter, { immediate: true })

// === Tooltip Positioning Logic ===
const iconRef = ref(null)
const tooltipStyle = ref({ top: '0px', left: '0px' })

const updateTooltipPosition = () => {
  nextTick(() => {
    if (iconRef.value) {
      const rect = iconRef.value.getBoundingClientRect()
      tooltipStyle.value = {
        top: `${rect.top - 36}px`, // place above
        left: `${rect.left + rect.width / 2}px`, // center horizontally
        transform: 'translateX(-50%)',
        position: 'fixed'
      }
    }
  })
}

onMounted(() => {
  updateTooltipPosition()
  window.addEventListener('scroll', updateTooltipPosition)
  window.addEventListener('resize', updateTooltipPosition)
})
</script>


<template>
  <component :is="to ? 'RouterLink' : 'div'" :to="to" class="block cursor-pointer hover:scale-[1.01] transition-transform duration-200">
  <div
    :class="cardClasses"
    class="flex items-center justify-between gap-4 relative z-10"
    @mouseenter="() => { isHovered = true; updateTooltipPosition(); }"
    @mouseleave="isHovered = false"
  >
    <div>
      <p class="text-sm text-gray-600">{{ label }}</p>
      <p class="text-3xl font-extrabold text-gray-900 tracking-tight">
        {{ displayValue }}
      </p>
    </div>

    <div class="relative z-50">
      <component
        :is="iconComponent"
        ref="iconRef"
        class="w-9 h-9 text-gray-700 drop-shadow"
      />
    </div>

    <Teleport to="body">
      <div
        v-if="tooltipText && isHovered"
        class="fixed px-3 py-1 text-xs text-white bg-gray-800 rounded shadow-lg transition-opacity duration-200 z-50"
        :style="tooltipStyle"
      >
        {{ tooltipText }}
      </div>
    </Teleport>
  </div>
</component>
</template>

<style scoped>
@keyframes pulse-soft {
  0%, 100% {
    box-shadow: 0 0 0 0 rgba(248, 113, 113, 0.4);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(248, 113, 113, 0);
  }
}

.animate-pulse-soft {
  animation: pulse-soft 1.8s infinite;
}
</style>
