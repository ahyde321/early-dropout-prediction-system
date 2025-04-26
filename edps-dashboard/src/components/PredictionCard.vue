<template>
  <div class="bg-white border border-gray-200 rounded-xl p-6 shadow-sm hover:shadow-md transition-shadow duration-300">
    <div class="flex justify-between items-start mb-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-800">{{ phaseLabel }} Phase</h3>
        <p class="text-sm text-gray-500">{{ formatTimestamp(timestamp) }}</p>
      </div>
      <div class="flex items-center gap-2">
        <span :class="[
          'px-3 py-1 rounded-full text-sm font-medium',
          riskColor
        ]">
          {{ riskLabel }} Risk
        </span>
        <div class="w-24 h-2 bg-gray-200 rounded-full overflow-hidden">
          <div
            :class="[
              'h-full transition-all duration-500',
              riskColor
            ]"
            :style="{ width: `${score}%` }"
          ></div>
        </div>
        <span class="text-sm font-medium text-gray-700">{{ score.toFixed(1) }}%</span>
        <button 
          @click="isExpanded = !isExpanded"
          class="ml-4 text-gray-500 hover:text-gray-700 transition-colors"
        >
          <svg 
            xmlns="http://www.w3.org/2000/svg" 
            class="h-5 w-5 transform transition-transform duration-200" 
            :class="{ 'rotate-180': isExpanded }"
            fill="none" 
            viewBox="0 0 24 24" 
            stroke="currentColor"
          >
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
          </svg>
        </button>
      </div>
    </div>
    <transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="transform scale-95 opacity-0"
      enter-to-class="transform scale-100 opacity-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="transform scale-100 opacity-100"
      leave-to-class="transform scale-95 opacity-0"
    >
      <div v-show="isExpanded" class="mt-4">
        <slot></slot>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  phaseLabel: String,
  riskLabel: String,
  score: Number,
  timestamp: String
})

const isExpanded = ref(false)

const riskColor = computed(() => {
  const risk = props.riskLabel.toLowerCase()
  return {
    high: 'bg-red-100 text-red-800',
    moderate: 'bg-yellow-100 text-yellow-800',
    low: 'bg-green-100 text-green-800'
  }[risk] || 'bg-gray-100 text-gray-800'
})

const formatTimestamp = (timestamp) => {
  return new Date(timestamp).toLocaleString()
}
</script>