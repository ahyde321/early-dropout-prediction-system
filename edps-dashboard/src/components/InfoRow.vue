<template>
  <div class="space-y-1">
    <label class="block text-sm font-medium text-gray-700">{{ label }}</label>
    <div v-if="!editable" class="text-gray-800 font-medium bg-gray-50 px-3 py-2 rounded-md">
      {{ value }}
    </div>
    <input
      v-else
      v-model="modelValue"
      type="text"
      class="input"
      :placeholder="label"
    />
  </div>
</template>

<script setup>
defineProps({
  label: String,
  value: [String, Number],
  editable: Boolean
})

const modelValue = defineModel()
</script>

<style scoped>
.input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-300 transition-colors;
}
</style>
