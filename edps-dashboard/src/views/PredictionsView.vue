<template>
  <div class="flex flex-col items-center justify-center min-h-[calc(100vh-80px)] p-8 bg-gray-100 space-y-12">
    <!-- Prediction Control Panel -->
    <div class="w-full max-w-2xl bg-white p-10 rounded-3xl shadow-2xl flex flex-col items-center space-y-8 animate-fade-in">
      <h1 class="text-3xl font-bold text-gray-800 text-center">
        Prediction Control Panel
      </h1>

      <!-- Action Buttons -->
      <div class="flex flex-col space-y-5 w-full">
        <button
          @click="runPredictions(false)"
          :disabled="running"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-xl font-semibold text-lg shadow transition-all duration-300 disabled:opacity-50"
        >
          <span v-if="!running || currentMode !== 'predict'">Predict Students</span>
          <span v-else-if="currentMode === 'predict'">⏳ Predicting...</span>
        </button>

        <button
          @click="runPredictions(true)"
          :disabled="running"
          class="w-full bg-indigo-600 hover:bg-indigo-700 text-white py-4 rounded-xl font-semibold text-lg shadow transition-all duration-300 disabled:opacity-50"
        >
          <span v-if="!running || currentMode !== 'recalculate'">Force Recalculate All</span>
          <span v-else-if="currentMode === 'recalculate'">⏳ Recalculating All...</span>
        </button>
      </div>

      <!-- Progress Bar -->
      <div v-if="running" class="w-full mt-6 space-y-3 animate-fade-in">
        <div class="h-3 w-full bg-gray-300 rounded-full overflow-hidden relative">
          <div
            class="h-full bg-gradient-to-r from-blue-400 to-blue-600 animate-gradient-x"
            :style="{ width: `${progress}%` }"
          ></div>
        </div>
        <p class="text-sm text-gray-600 text-center flex items-center justify-center gap-2 animate-pulse">
          <span class="spinner"></span>
          {{ statusMessage }}
        </p>
      </div>

      <!-- Results Summary -->
      <div v-if="!running && results" class="w-full mt-8 space-y-8 animate-fade-in">
        <div class="text-center">
          <h2 class="text-2xl font-bold text-gray-700 mb-2">✅ Prediction Summary</h2>
          <p class="text-md text-gray-600">
            Mode: 
            <span class="font-semibold">
              {{ currentMode === 'recalculate' ? 'Full Recalculation' : 'Predict Missing' }}
            </span>
          </p>
        </div>

        <div class="grid grid-cols-2 gap-6">
          <div class="bg-green-100 text-green-700 rounded-xl p-5 text-center shadow">
            <div class="text-2xl font-bold">
              {{
                currentMode === 'recalculate'
                  ? results.predictions_updated_or_created.length
                  : results.predictions.length
              }}
            </div>
            <div class="text-xs uppercase tracking-wider font-semibold mt-2">Predicted</div>
          </div>
          <div class="bg-red-100 text-red-700 rounded-xl p-5 text-center shadow">
            <div class="text-2xl font-bold">{{ results.skipped.length }}</div>
            <div class="text-xs uppercase tracking-wider font-semibold mt-2">Skipped</div>
          </div>
        </div>

        <p class="text-xs text-gray-500 text-center mt-2">
          Tip: Skipped = Students who already had up-to-date predictions.
        </p>
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
const results = ref(null)
const currentMode = ref('predict')

async function runPredictions(forceRecalculate = false) {
  running.value = true
  progress.value = 0
  results.value = null
  currentMode.value = forceRecalculate ? 'recalculate' : 'predict'

  try {
    const endpoint = forceRecalculate ? '/predict/recalculate-all' : '/predict/all'

    // 1. Start both loading bar and API call at the SAME time
    const apiPromise = api.get(endpoint)
    const loadingPromise = simulateLoadingStep()

    // 2. Wait for BOTH to finish
    const [{ data }] = await Promise.all([apiPromise, loadingPromise])

    results.value = data

    // === Smarter toast ===
    const created = data.predictions?.length || data.predictions_updated_or_created?.length || 0
    const skipped = data.skipped?.length || 0

    if (created === 0 && skipped > 0) {
      toast.warning('⚠️ No new predictions created (all students were already predicted)')
    } else {
      toast.success(`✅ Predictions completed: ${created} updated, ${skipped} skipped.`)
    }

  } catch (err) {
    toast.error('❌ Prediction run failed')
    console.error(err)
  } finally {
    running.value = false
  }
}

async function simulateLoadingStep() {
  const funnyStatusMessages = [
    "🧹 Dusting off student records...",
    "🔍 Looking for missing coursework...",
    "🐢 Warming up the prediction engines...",
    "📚 Reading every assignment ever submitted...",
    "🎯 Target acquired: High risk students!",
    "🤔 Overthinking each grade by 300%...",
    "🧪 Mixing up a prediction potion...",
    "✍️ Writing stern emails to hypothetical students...",
    "🔮 Gazing into the academic crystal ball...",
    "📈 Plotting dropout probability curves...",
    "🚀 Preparing risk scores for liftoff...",
    "🧹 Sweeping up final scores...",
    "🎉 Celebrating successful predictions...",
    "📝 Filing paperwork with imaginary university admin...",
    "🕵️‍♂️ One last check for sneaky dropouts..."
  ]

  const totalDuration = 20000 // aim for 95% in ~20 seconds
  const updateInterval = 500   // update every 500ms
  const steps = totalDuration / updateInterval
  const progressIncrement = 95 / steps

  statusMessage.value = "Starting prediction process... 🤖"

  let nextFunnyUpdate = 10 + Math.random() * 10 // every 10-20% update a funny message

  while (progress.value < 95) {
    await new Promise(resolve => setTimeout(resolve, updateInterval))

    // Slight random fluctuation to feel more natural
    const randomBoost = (Math.random() - 0.5) * 0.5
    progress.value += progressIncrement + randomBoost

    // Whenever progress crosses the "next funny" threshold
    if (progress.value >= nextFunnyUpdate) {
      statusMessage.value = funnyStatusMessages[Math.floor(Math.random() * funnyStatusMessages.length)]
      nextFunnyUpdate += 10 + Math.random() * 10 // schedule next funny update
    }

    // Make sure it doesn't exceed 95 accidentally
    if (progress.value > 95) {
      progress.value = 95
    }
  }

  // After backend finishes, separately you can finalize it to 100%
}

</script>

<style scoped>
@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

@keyframes gradient-x {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out both;
}

.animate-gradient-x {
  background-size: 200% 200%;
  animation: gradient-x 2s ease infinite;
}

.spinner {
  width: 16px;
  height: 16px;
  border: 3px solid #cbd5e0;
  border-top: 3px solid #3b82f6;
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>
