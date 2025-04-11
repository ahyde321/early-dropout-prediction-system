<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">📊 Dashboard Overview</h1>

    <!-- Summary Cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
      <RiskSummaryCard label="Total Students" :value="students.length" color="blue" />
      <RiskSummaryCard label="High Risk" :value="summary.high.count" :trend="summary.high.trend" color="red" />
      <RiskSummaryCard label="Medium Risk" :value="summary.moderate.count" :trend="summary.moderate.trend" color="yellow" />
      <RiskSummaryCard label="Low Risk" :value="summary.low.count" :trend="summary.low.trend" color="green" />
    </div>


    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <RiskPieChart :students="students" />
      <RiskTrendChart />
    </div>

    <!-- High Risk Students List -->
    <HighRiskStudentList :students="students" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

import RiskSummaryCard from '@/components/RiskSummaryCard.vue'
import RiskPieChart from '@/components/RiskPieChart.vue'
import RiskTrendChart from '@/components/RiskTrendChart.vue'
import HighRiskStudentList from '@/components/HighRiskStudentList.vue'

// Reactive state
const students = ref([])
const summary = ref({
  high: { count: 0, trend: 0 },
  moderate: { count: 0, trend: 0 },
  low: { count: 0, trend: 0 },
})

// === Fetch summary card values and student list ===
const fetchDashboardData = async () => {
  try {
    // Fetch summary totals + trends
    const summaryRes = await api.get('/students/summary')
    summary.value = summaryRes.data

    // Fetch student list (with optional trend info per student)
    const studentsRes = await api.get('/students/list')
    students.value = studentsRes.data

  } catch (error) {
    console.error('❌ Dashboard data fetch failed:', error)
  }
}

onMounted(fetchDashboardData)
</script>

