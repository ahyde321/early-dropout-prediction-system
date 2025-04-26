<template>
    <div class="flex flex-col gap-1">
      <label class="text-gray-600 font-medium">{{ label }}</label>
      <div v-if="editable">
        <select
          v-model="localValue"
          @change="updateModel"
          class="border border-gray-300 rounded-lg p-2 text-sm w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
        >
          <option v-for="(text, key) in options" :key="key" :value="String(key)">
            {{ text }}
          </option>
        </select>
      </div>
      <div v-else class="text-gray-800">
        {{ options[String(modelValue)] ?? 'N/A' }}
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  
  const props = defineProps({
    label: String,
    editable: Boolean,
    modelValue: [String, Number, Boolean],
    options: Object
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  const localValue = ref(String(props.modelValue ?? ''))
  
  watch(() => props.modelValue, (val) => {
    localValue.value = String(val ?? '')
  })
  
  function updateModel() {
    let val = localValue.value
  
    if (val === 'true') emit('update:modelValue', true)
    else if (val === 'false') emit('update:modelValue', false)
    else if (!isNaN(val) && Object.keys(props.options).includes('0')) emit('update:modelValue', parseInt(val))
    else emit('update:modelValue', val)
  }
  </script>
  