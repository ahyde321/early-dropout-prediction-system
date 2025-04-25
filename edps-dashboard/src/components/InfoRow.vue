<!-- InfoRow.vue -->
<template>
    <div class="flex flex-col">
      <span class="text-xs font-medium text-gray-500">{{ label }}</span>
      <span class="text-sm text-gray-800">{{ value ?? '—' }}</span>
    </div>
  </template>
  
  <script setup>
  defineProps({
    label: String,
    value: [String, Number]
  })
  </script>
  