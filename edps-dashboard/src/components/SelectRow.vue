<template>
  <div class="space-y-1">
    <label class="block text-sm font-medium text-gray-700">{{ label }}</label>
    <div v-if="!editable" class="text-gray-800 font-medium bg-gray-50 px-3 py-2 rounded-md">
      {{ displayValue }}
    </div>
    <select
      v-else
      v-model="modelValue"
      class="input"
    >
      <option v-for="(value, key) in options" :key="key" :value="key">
        {{ value }}
      </option>
    </select>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: String,
  options: Object,
  editable: Boolean,
  modelValue: [String, Number, Boolean]
})

const emit = defineEmits(['update:modelValue'])

const modelValue = computed({
  get: () => props.modelValue,
  set: (value) => {
    // Convert string values to appropriate types
    if (value === 'true') emit('update:modelValue', true)
    else if (value === 'false') emit('update:modelValue', false)
    else if (!isNaN(value) && Object.keys(props.options).includes('0')) emit('update:modelValue', parseInt(value))
    else emit('update:modelValue', value)
  }
})

const displayValue = computed(() => {
  const value = props.modelValue
  if (value === true || value === 'true') return props.options['1']
  if (value === false || value === 'false') return props.options['0']
  return props.options[value] || value
})
</script>

<style scoped>
.input {
  @apply w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-sky-300 transition-colors;
}
</style>
