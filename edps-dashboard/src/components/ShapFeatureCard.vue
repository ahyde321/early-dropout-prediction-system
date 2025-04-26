<template>
  <div class="bg-gradient-to-br from-white to-gray-50 p-5 rounded-xl shadow-sm">
    <h4 class="text-lg font-bold text-gray-800 mb-5 border-b pb-2">
      Top Contributing Features
    </h4>

    <div v-if="topFeatures.length" class="space-y-3">
      <div
        v-for="(item, index) in topFeatures"
        :key="index"
        class="flex justify-between items-center py-1 px-2 hover:bg-gray-100 rounded-lg transition-all"
      >
        <span class="text-gray-700 text-[13px] font-medium truncate">
          {{ formatLabel(item.feature) }}
        </span>
        <span
          class="text-xs font-semibold px-3 py-1 rounded-full min-w-[60px] text-center shadow-sm"
          :class="item.value > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
        >
          {{ item.value.toFixed(3) }}
        </span>
      </div>
    </div>

    <div v-else class="text-sm text-gray-400 italic text-center py-6">
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