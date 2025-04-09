<template>
    <div class="p-6 max-w-2xl mx-auto">
      <h2 class="text-2xl font-semibold mb-4">Upload CSV</h2>
  
      <input
        type="file"
        accept=".csv"
        @change="handleFile"
        class="block mb-4"
      />
  
      <button
        class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
        @click="upload"
        :disabled="!csvFile"
      >
        Upload
      </button>
  
      <p v-if="fileName" class="mt-2 text-sm text-gray-600">Selected: {{ fileName }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref } from 'vue'
  import axios from 'axios'
  import { useToast } from 'vue-toastification'
  const toast = useToast()
  toast.success('✅ File uploaded')
  toast.error('❌ Upload failed')

  
  const csvFile = ref(null)
  const fileName = ref('')
  
  function handleFile(event) {
    const file = event.target.files[0]
    if (!file) return
  
    if (!file.name.endsWith('.csv')) {
      toast.error('Please upload a .csv file')
      csvFile.value = null
      fileName.value = ''
      return
    }
  
    csvFile.value = file
    fileName.value = file.name
  }
  
  async function upload() {
    const formData = new FormData()
    formData.append('file', csvFile.value)
  
    try {
      await axios.post('http://localhost:8000/students/upload', formData)
      toast.success('✅ Upload successful!')
    } catch (err) {
      toast.error('❌ Upload failed')
    }
  }
  </script>
  