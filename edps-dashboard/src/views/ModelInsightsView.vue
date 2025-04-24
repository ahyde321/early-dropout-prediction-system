<template>
    <div class="p-6 space-y-6">
      <h1 class="text-2xl font-bold">📈 Model Insights</h1>
  
      <!-- Phase Selector -->
      <div class="flex items-center space-x-4">
        <label for="phase" class="font-medium">Select Phase:</label>
        <select
          id="phase"
          v-model="selectedPhase"
          class="border rounded px-3 py-1"
          @change="fetchModelInfo"
        >
          <option value="">All Phases</option>
          <option v-for="p in ['early', 'mid', 'final']" :key="p" :value="p">
            {{ p.charAt(0).toUpperCase() + p.slice(1) }}
          </option>
        </select>
      </div>
  
      <!-- Loading -->
      <div v-if="loading" class="text-gray-500">Loading...</div>
  
      <!-- Error -->
      <div v-if="errorMessage" class="text-red-600">{{ errorMessage }}</div>
  
      <!-- Model Info Display -->
      <div v-if="!loading && validModelPhases.length > 0">
        <div
          v-for="([phase, info]) in validModelPhases"
          :key="phase"
          class="border rounded-lg shadow p-4 mb-6"
        >
          <h2 class="text-xl font-semibold mb-2 capitalize">{{ phase }} Model</h2>
  
          <div class="grid grid-cols-2 gap-4 mb-4">
            <!-- Metrics Section -->
            <div>
              <h3 class="font-semibold mb-1">Performance Metrics</h3>
              <ul
                v-if="info.metrics && Object.keys(info.metrics).length > 0"
                class="list-disc list-inside text-sm"
              >
                <li v-for="(value, key) in info.metrics" :key="key">
                  {{ key }}: {{ value }}
                </li>
              </ul>
              <p v-else class="text-sm text-gray-500">No metrics available.</p>
            </div>
  
            <!-- Feature Importance -->
            <div>
              <h3 class="font-semibold mb-1">Feature Importance</h3>
              <FeatureBarChart :data="info.feature_importance" />
            </div>
          </div>
        </div>
      </div>
  
      <!-- No Valid Data -->
      <div
        v-if="!loading && validModelPhases.length === 0 && !errorMessage"
        class="text-gray-500"
      >
        No valid model data available.
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed, onMounted } from "vue"
  import axios from "axios"
  import FeatureBarChart from "@/components/ModelFeatureChart.vue"
  
  const selectedPhase = ref("")
  const modelInfo = ref({})
  const loading = ref(false)
  const errorMessage = ref("")
  
  const fetchModelInfo = async () => {
    loading.value = true
    errorMessage.value = ""
    try {
      const url = selectedPhase.value
        ? `/api/model/info/${selectedPhase.value}`
        : `/api/model/info`
  
      const res = await axios.get(url)
      modelInfo.value = selectedPhase.value
        ? { [selectedPhase.value]: res.data }
        : res.data
  
      // ✅ Debug output
      console.log("🌐 Raw modelInfo:", res.data)
      console.log("✅ Filtered valid phases:", validModelPhases.value)
  
    } catch (err) {
      console.error("Failed to load model info", err)
      errorMessage.value = "Unable to load model insights. Please try again later."
      modelInfo.value = {}
    } finally {
      loading.value = false
    }
  }
  
  const validModelPhases = computed(() =>
    Object.entries(modelInfo.value).filter(([_, info]) => {
      return (
        info &&
        typeof info === "object" &&
        info.feature_importance &&
        typeof info.feature_importance === "object" &&
        Object.keys(info.feature_importance).length > 0
      )
    })
  )
  
  onMounted(fetchModelInfo)
  </script>
  
  