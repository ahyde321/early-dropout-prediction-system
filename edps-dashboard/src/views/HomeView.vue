<template>
  <div class="p-6 space-y-6">
    <h1 class="text-2xl font-bold text-gray-800">📊 Dashboard Overview</h1>

    <!-- Cards -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <RiskSummaryCard label="Total Students" :value="320" color="blue" />
      <RiskSummaryCard label="High Risk" :value="47" color="red" />
      <RiskSummaryCard label="Medium Risk" :value="88" color="yellow" />
    </div>

    <!-- Charts -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
      <RiskPieChart />
      <RiskTrendChart />
    </div>

    <!-- High Risk Students -->
    <HighRiskStudentList />
  </div>
</template>

<script setup>
import RiskSummaryCard from '@/components/RiskSummaryCard.vue'
import RiskPieChart from '@/components/RiskPieChart.vue'
import RiskTrendChart from '@/components/RiskTrendChart.vue'
import HighRiskStudentList from '@/components/HighRiskStudentList.vue'
</script>
