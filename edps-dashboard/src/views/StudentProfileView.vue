<template>
  <InfoRow v-if="false" /> <!-- dummy use to make Vue register it properly -->
  <div class="p-8 space-y-8 bg-white rounded-3xl shadow-lg max-w-5xl mx-auto mt-8 animate-fade-in">
    <!-- Header -->
    <div class="flex justify-between items-center">
      <div>
        <h1 class="text-3xl font-bold text-gray-800">
          {{ student?.first_name }} {{ student?.last_name }}
        </h1>
        <p class="text-sm text-gray-500">Student Number: {{ student?.student_number }}</p>
      </div>

      <button
        @click="recalculatePrediction"
        :disabled="loading"
        class="bg-indigo-600 hover:bg-indigo-700 text-white px-5 py-2.5 rounded-lg text-sm font-semibold flex items-center gap-2 transition disabled:opacity-50"
      >
        <span>{{ loading ? 'Recalculating...' : 'Recalculate Risk' }}</span>
      </button>
    </div>

    <!-- Student Info -->
    <section>
      <h2 class="text-xl font-semibold mb-4 text-gray-700">Student Information</h2>
      <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 text-sm">
        <InfoRow label="Age at Enrollment" :value="student?.age_at_enrollment" />
        <InfoRow label="Gender" :value="student?.gender === 0 ? 'Male' : 'Female'" />
        <InfoRow label="Marital Status" :value="student?.marital_status" />
        <InfoRow label="Displaced" :value="student?.displaced ? 'Yes' : 'No'" />
        <InfoRow label="Debtor" :value="student?.debtor ? 'Yes' : 'No'" />
        <InfoRow label="Scholarship Holder" :value="student?.scholarship_holder ? 'Yes' : 'No'" />
        <InfoRow label="Tuition Fees Up To Date" :value="student?.tuition_fees_up_to_date ? 'Yes' : 'No'" />
        <InfoRow label="Previous Qualification Grade" :value="student?.previous_qualification_grade" />
        <InfoRow label="Admission Grade" :value="student?.admission_grade" />
        <InfoRow label="Curricular Units 1st Sem Enrolled" :value="student?.curricular_units_1st_sem_enrolled" />
        <InfoRow label="Curricular Units 1st Sem Approved" :value="student?.curricular_units_1st_sem_approved" />
        <InfoRow label="Curricular Units 1st Sem Grade" :value="student?.curricular_units_1st_sem_grade" />
        <InfoRow label="Curricular Units 2nd Sem Grade" :value="student?.curricular_units_2nd_sem_grade" />
        <InfoRow label="Notes" :value="student?.notes || 'None'" />
      </div>
    </section>

    <!-- Prediction History -->
    <section>
      <h2 class="text-xl font-semibold mb-4 text-gray-700">📈 Prediction History</h2>

      <div v-if="predictions.length" class="space-y-4">
        <div v-for="p in predictions" :key="p.id" class="border rounded-lg p-4 bg-gray-50 shadow-sm">
          <div class="flex justify-between items-center">
            <div class="text-gray-700">
              <div><strong>Phase:</strong> {{ capitalize(p.model_phase) }}</div>
              <div><strong>Risk Level:</strong> 
                <span :class="riskColor(p.risk_level)">
                  {{ capitalize(p.risk_level) }}
                </span>
              </div>
            </div>
            <div class="text-right text-gray-600">
              <div><strong>Risk Score:</strong> {{ (p.risk_score * 100).toFixed(2) }}%</div>
              <div><small>{{ formatTimestamp(p.timestamp) }}</small></div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="text-gray-500 text-sm text-center">
        No predictions yet for this student.
      </div>
    </section>
  </div>
</template>

<script setup>
import InfoRow from '@/components/InfoRow.vue'
import api from '@/services/api'
import { onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'

// --- Main component logic continues below ---
const route = useRoute()
const toast = useToast()

const student = ref(null)
const predictions = ref([])
const loading = ref(false)

async function fetchProfileData() {
  const studentNumber = route.params.student_number
  try {
    const { data: studentData } = await api.get(`/students/by-number/${studentNumber}`)
    student.value = studentData

    const { data: predictionData } = await api.get(`/predictions/${studentNumber}`)
    predictions.value = predictionData
  } catch (error) {
    console.error('❌ Failed to load student profile', error)
  }
}

async function recalculatePrediction() {
  loading.value = true
  const studentNumber = route.params.student_number

  try {
    await api.get(`/predict/by-number/${studentNumber}?recalculate=true`)
    toast.success('✅ Risk recalculated successfully!')

    const { data: updatedPredictions } = await api.get(`/predictions/${studentNumber}`)
    predictions.value = updatedPredictions
  } catch (error) {
    console.error('❌ Failed to recalculate', error)
    toast.error('❌ Recalculation failed')
  } finally {
    loading.value = false
  }
}

onMounted(fetchProfileData)

const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1)
const formatTimestamp = (timestamp) => new Date(timestamp).toLocaleString()
const riskColor = (risk) => ({
  high: 'text-red-600 font-semibold',
  moderate: 'text-yellow-600 font-semibold',
  low: 'text-green-600 font-semibold'
})[risk] || 'text-gray-600'
</script>


<style scoped>
@keyframes slow-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin-slow {
  animation: slow-spin 1s linear infinite;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out both;
}
</style>
