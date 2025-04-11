<template>
    <div
      class="bg-gradient-to-br from-white to-gray-50 p-6 rounded-3xl shadow-md border border-gray-200 hover:shadow-xl hover:scale-[1.01] transition-transform duration-300"
    >
      <!-- Header -->
      <div class="flex items-center gap-4 mb-5">
        <div class="p-2 rounded-full bg-purple-100 text-purple-600 shadow-inner ring-2 ring-purple-300">
          <BarChart2 class="w-6 h-6" />
        </div>
        <div>
          <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">
            Distribution
          </h2>
          <h3 class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent tracking-tight">
            Risk Score Spread
          </h3>
        </div>
      </div>
  
      <!-- Chart -->
      <div class="h-64">
        <BarChart
          v-if="chartData.labels.length"
          :data="chartData"
          :options="chartOptions"
          class="w-full h-full"
        />
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue'
  import { Bar } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    BarElement,
    CategoryScale,
    LinearScale
  } from 'chart.js'
  import { BarChart2 } from 'lucide-vue-next'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  const BarChart = Bar
  
  // Props
  const props = defineProps({
    students: {
      type: Array,
      required: true
    }
  })
  
  // Chart state
  const chartData = ref({ labels: [], datasets: [] })
  
  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: {
        callbacks: {
          title: ctx => `Score ~ ${ctx[0].label}`,
          label: ctx => `${ctx.raw} students`
        },
        backgroundColor: '#1f2937',
        titleColor: '#fff',
        bodyColor: '#d1d5db',
        borderColor: '#4b5563',
        borderWidth: 1,
        padding: 10,
        displayColors: false
      }
    },
    scales: {
      y: {
        beginAtZero: true,
        ticks: {
          color: '#6b7280',
          precision: 0
        },
        grid: { color: '#e5e7eb' }
      },
      x: {
        title: {
          display: true,
          text: 'Risk Score Range',
          color: '#6b7280',
          font: { size: 13 }
        },
        ticks: {
          color: '#6b7280',
          maxRotation: 0,
          minRotation: 0
        },
        grid: { display: false }
      }
    }
  }
  
  // Compute bucket distribution and nice Y-axis ticks
  watch(
    () => props.students,
    (students) => {
      const buckets = Array(10).fill(0)
  
      students.forEach(student => {
        const score = student.risk_score
        if (typeof score === 'number') {
          const index = Math.min(Math.floor(score * 10), 9)
          buckets[index]++
        }
      })
  
      const maxBucket = Math.max(...buckets)
      const niceStep = getNiceStepSize(maxBucket)
      const roundedMax = Math.ceil(maxBucket / niceStep) * niceStep
  
      chartOptions.scales.y.ticks.stepSize = niceStep
      chartOptions.scales.y.suggestedMax = roundedMax
  
      chartData.value.labels = buckets.map((_, i) => ((i + 0.5) * 0.1).toFixed(1))
      chartData.value.datasets = [
        {
          label: 'Students per risk range',
          data: buckets,
          backgroundColor: '#8b5cf6',
          borderRadius: 4,
          barPercentage: 0.9
        }
      ]
    },
    { immediate: true }
  )
  
  // Utility to generate nice rounded steps like 50, 100, etc.
  function getNiceStepSize(max) {
    const rawStep = max / 4
    const rounded = Math.ceil(rawStep / 50) * 50
    return rounded || 50
  }
  </script>
  