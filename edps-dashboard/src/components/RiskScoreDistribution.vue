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
          :key="renderKey"
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
  
  const props = defineProps({
    students: {
      type: Array,
      required: true
    }
  })
  
  // Chart state
  const chartData = ref({ labels: [], datasets: [] })
  const chartOptions = ref({})
  const renderKey = ref(0)
  
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
      const step = getNiceStep(maxBucket)
      const roundedMax = Math.ceil(maxBucket / step) * step
  
      chartData.value.labels = Array.from({ length: 10 }, (_, i) =>
        ((i + 1) * 0.1).toFixed(1)
      )
  
      chartData.value.datasets = [
        {
          label: 'Students per risk range',
          data: buckets,
          backgroundColor: '#8b5cf6',
          borderRadius: { topLeft: 6, topRight: 6 },
          barPercentage: 0.9
        }
      ]
  
      chartOptions.value = {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              title: ctx => `Score ≈ ${ctx[0].label}`,
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
            suggestedMax: roundedMax,
            ticks: {
              stepSize: step,
              color: '#6b7280',
              precision: 0,
              callback: value => value
            },
            grid: { color: '#e5e7eb' }
          },
          x: {
            title: {
              display: true,
              text: 'Risk Score Range',
              color: '#4b5563',
              font: { size: 13, weight: '600' },
              padding: { top: 10 }
            },
            ticks: {
              color: '#6b7280',
              font: { size: 11, weight: '500' },
              padding: 6,
              maxRotation: 0,
              minRotation: 0
            },
            grid: { display: false }
          }
        }
      }
  
      renderKey.value = Date.now() // Always a new key to force re-render
    },
    { immediate: true }
  )
  
  function getNiceStep(max) {
    if (max <= 5) return 1
    if (max <= 20) return 5
    if (max <= 100) return 10
    return 50
  }
  </script>
  