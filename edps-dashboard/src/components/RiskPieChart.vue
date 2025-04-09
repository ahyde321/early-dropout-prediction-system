<template>
    <div class="bg-white p-4 rounded-lg shadow border">
      <h2 class="text-lg font-semibold text-gray-800 mb-3">📈 Risk Distribution</h2>
      <div class="h-64"> <!-- ✅ fixed height wrapper -->
        <PieChart :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { reactive } from 'vue'
  import { Pie } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement)
  
  // ✅ Component alias
  const PieChart = Pie
  
  // ✅ Reactive data object
  const chartData = reactive({
    labels: ['Low', 'Medium', 'High'],
    datasets: [{
      label: 'Risk Levels',
      data: [30, 60, 90],
      backgroundColor: ['#34d399', '#fbbf24', '#f87171'],
      borderWidth: 1
    }]
  })
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
      },
      title: {
        display: false,
      }
    }
  }
  </script>
  