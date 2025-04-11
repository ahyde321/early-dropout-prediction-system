<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">📊 Dashboard Overview</h1>

    <!-- Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <RiskSummaryCard label="Total Students" :value="total.value" color="blue" />
      <RiskSummaryCard label="High Risk" :value="high.value" color="red" />
      <RiskSummaryCard label="Medium Risk" :value="moderate.value" color="yellow" />
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <RiskPieChart :students="students.value" />
      <RiskTrendChart />
    </div>

    <!-- High Risk Students -->
    <HighRiskStudentList :students="students.value" />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

import RiskSummaryCard from '@/components/RiskSummaryCard.vue'
import RiskPieChart from '@/components/RiskPieChart.vue'
import RiskTrendChart from '@/components/RiskTrendChart.vue'
import HighRiskStudentList from '@/components/HighRiskStudentList.vue'

const students = ref([])
const total = ref(0)
const high = ref(0)
const moderate = ref(0)

onMounted(async () => {
  try {
    const response = await api.get('/students/list')
    students.value = response.data
    total.value = students.value.length
    high.value = students.value.filter(s => s.risk_level === 'high').length
    moderate.value = students.value.filter(s => s.risk_level === 'moderate').length
  } catch (err) {
    console.error('Failed to load student data:', err)
  }
})
</script>