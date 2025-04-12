<template>
    <div class="relative">
      <!-- Trigger Button -->
      <button
        @click="toggle"
        class="flex items-center gap-2 text-sm font-medium px-3 py-1.5 rounded-full border border-gray-300 bg-white hover:bg-sky-50 shadow transition-all focus:outline-none focus:ring-2 focus:ring-sky-300"
      >
        <slot name="icon" />
      </button>
  
      <!-- Backdrop -->
      <div
        v-if="open"
        @click="toggle"
        class="fixed inset-0 z-40 bg-black bg-opacity-10 backdrop-blur-sm transition-opacity duration-200"
      ></div>
  
      <!-- Panel -->
      <div
        v-if="open"
        @click.stop
        class="fixed z-50 bg-white border border-gray-200 rounded-xl shadow-lg p-4 right-6 top-24 w-72 space-y-4 transition-all"
        >

        <div class="flex flex-col gap-2">
          <label class="text-sm font-medium text-gray-600">Filter Field</label>
          <select
            v-model="localField"
            @change="loadFilterValues"
            class="text-sm px-3 py-2 border rounded-md bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-300"
          >
            <option disabled value="">Select Field</option>
            <option v-for="(label, key) in fields" :key="key" :value="key">
              {{ label }}
            </option>
          </select>
        </div>
  
        <div class="flex flex-col gap-2">
          <label class="text-sm font-medium text-gray-600">Filter Value</label>
          <select
            v-model="localValue"
            :disabled="!filterValues.length"
            class="text-sm px-3 py-2 border rounded-md bg-white shadow-sm focus:outline-none focus:ring-2 focus:ring-sky-300"
          >
            <option disabled value="">Select Value</option>
            <option v-for="val in filterValues" :key="val" :value="val">
              {{ format(val) }}
            </option>
          </select>
        </div>
  
        <div class="flex justify-end gap-2 pt-2">
          <button @click="reset" class="text-xs text-gray-500 hover:underline">
            Reset
          </button>
          <button
            @click="apply"
            class="text-sm px-3 py-1.5 rounded-md bg-sky-500 text-white hover:bg-sky-600 transition"
          >
            Apply
          </button>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import api from '@/services/api'
  
  const props = defineProps({
    fields: Object,
    format: {
      type: Function,
      default: (val) => val
    },
    modelValue: {
      type: Object,
      default: () => ({ field: '', value: '' })
    }
  })
  
  const emit = defineEmits(['update:modelValue'])
  
  const open = ref(false)
  const filterValues = ref([])
  const localField = ref(props.modelValue.field)
  const localValue = ref(props.modelValue.value)
  
  const toggle = () => (open.value = !open.value)
  
  const reset = () => {
    localField.value = ''
    localValue.value = ''
    filterValues.value = []
    emit('update:modelValue', { field: '', value: '' })
    toggle()
  }
  
  const apply = () => {
    emit('update:modelValue', {
      field: localField.value,
      value: localValue.value
    })
    toggle()
  }
  
  const loadFilterValues = async () => {
    localValue.value = ''
    try {
      const { data } = await api.get('/students/distinct-values', {
        params: { field: localField.value }
      })
      filterValues.value = data
    } catch (err) {
      console.error('❌ Error loading filter values:', err)
    }
  }
  
  watch(() => props.modelValue, (val) => {
    localField.value = val.field
    localValue.value = val.value
  })
  </script>
  