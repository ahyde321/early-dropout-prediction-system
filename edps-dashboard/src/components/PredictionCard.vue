<template>
    <div class="bg-white border border-gray-200 rounded-xl p-5 shadow-md hover:shadow-lg transition-transform hover:scale-[1.01]">
      <!-- Header -->
      <div class="flex justify-between items-start">
        <div>
          <p class="text-md font-extrabold text-gray-900">Phase: {{ phaseLabel }}</p>
          <p :class="riskColorClass" class="text-sm mt-1">Level: {{ riskLabel }}</p>
        </div>
        <div class="text-right text-gray-500 text-xs">
          <p><span class="font-semibold">Score:</span> {{ score.toFixed(2) }}%</p>
          <p class="text-[11px] mt-1">{{ formattedShortTimestamp }}</p>
        </div>
      </div>
  
      <!-- Toggle Button -->
      <div class="flex justify-end mt-3">
        <button
          @click="toggleExpand"
          class="text-indigo-600 hover:text-indigo-800 text-xs font-bold flex items-center gap-1 transition"
        >
          <span>{{ expanded ? 'Hide Explanation' : 'Show Explanation' }}</span>
          <span :class="['transition-transform', expanded ? 'rotate-180' : '']">⌄</span>
        </button>
      </div>
  
      <!-- Expandable Slot Area -->
      <transition name="fade">
        <div v-if="expanded" class="mt-4">
          <slot />
        </div>
      </transition>
    </div>
  </template>
  
  <script setup>
  import { computed, ref } from 'vue'
  
  const props = defineProps({
    phaseLabel: {
      type: String,
      required: true
    },
    riskLabel: {
      type: String,
      required: true
    },
    score: {
      type: Number,
      required: true
    },
    timestamp: {
      type: String,
      required: true
    }
  })
  
  const expanded = ref(false)
  const toggleExpand = () => {
    expanded.value = !expanded.value
  }
  
  const riskColorClass = computed(() => {
    return {
      Low: 'text-green-600 font-bold',
      Moderate: 'text-yellow-500 font-bold',
      High: 'text-red-600 font-bold'
    }[props.riskLabel] || 'text-gray-600'
  })
  
  const formattedShortTimestamp = computed(() => {
    const date = new Date(props.timestamp)
    const hours = String(date.getHours()).padStart(2, '0')
    const minutes = String(date.getMinutes()).padStart(2, '0')
    return `${hours}:${minutes}`
  })
  </script>
  
  <style scoped>
  .fade-enter-active, .fade-leave-active {
    transition: all 0.3s ease;
  }
  .fade-enter-from, .fade-leave-to {
    opacity: 0;
    transform: translateY(-4px);
  }
  .rotate-180 {
    transform: rotate(180deg);
  }
  </style>