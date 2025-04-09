<template>
    <div class="bg-white p-4 rounded-lg shadow border">
      <h2 class="text-lg font-semibold text-gray-800 mb-3">📉 Risk Trend Over Time</h2>
      <div class="h-64">
        <LineChart :data="chartData" :options="chartOptions" />
      </div>
    </div>
  </template>
  
  
  <script setup>
  import { Line } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale
  } from 'chart.js'
  
  ChartJS.register(
    Title,
    Tooltip,
    Legend,
    LineElement,
    PointElement,
    LinearScale,
    CategoryScale
  )
  
  const LineChart = Line
  
  const chartData = {
  labels: ['Low', 'Medium', 'High'], // ✅ REQUIRED
  datasets: [{
    label: 'Risk Levels',
    data: [30, 60, 90],
    backgroundColor: ['#34d399', '#fbbf24', '#f87171'],
  }]
}

  
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top'
      },
      title: {
        display: false
      }
    }
  }
  </script>
  