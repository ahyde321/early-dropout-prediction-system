<template>
  <div class="flex items-center justify-center min-h-[calc(100vh-80px)] px-4 py-10">
    <div
      class="w-full max-w-2xl bg-white p-8 rounded-2xl shadow-2xl transition-all duration-500 ease-in-out opacity-0 scale-95"
      ref="uploadCard"
    >
      <h2 class="text-2xl font-bold mb-6 text-gray-800 text-center">📄 Upload Student CSV</h2>

      <!-- Drag & Drop Area -->
      <div
        class="w-full h-40 border-2 border-dashed border-blue-400 rounded-xl flex items-center justify-center text-gray-500 text-sm mb-6 cursor-pointer hover:border-blue-600 transition-all"
        @dragover.prevent
        @drop.prevent="handleDrop"
        @click="fileInput.click()"
      >
        <span v-if="!fileName">Drag & drop or click to select a .csv file</span>
        <span v-else class="text-blue-600">📎 Selected: {{ fileName }}</span>
        <input
          type="file"
          accept=".csv"
          class="hidden"
          ref="fileInput"
          @change="handleFile"
        />
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-between gap-3 mb-4">
        <button
          class="w-1/2 bg-gray-100 text-gray-700 py-2 rounded hover:bg-gray-200 transition"
          @click="resetFile"
          :disabled="!csvFile"
        >
          Reset
        </button>

        <button
          class="w-1/2 bg-blue-600 text-white py-2 rounded hover:bg-blue-700 transition disabled:opacity-50"
          @click="upload"
          :disabled="!csvFile"
        >
          Upload
        </button>
      </div>

      <!-- Upload Feedback -->
      <p v-if="uploaded && uploadSummary?.added === 0" class="text-yellow-600 text-sm text-center mt-1">⚠️ All records were skipped</p>
      <p v-if="fullRows?.length > 1" class="text-xs text-gray-500 text-center mt-2">
        {{ fullRows.length - 1 }} records ready to upload
      </p>

      <!-- Upload Summary -->
      <div v-if="uploadSummary" class="mt-6 text-sm text-gray-700">
        <div class="border rounded-lg p-4 bg-gray-50">
          <h3 class="font-semibold text-base mb-4 text-gray-800">Upload Results</h3>
          <div class="grid grid-cols-3 gap-4 text-center">
            <div class="bg-green-100 text-green-700 rounded p-2">
              <div class="font-medium text-lg">{{ uploadSummary.added || 0 }}</div>
              <div class="text-xs">Added</div>
            </div>
            <div class="bg-yellow-100 text-yellow-800 rounded p-2">
              <div class="font-medium text-lg">{{ uploadSummary.skipped || 0 }}</div>
              <div class="text-xs">Skipped</div>
            </div>
            <div class="bg-red-100 text-red-700 rounded p-2">
              <div class="font-medium text-lg">{{ uploadSummary.failed || 0 }}</div>
              <div class="text-xs">Failed</div>
            </div>
          </div>
        </div>

        <!-- Skipped Pagination -->
        <div v-if="uploadSummary.details && uploadSummary.details.skipped && uploadSummary.details.skipped.length" class="mt-6">
          <PaginatedList :items="uploadSummary.details.skipped" label="Duplicate student_number" />
        </div>

        <!-- Failed Pagination -->
        <div v-if="uploadSummary.details && uploadSummary.details.failures && uploadSummary.details.failures.length" class="mt-6">
          <PaginatedList :items="uploadSummary.details.failures" label="Failure reason" />
        </div>
      </div>

      <!-- CSV Preview -->
      <div v-if="preview?.length" class="mt-6 text-sm">
        <h3 class="font-semibold mb-2 text-gray-700">🔍 CSV Preview (first 5 rows)</h3>
        <div class="overflow-x-auto border rounded">
          <table class="min-w-full text-left text-sm text-gray-700 border-collapse">
            <thead class="bg-gray-100">
              <tr>
                <th
                  v-for="(col, index) in preview[0]"
                  :key="'header-' + index"
                  class="px-3 py-2 border-b"
                >
                  {{ col }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(row, rIndex) in preview.slice(1, 6)"
                :key="'row-' + rIndex"
                class="hover:bg-gray-50"
              >
                <td
                  v-for="(value, cIndex) in row"
                  :key="'cell-' + rIndex + '-' + cIndex"
                  class="px-3 py-2 border-b"
                >
                  {{ value }}
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Papa from 'papaparse'
import { useToast } from 'vue-toastification'
import PaginatedList from '@/components/PaginatedList.vue'

const toast = useToast()
const baseURL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const csvFile = ref(null)
const fileName = ref('')
const fileInput = ref(null)
const preview = ref([])
const uploaded = ref(false)
const uploadSummary = ref(null)
const fullRows = ref([])
const uploadCard = ref(null)

onMounted(() => {
  requestAnimationFrame(() => {
    uploadCard.value.classList.remove('opacity-0', 'scale-95')
    uploadCard.value.classList.add('opacity-100', 'scale-100')
  })
})

function handleFile(event) {
  const file = event.target.files[0]
  processFile(file)
}

function handleDrop(event) {
  const file = event.dataTransfer.files[0]
  processFile(file)
}

function processFile(file) {
  if (!file || !file.name.endsWith('.csv')) {
    toast.error('❌ Please upload a valid .csv file')
    resetFile()
    return
  }

  if (file.size > 2 * 1024 * 1024) {
    toast.error('🚫 File too large (max 2MB)')
    resetFile()
    return
  }

  csvFile.value = file
  fileName.value = file.name
  uploaded.value = false
  uploadSummary.value = null

  Papa.parse(file, {
    header: false,
    complete: (results) => {
      fullRows.value = results.data.filter(row => Array.isArray(row) && row.some(cell => cell !== ""))
      preview.value = fullRows.value.slice(0, 6)
    },
    error: () => {
      toast.error('❌ Failed to parse CSV preview')
      resetFile()
    }
  })

  fileInput.value.value = ''
}

function resetFile() {
  csvFile.value = null
  fileName.value = ''
  preview.value = []
  fullRows.value = []
  uploaded.value = false
  uploadSummary.value = null
  fileInput.value.value = ''
}

async function upload() {
  if (!csvFile.value) return

  const formData = new FormData()
  formData.append('file', csvFile.value)

  try {
    const { data } = await axios.post(`${baseURL.replace(/\/$/, '')}/api/upload/students`, formData)
    uploaded.value = true
    uploadSummary.value = data

    if (data.added > 0) {
      toast.success('✅ Upload successful!')
    } else {
      toast.warning('⚠️ All records were skipped')
    }
  } catch (err) {
    uploaded.value = false
    uploadSummary.value = null

    const message =
      err?.response?.data?.detail ||
      err?.response?.data?.message ||
      err?.message ||
      '❌ Upload failed due to an unknown error'

    toast.error(message)
    console.error('Upload error:', err)
  }
}
</script>
