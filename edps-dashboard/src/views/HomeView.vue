<template>
  <div class="relative">
    <!-- Loading Overlay -->
    <transition name="fade" mode="out-in">
      <div
        v-if="loading"
        key="loading"
        class="fixed inset-0 bg-gray-100/90 flex flex-col items-center justify-center z-50 space-y-6"
      >
        <div class="w-2/3 max-w-md">
          <div class="relative w-full h-4 bg-gray-300 rounded-full overflow-hidden shadow-inner">
            <div
              class="absolute inset-0 bg-gradient-to-r from-blue-400 via-blue-500 to-blue-600 animate-gradient-shimmer rounded-full"
              :style="{ width: `${progress}%` }"
            ></div>
          </div>
        </div>
        <p class="text-sm text-gray-600 animate-pulse">{{ statusMessage }}</p>
      </div>
    </transition>

    <!-- Dashboard Content -->
    <transition name="fade" mode="out-in">
      <div v-if="!loading" key="dashboard" class="p-6 lg:p-8 space-y-10 bg-gray-50 min-h-screen text-gray-900 animate-fade-in">
        <!-- Summary Cards -->
        <section>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            <RiskSummaryCard label="Total Students" :value="students.length" color="blue" />
            <RiskSummaryCard label="High Risk" :value="summary.high.count" :trend="summary.high.trend" color="red" />
            <RiskSummaryCard label="Medium Risk" :value="summary.moderate.count" :trend="summary.moderate.trend" color="yellow" />
            <RiskSummaryCard label="Low Risk" :value="summary.low.count" :trend="summary.low.trend" color="green" />
          </div>
        </section>

        <!-- Charts -->
        <section>
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <RiskPieChart :summary="summary" :onFilter="filterByRisk" />
            <RiskTrendChart />
            <RiskScoreDistribution :students="students" />
          </div>
        </section>

        <!-- Insights -->
        <section>
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <HighRiskStudentList />
            <BiggestRiskIncreases />
            <StudentsRequiringReview />
          </div>
        </section>
      </div>
    </transition>
  </div>
</template>

<script setup>
import api from '@/services/api'
import { onMounted, ref } from 'vue'

import BiggestRiskIncreases from '@/components/BiggestRiskIncrease.vue'
import HighRiskStudentList from '@/components/HighRiskStudentList.vue'
import RiskPieChart from '@/components/RiskPieChart.vue'
import RiskScoreDistribution from '@/components/RiskScoreDistribution.vue'
import RiskSummaryCard from '@/components/RiskSummaryCard.vue'
import RiskTrendChart from '@/components/RiskTrendChart.vue'
import StudentsRequiringReview from '@/components/StudentsRequiringReview.vue'

const loading = ref(true)
const progress = ref(0)
const statusMessage = ref('Connecting...')
const allStudents = ref([])
const students = ref([])
const summary = ref({
  high: { count: 0, trend: 0 },
  moderate: { count: 0, trend: 0 },
  low: { count: 0, trend: 0 },
})
const user = ref({ full_name: 'User' })

async function simulateQuickLoading() {
  const steps = [
    { message: 'Fetching student data...', until: 30 },
    { message: 'Loading charts and graphs...', until: 60 },
    { message: 'Finalizing dashboard...', until: 90 }
  ]

  for (const step of steps) {
    while (progress.value < step.until) {
      await new Promise(resolve => setTimeout(resolve, 50))
      progress.value += 3
    }
    statusMessage.value = step.message
  }
}

// Fetch backend API
async function fetchDashboardData() {
  try {
    const [summaryRes, studentsRes] = await Promise.all([
      api.get('/students/summary'),
      api.get('/students/list')
    ])
    summary.value = summaryRes.data
    allStudents.value = studentsRes.data
    students.value = studentsRes.data
  } catch (error) {
    console.error('❌ Failed to load dashboard data:', error)
  }
}

// Risk filter
const filterByRisk = (riskLevel) => {
  students.value = allStudents.value.filter(s => s.risk_level === riskLevel)
}

onMounted(async () => {
  try {
    const { data } = await api.get('/auth/me')
    user.value = data
  } catch (err) {
    console.error('⚠️ Failed to fetch user info:', err)
  }

  // 🚀 Start loading and API simultaneously
  const loadingTask = simulateQuickLoading()
  const dataTask = fetchDashboardData()

  await Promise.all([loadingTask, dataTask])

  progress.value = 100
  statusMessage.value = "Dashboard ready 🚀"
  await new Promise(resolve => setTimeout(resolve, 300)) // Short pause
  loading.value = false
})

</script>

<style scoped>
@keyframes gradient-shimmer {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}

.animate-gradient-shimmer {
  background-size: 200% 200%;
  animation: gradient-shimmer 2s linear infinite;
}

@keyframes fade-in {
  from { opacity: 0; transform: translateY(10px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade-in {
  animation: fade-in 0.5s ease-out both;
}
</style>
