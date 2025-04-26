<template>
  <div v-if="student" class="p-10 space-y-14 bg-gradient-to-b from-gray-50 to-white min-h-screen">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8 bg-white p-8 rounded-2xl shadow-lg">
      <div>
        <h1 class="text-5xl font-extrabold bg-gradient-to-r from-sky-600 to-blue-800 bg-clip-text text-transparent tracking-tight">
          {{ student.first_name }} {{ student.last_name }}
        </h1>
        <p class="text-sm text-gray-500 mt-2 flex items-center gap-2">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
          </svg>
          Student Number: {{ student.student_number }}
        </p>
      </div>
      <div class="flex flex-wrap gap-4">
        <button @click="toggleEdit" class="btn-secondary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
          </svg>
          {{ isEditing ? 'Cancel' : 'Edit Student' }}
        </button>
        <button v-if="isEditing" @click="saveChanges" class="btn-primary">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
          </svg>
          Save Changes
        </button>
        <button @click="recalculatePrediction" :disabled="loading" class="btn-gradient">
          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ loading ? 'Recalculating...' : 'Recalculate Risk' }}
        </button>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-[2fr_2fr] gap-14">
      <!-- Left: Student Info -->
      <section class="bg-white border border-gray-200 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-shadow duration-300">
        <!-- Personal Info -->
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
            </svg>
            Personal Information
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-20 gap-y-6">
            <InfoRow label="Age at Enrollment" :value="displayValue('age_at_enrollment')" :editable="isEditing" v-model="editableFields.age_at_enrollment" />
            <SelectRow label="Gender" :editable="isEditing" v-model="editableFields.gender" :options="{ 0: 'Male', 1: 'Female' }" />
            <InfoRow label="Marital Status" :value="displayValue('marital_status')" :editable="isEditing" v-model="editableFields.marital_status" />
            <SelectRow label="Displaced" :editable="isEditing" v-model="editableFields.displaced" :options="{ 1: 'Yes', 0: 'No' }" />
            <SelectRow label="Debtor" :editable="isEditing" v-model="editableFields.debtor" :options="{ 1: 'Yes', 0: 'No' }" />
            <SelectRow label="Scholarship Holder" :editable="isEditing" v-model="editableFields.scholarship_holder" :options="{ 1: 'Yes', 0: 'No' }" />
            <SelectRow label="Tuition Fees Paid" :editable="isEditing" v-model="editableFields.tuition_fees_up_to_date" :options="{ 1: 'Yes', 0: 'No' }" />
            <InfoRow label="Notes" :value="displayValue('notes')" :editable="isEditing" v-model="editableFields.notes" />
          </div>
        </div>

        <!-- Academic KPIs -->
        <div class="mt-12">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
            </svg>
            Academic KPIs
          </h2>
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-x-20 gap-y-6">
            <InfoRow label="Qualification Grade" :value="displayValue('previous_qualification_grade')" :editable="isEditing" v-model="editableFields.previous_qualification_grade" />
            <InfoRow label="Admission Grade" :value="displayValue('admission_grade')" :editable="isEditing" v-model="editableFields.admission_grade" />
            <InfoRow label="1st Sem Enrolled" :value="displayValue('curricular_units_1st_sem_enrolled')" :editable="isEditing" v-model="editableFields.curricular_units_1st_sem_enrolled" />
            <InfoRow label="1st Sem Approved" :value="displayValue('curricular_units_1st_sem_approved')" :editable="isEditing" v-model="editableFields.curricular_units_1st_sem_approved" />
            <InfoRow label="1st Sem Grade" :value="displayValue('curricular_units_1st_sem_grade')" :editable="isEditing" v-model="editableFields.curricular_units_1st_sem_grade" />
            <InfoRow label="2nd Sem Grade" :value="displayValue('curricular_units_2nd_sem_grade')" :editable="isEditing" v-model="editableFields.curricular_units_2nd_sem_grade" />
          </div>
        </div>
      </section>

      <!-- Right: Prediction History -->
      <section class="space-y-8">
        <div class="bg-white rounded-2xl p-8 border border-gray-200 shadow-lg hover:shadow-xl transition-shadow duration-300">
          <h2 class="text-2xl font-bold text-gray-800 mb-6 flex items-center gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6 text-sky-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            Prediction History
          </h2>

          <div v-if="Array.isArray(predictions) && predictions.length" class="space-y-8">
            <PredictionCard
              v-for="(p, index) in predictions"
              :key="p.id"
              :phaseLabel="capitalize(p.model_phase)"
              :riskLabel="capitalize(p.risk_level)"
              :score="p.risk_score * 100"
              :timestamp="p.timestamp"
            >
              <ShapFeatureCard v-if="p.shap_values" :shapValues="p.shap_values" />
            </PredictionCard>
          </div>

          <div v-else class="text-center py-8">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12 mx-auto text-gray-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
            </svg>
            <p class="mt-4 text-gray-500">No predictions yet for this student.</p>
          </div>
        </div>
      </section>
    </div>
  </div>

  <div v-else class="flex items-center justify-center min-h-screen">
    <div class="text-center">
      <svg class="animate-spin-slow h-12 w-12 text-sky-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
      </svg>
      <p class="mt-4 text-gray-500 text-lg">Loading student profile...</p>
    </div>
  </div>
