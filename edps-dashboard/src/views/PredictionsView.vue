<template>
  <div class="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] p-6 bg-gradient-to-b from-gray-50 to-gray-100 space-y-12">
    <!-- Prediction Control Panel -->
    <div class="w-full max-w-2xl bg-white p-8 rounded-3xl shadow-xl border border-gray-100 flex flex-col items-center space-y-8 animate-fade-in transition-all hover:shadow-2xl">
      <div class="flex items-center space-x-3">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-8 w-8 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
          <path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" />
          <path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" />
        </svg>
        <h1 class="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-600 to-purple-600">
          Prediction Control Panel
        </h1>
      </div>

      <!-- Action Buttons -->
      <div class="flex flex-col space-y-5 w-full">
        <button
          @click="runPredictions(false)"
          :disabled="running"
          class="w-full bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 text-white py-4 rounded-xl font-semibold text-lg shadow-md transition-all duration-300 disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          <svg v-if="!running || currentMode !== 'predict'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span v-if="!running || currentMode !== 'predict'">Predict Students</span>
          <span v-else-if="currentMode === 'predict'">Predicting...</span>
        </button>

        <button
          @click="runPredictions(true)"
          :disabled="running"
          class="w-full bg-gradient-to-r from-indigo-500 to-indigo-700 hover:from-indigo-600 hover:to-indigo-800 text-white py-4 rounded-xl font-semibold text-lg shadow-md transition-all duration-300 disabled:opacity-50 flex items-center justify-center space-x-2"
        >
          <svg v-if="!running || currentMode !== 'recalculate'" xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          <span v-if="!running || currentMode !== 'recalculate'">Force Recalculate All</span>
          <span v-else-if="currentMode === 'recalculate'">Recalculating All...</span>
        </button>
      </div>

      <!-- Progress Bar -->
      <div v-if="running" class="w-full mt-6 space-y-3 animate-fade-in">
        <div class="h-4 w-full bg-gray-200 rounded-full overflow-hidden relative shadow-inner">
          <div
            class="h-full bg-gradient-to-r from-blue-400 to-blue-600 transition-all duration-300"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <div class="space-y-1 text-center">
          <p class="text-sm font-medium text-gray-600 flex items-center justify-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 animate-spin" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ statusMessage }}
          </p>
          <p class="text-sm text-gray-500 italic transition-all duration-300">{{ wittyMessage }}</p>
        </div>
      </div>

      <!-- Results Summary -->
      <div v-if="lastRunResults && !running" class="w-full bg-gray-50 p-5 rounded-xl border border-gray-200 shadow-sm">
        <h3 class="text-lg font-semibold text-gray-800 mb-3 flex items-center">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2 text-blue-600" viewBox="0 0 20 20" fill="currentColor">
            <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd" />
          </svg>
          Last Run Results
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div class="bg-white p-4 rounded-lg border border-gray-200 shadow-sm">
            <div class="text-sm text-gray-600 mb-1">Total Students</div>
            <div class="text-2xl font-bold text-gray-800">{{ lastRunResults.total }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg border border-green-200 shadow-sm">
            <div class="text-sm text-gray-600 mb-1">Successful</div>
            <div class="text-2xl font-bold text-green-600">{{ lastRunResults.success }}</div>
          </div>
          <div class="bg-white p-4 rounded-lg border border-red-200 shadow-sm">
            <div class="text-sm text-gray-600 mb-1">Failed</div>
            <div class="text-2xl font-bold text-red-600">{{ lastRunResults.failed }}</div>
          </div>
        </div>
        <div class="mt-4 text-sm text-gray-500">
          Completed at: {{ new Date(lastRunResults.timestamp).toLocaleString() }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import api from '@/services/api'
import { ref } from 'vue'
import { useToast } from 'vue-toastification'

const toast = useToast()

const running = ref(false)
const progress = ref(0)
const statusMessage = ref('')
const wittyMessage = ref('')
const currentMode = ref(null)
const lastRunResults = ref(null)

const runPredictions = async (forceAll) => {
  if (running.value) return
  
  running.value = true
  progress.value = 0
  currentMode.value = forceAll ? 'recalculate' : 'predict'
  statusMessage.value = forceAll ? 'Preparing to recalculate all students...' : 'Preparing to predict for new students...'
  
  // Collection of witty messages to display during processing
  const wittyMessages = [
    "Calculating risk factors faster than students calculate excuses...",
    "Brewing coffee for the prediction algorithms...",
    "Checking which students actually attended their 8am lectures...",
    "Teaching neural networks to recognize procrastination patterns...",
    "Convincing the database that we really need this data right now...",
    "Looking for patterns in student behavior (and finding mostly Netflix)...",
    "Converting caffeine into risk predictions...",
    "Analyzing homework submission timestamps (mostly 11:59pm)...",
    "Checking how many times students Googled 'how to pass without studying'...",
    "Counting pizza deliveries to dorm rooms as a risk factor...",
    "Estimating risk based on number of all-nighters pulled...",
    "Predicting which students need a good night's sleep (probably all of them)...",
    "Determining correlation between energy drink consumption and grades...",
    "Searching for excuses in the 'my dog ate my homework' database...",
    "Running numbers faster than students run to class when they're late...",
  ]
  
  let messageIndex = 0
  const totalSeconds = 45 // Target duration in seconds
  const intervalMs = 350 // Update interval in milliseconds
  const totalUpdates = (totalSeconds * 1000) / intervalMs
  const progressIncrement = 90 / totalUpdates // Increment to reach 90% in totalSeconds
  
  // Set initial witty message
  wittyMessage.value = wittyMessages[0]
  
  // Start witty message rotation on a separate timer
  const wittyMessageInterval = setInterval(() => {
    messageIndex = (messageIndex + 1) % wittyMessages.length
    wittyMessage.value = wittyMessages[messageIndex]
  }, 6000) // Change witty message every 6 seconds
  
  // Simulate initial progress up to 90%
  const interval = setInterval(() => {
    if (progress.value < 90) {
      progress.value += progressIncrement
      
      // Update main status message based on progress
      if (progress.value < 20) {
        statusMessage.value = forceAll 
          ? 'Loading student data...' 
          : 'Identifying students for prediction...'
      } else if (progress.value < 40) {
        statusMessage.value = forceAll 
          ? 'Recalculating risk assessments...' 
          : 'Running prediction models...'
      } else if (progress.value < 60) {
        statusMessage.value = 'Analyzing academic patterns...'
      } else if (progress.value < 80) {
        statusMessage.value = 'Processing attendance records...' 
      } else {
        statusMessage.value = 'Finalizing risk calculations...'
      }
    } else {
      clearInterval(interval)
      statusMessage.value = 'Waiting for server to complete processing...'
    }
  }, intervalMs)
  
  try {
    const endpoint = forceAll ? '/predict/recalculate-all' : '/predict/all'
    const response = await api.get(endpoint)
    
    // Clear the witty message interval
    clearInterval(wittyMessageInterval)
    
    // Now that we have the complete response, finish the progress
    statusMessage.value = 'Processing complete! Finalizing results...'
    wittyMessage.value = "All done! Your academic crystal ball is ready."
    progress.value = 100
    
    // Wait a moment before showing completion
    setTimeout(() => {
      if (response.data) {
        completeOperation(forceAll, {
          total: forceAll 
            ? (response.data.predictions_updated_or_created?.length || 0) + (response.data.skipped?.length || 0)
            : (response.data.predictions?.length || 0) + (response.data.skipped?.length || 0),
          success: forceAll 
            ? response.data.predictions_updated_or_created?.length || 0
            : response.data.predictions?.length || 0,
          failed: response.data.skipped?.length || 0,
          timestamp: new Date()
        })
      } else {
        throw new Error('Invalid response from server')
      }
    }, 500)
  } catch (error) {
    clearInterval(interval)
    clearInterval(wittyMessageInterval)
    progress.value = 0
    running.value = false
    currentMode.value = null
    wittyMessage.value = ''
    toast.error(`Failed to run predictions: ${error.message || 'Unknown error'}`)
  }
}

const completeOperation = (wasForceAll, results = null) => {
  setTimeout(() => {
    running.value = false
    currentMode.value = null
    
    if (results) {
      lastRunResults.value = results
    } else {
      // Demo data if API call wasn't implemented
      lastRunResults.value = {
        total: wasForceAll ? 250 : 50,
        success: wasForceAll ? 245 : 48,
        failed: wasForceAll ? 5 : 2,
        timestamp: new Date()
      }
    }
    
    toast.success(wasForceAll 
      ? 'Successfully recalculated risk for all students!' 
      : 'Successfully ran predictions for eligible students!')
      
  }, 500)
}
</script>

<style scoped>
.animate-fade-in {
  animation: fadeIn 0.5s ease-in-out;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
