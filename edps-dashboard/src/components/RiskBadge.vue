<template>
    <span
      :class="badgeClass"
      class="inline-block text-xs font-semibold px-2 py-1 rounded"
    >
      {{ label }}
    </span>
  </template>
  
  <script setup>
  import { computed, toRef } from 'vue'
  
  const props = defineProps({
    score: {
      type: Number,
      required: true,
    },
  })
  
  const score = toRef(props, 'score')
  
  const label = computed(() => {
    if (score.value >= 0.8) return 'High Risk'
    if (score.value >= 0.5) return 'Medium Risk'
    return 'Low Risk'
  })
  
  const badgeClass = computed(() => {
    if (score.value >= 0.8) return 'bg-red-100 text-red-700'
    if (score.value >= 0.5) return 'bg-yellow-100 text-yellow-700'
    return 'bg-green-100 text-green-700'
  })
  </script>
  