<template>
  <div class="bg-white border rounded-xl p-4 shadow-sm">
    <h4 class="text-md font-semibold text-gray-800 mb-4 flex items-center gap-2">
      🧠 Top Contributing Features
    </h4>

    <div v-if="topFeatures.length">
      <div
        v-for="(item, index) in topFeatures"
        :key="index"
        class="flex justify-between items-center py-1.5 border-b last:border-none"
      >
        <span class="text-gray-700 text-sm truncate">
          {{ formatLabel(item.feature) }}
        </span>
        <span
          class="text-xs font-semibold px-2 py-1 rounded-lg min-w-[64px] text-center"
          :class="item.value > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
        >
          {{ item.value.toFixed(3) }}
        </span>
      </div>
    </div>

    <div v-else class="text-sm text-gray-400 italic">
      No SHAP explanation available.
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  shapValues: {
    type: Object,
    required: true
  },
  topN: {
    type: Number,
    default: 5
  }
})

const topFeatures = computed(() => {
  if (!props.shapValues) return []
  return Object.entries(props.shapValues)
    .map(([feature, value]) => ({ feature, value }))
    .sort((a, b) => Math.abs(b.value) - Math.abs(a.value))
    .slice(0, props.topN)
})

function formatLabel(label) {
  return label.replace(/_/g, ' ').replace(/\b\w/g, (c) => c.toUpperCase())
}
</script>
