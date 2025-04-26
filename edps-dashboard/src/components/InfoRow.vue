<template>
  <div class="flex flex-col gap-1">
    <label class="text-gray-600 font-medium">{{ label }}</label>
    <div v-if="editable">
      <input
        v-model="localValue"
        @input="$emit('update:modelValue', localValue)"
        class="border border-gray-300 rounded-lg p-2 text-sm w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        type="text"
      />
    </div>
    <div v-else class="text-gray-800">
      {{ value }}
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  label: String,
  value: [String, Number],
  editable: Boolean,
  modelValue: [String, Number]
})

const emit = defineEmits(['update:modelValue'])

const localValue = ref(props.modelValue)
watch(() => props.modelValue, (newVal) => {
  localValue.value = newVal
})
</script>