</template>

<script setup>
import InfoRow from '@/components/InfoRow.vue'
import PredictionCard from '@/components/PredictionCard.vue'
import SelectRow from '@/components/SelectRow.vue'
import ShapFeatureCard from '@/components/ShapFeatureCard.vue'
import api from '@/services/api'
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useToast } from 'vue-toastification'



const route = useRoute()
const toast = useToast()

const student = ref(null)
const editableFields = ref({})
const predictions = ref([])
const loading = ref(false)
const isEditing = ref(false)

async function fetchProfileData() {
  const studentNumber = route.params.student_number
  try {
    const { data: studentData } = await api.get(`/students/by-number/${studentNumber}`)
    student.value = studentData
    editableFields.value = { ...studentData }
    console.log('✅ student data:', JSON.parse(JSON.stringify(student.value)))
    console.log('✅ editableFields:', JSON.parse(JSON.stringify(editableFields.value)))
  } catch (error) {
    console.error('❌ Failed to load student profile', error)
  }

  try {
    const { data: predictionData } = await api.get(`/predictions/${studentNumber}`)
    predictions.value = predictionData
    console.log('✅ predictions data:', JSON.parse(JSON.stringify(predictions.value)))
  } catch (error) {
    console.error('❌ Failed to load predictions', error)
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

async function saveChanges() {
  const studentNumber = route.params.student_number
  try {
    const payload = {
      ...editableFields.value,
      displaced: Number(editableFields.value.displaced),
      debtor: Number(editableFields.value.debtor),
      scholarship_holder: Number(editableFields.value.scholarship_holder),
      tuition_fees_up_to_date: Number(editableFields.value.tuition_fees_up_to_date)
    };

    console.log('🚀 Final payload:', payload);

    await api.patch(`/students/${studentNumber}`, payload, {
      headers: {
        'Content-Type': 'application/json'
      }
    });

    toast.success('✅ Student information updated!');
    isEditing.value = false;
    await fetchProfileData(); // refresh after save
  } catch (error) {
    console.error('❌ Failed to save changes', error);
    toast.error('❌ Failed to update student information');
  }
}


function toggleEdit() {
  if (isEditing.value) {
    editableFields.value = { ...student.value }
  }
  isEditing.value = !isEditing.value
}



const capitalize = (str) => str.charAt(0).toUpperCase() + str.slice(1)
const formatTimestamp = (timestamp) => new Date(timestamp).toLocaleString()
const riskColor = (risk) => ({
  high: 'text-red-600 font-semibold',
  moderate: 'text-yellow-600 font-semibold',
  low: 'text-green-600 font-semibold'
})[risk] || 'text-gray-600'

const shapExpanded = ref([])

function toggleShap(index) {
  shapExpanded.value[index] = !shapExpanded.value[index]
}

const expandedIndex = ref(null)

watch(predictions, (newPreds) => {
  if (Array.isArray(newPreds) && newPreds.length) {
    expandedIndex.value = newPreds.length - 1 // auto-open most recent
  }
})

const displayValue = (field) => {
  if (!student.value || !editableFields.value) return ''

  const value = isEditing.value ? editableFields.value[field] : student.value[field]

  // Check if the field is one of the ones you want to round
  const fieldsToRound = [
    'curricular_units_1st_sem_grade',
    'curricular_units_2nd_sem_grade',
    'previous_qualification_grade',
    'admission_grade'
  ]

  if (fieldsToRound.includes(field) && typeof value === 'number') {
    return value.toFixed(2) // round to 2 decimal places
  }

  return value
}


onMounted(fetchProfileData)
</script>

<style scoped>
.btn-primary {
  @apply bg-gradient-to-r from-sky-500 to-sky-600 text-white px-5 py-2.5 rounded-lg text-sm font-semibold transition-all shadow-sm flex items-center hover:from-sky-600 hover:to-sky-700;
}

.btn-secondary {
  @apply bg-gray-200 text-gray-700 px-5 py-2.5 rounded-lg text-sm font-semibold transition-all shadow-sm flex items-center hover:bg-gray-300;
}

.btn-gradient {
  @apply bg-gradient-to-r from-indigo-500 to-purple-600 text-white px-6 py-3 rounded-lg text-sm font-semibold flex items-center gap-2 transition-all shadow-sm hover:from-indigo-600 hover:to-purple-700 disabled:opacity-50;
}

@keyframes slow-spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.animate-spin-slow {
  animation: slow-spin 2s linear infinite;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 0.6s ease-out both;
}

.fade-enter-active,
.fade-leave-active {
  transition: all 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
