<template>
  <div class="p-6 lg:p-8 space-y-10 bg-gradient-to-br from-slate-50 to-white min-h-screen text-gray-900">
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

    <!-- Lists / Insights -->
    <section>
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <HighRiskStudentList />
        <BiggestRiskIncreases />
        <StudentsRequiringReview />
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

// Components
import StudentsRequiringReview from '@/components/StudentsRequiringReview.vue'
import RiskSummaryCard from '@/components/RiskSummaryCard.vue'
import RiskPieChart from '@/components/RiskPieChart.vue'
import RiskTrendChart from '@/components/RiskTrendChart.vue'
import RiskScoreDistribution from '@/components/RiskScoreDistribution.vue'
import HighRiskStudentList from '@/components/HighRiskStudentList.vue'
import BiggestRiskIncreases from '@/components/BiggestRiskIncrease.vue'

// State
const allStudents = ref([])
const students = ref([])
const summary = ref({
  high: { count: 0, trend: 0 },
  moderate: { count: 0, trend: 0 },
  low: { count: 0, trend: 0 },
})

// Filter handler
const filterByRisk = (riskLevel) => {
  students.value = allStudents.value.filter(s => s.risk_level === riskLevel)
}

// Fetch data function
const fetchDashboardData = async () => {
  try {
    const [summaryRes, studentsRes] = await Promise.all([
      api.get('/students/summary'),
      api.get('/students/list')
    ])

    // Assign fetched data to reactive states
    summary.value = summaryRes.data
    allStudents.value = studentsRes.data
    students.value = studentsRes.data

    console.log('✅ Dashboard data loaded')
  } catch (error) {
    console.error('❌ Failed to load dashboard data:', error)
  }
}

onMounted(fetchDashboardData)
</script>
