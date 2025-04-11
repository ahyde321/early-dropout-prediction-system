<template>
  <div
  class="bg-gradient-to-br from-white to-gray-50 p-6 rounded-3xl border border-gray-200 shadow-md hover:shadow-xl hover:scale-[1.015] transition-transform duration-300"
  >
    <!-- Header with Icon -->
    <div class="flex items-center gap-4 mb-5">
      <div
        class="p-2 rounded-full bg-gradient-to-br from-indigo-100 to-indigo-200 text-indigo-700 shadow-md ring-2 ring-indigo-300">
        <PieChart class="w-6 h-6" stroke-width="2" />
      </div>

      <div>
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">
          Overview
        </h2>
        <h3
          class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent tracking-tight"
        >
          Risk Distribution
        </h3>
      </div>
    </div>


    <!-- Chart Container -->
    <div class="relative h-64 w-full">
      <canvas ref="canvasRef" class="w-full h-full"></canvas>
    </div>
  </div>
</template>


<script setup>
import { ref, watch, nextTick, onMounted } from 'vue'
import { PieChart } from 'lucide-vue-next'
import {
  Chart,
  PieController,
  ArcElement,
  Tooltip,
  Legend,
  Title
} from 'chart.js'

// Register required components
Chart.register(PieController, ArcElement, Tooltip, Legend, Title)

// Props from parent
const props = defineProps({
  summary: {
    type: Object,
    required: true
  },
  onFilter: {
    type: Function,
    default: null
  }
})

// Canvas reference and chart instance
const canvasRef = ref(null)
let chartInstance = null

// Chart setup
const createChart = () => {
  if (!canvasRef.value) return
  if (chartInstance) {
    chartInstance.destroy()
  }

  const ctx = canvasRef.value.getContext('2d')

  const data = [
    props.summary.low?.count || 0,
    props.summary.moderate?.count || 0,
    props.summary.high?.count || 0
  ]

  chartInstance = new Chart(ctx, {
    type: 'pie',
    data: {
      labels: ['Low Risk', 'Moderate Risk', 'High Risk'],
      datasets: [
        {
          data,
          backgroundColor: ['#34d399', '#fbbf24', '#f87171'],
          borderWidth: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        animateScale: true,
        duration: 800
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#4b5563',
            boxWidth: 14,
            boxHeight: 14,
            borderRadius: 4,
            font: {
              size: 13,
              weight: '500'
            },
            padding: 20
          }
        },
        tooltip: {
          callbacks: {
            label: (context) => {
              const value = context.parsed
              const label = context.label
              const total = context.chart.data.datasets[0].data.reduce((a, b) => a + b, 0)
              const percent = ((value / total) * 100).toFixed(1)
              return `${label}: ${value} students (${percent}%)`
            }
          }
        }
      },
      onClick: (event, elements) => {
        if (!elements.length || !props.onFilter) return
        const index = elements[0].index
        const label = chartInstance.data.labels[index]
        const risk = label.toLowerCase().split(' ')[0]
        props.onFilter(risk)
      }
    }
  })
}

// Watch for changes
watch(
  () => props.summary,
  () => {
    nextTick(() => createChart())
  },
  { immediate: true }
)

onMounted(() => {
  nextTick(() => createChart())
})
</script>
