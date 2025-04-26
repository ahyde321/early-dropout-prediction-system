<template>
  <div v-if="student" class="p-10 space-y-14 bg-white rounded-2xl shadow-2xl max-w-6xl mx-auto mt-10 animate-fade-in">
    <!-- Header -->
    <div class="flex flex-col lg:flex-row justify-between items-start lg:items-center gap-8">
      <div>
        <h1 class="text-5xl font-extrabold text-gray-800 tracking-tight">{{ student.first_name }} {{ student.last_name }}</h1>
        <p class="text-sm text-gray-500 mt-2">Student Number: {{ student.student_number }}</p>
      </div>
      <div class="flex flex-wrap gap-4">
        <button @click="toggleEdit" class="bg-gray-200 hover:bg-gray-300 text-gray-700 px-5 py-2.5 rounded-lg text-sm font-semibold transition">
          {{ isEditing ? 'Cancel' : 'Edit Student' }}
        </button>
        <button v-if="isEditing" @click="saveChanges" class="bg-green-600 hover:bg-green-700 text-white px-5 py-2.5 rounded-lg text-sm font-semibold transition">
          Save
        </button>
        <button @click="recalculatePrediction" :disabled="loading" class="bg-indigo-600 hover:bg-indigo-700 text-white px-6 py-3 rounded-lg text-sm font-semibold flex items-center gap-2 transition disabled:opacity-50">
          <span>{{ loading ? 'Recalculating...' : 'Recalculate Risk' }}</span>
        </button>
      </div>
    </div>

    <!-- Main Grid -->
    <div class="grid grid-cols-1 xl:grid-cols-[2fr_2fr] gap-14">
      <!-- Left: Student Info -->
      <section class="bg-gray-50 border border-gray-200 rounded-3xl p-10 shadow-md space-y-12">
        <!-- Personal Info -->
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Personal Information</h2>
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
        <div>
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Academic KPIs</h2>
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
        <div class="bg-gray-50 rounded-3xl p-8 border border-gray-200 shadow-md">
          <h2 class="text-2xl font-bold text-gray-800 mb-6">Prediction History</h2>

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

          <div v-else class="text-sm text-gray-500 text-center">
            No predictions yet for this student.
          </div>
        </div>
      </section>

    </div>
  </div>

  <div v-else class="text-center text-gray-500 mt-32 text-lg">Loading student profile...</div>
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
