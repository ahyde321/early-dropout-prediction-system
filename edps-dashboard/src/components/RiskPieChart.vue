<template>
  <div class="bg-blue-50/50 p-6 rounded-3xl shadow-sm transition-all duration-200 hover:shadow-md hover:bg-blue-50/70">
    <!-- Header -->
    <div class="mb-4">
      <div class="flex items-center gap-3 mb-1">
        <div class="p-2 rounded-lg bg-blue-100 text-blue-600 transition-colors duration-200 group-hover:bg-blue-200">
          <PieChart class="w-4 h-4" />
        </div>
        <h3 class="text-[15px] font-semibold text-gray-900">
          Risk Distribution
        </h3>
      </div>
      <p class="text-sm text-gray-500 ml-9">Overview</p>
    </div>

    <!-- Chart Container -->
    <div class="mb-4">
      <div class="h-[240px]">
        <canvas ref="canvasRef" class="w-full h-full"></canvas>
      </div>
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
          backgroundColor: ['#3b82f6', '#fbbf24', '#f87171'],
          borderColor: '#ffffff',
          borderWidth: 2,
          hoverBorderColor: '#ffffff',
          hoverBorderWidth: 3,
          spacing: 2
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        animateScale: true,
        duration: 500
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#374151',
            boxWidth: 12,
            boxHeight: 12,
            padding: 15,
            borderRadius: 3,
            font: {
              size: 13,
              family: "'Inter', sans-serif"
            },
            generateLabels: (chart) => {
              const data = chart.data
              return data.labels.map((label, index) => ({
                text: label,
                fillStyle: data.datasets[0].backgroundColor[index],
                strokeStyle: data.datasets[0].backgroundColor[index],
                lineWidth: 0,
                hidden: false,
                index: index
              }))
            }
          }
        },
        tooltip: {
          backgroundColor: 'white',
          titleColor: '#374151',
          bodyColor: '#374151',
          borderColor: '#e5e7eb',
          borderWidth: 1,
          padding: 12,
          cornerRadius: 8,
          titleFont: {
            size: 13,
            weight: 600
          },
          bodyFont: {
            size: 12
          },
          callbacks: {
            label: (context) => {
              const value = context.parsed
              const total = context.dataset.data.reduce((a, b) => a + b, 0)
              const percent = ((value / total) * 100).toFixed(1)
              return `${context.label}: ${value.toLocaleString()} students (${percent}%)`
            }
          }
        }
      },
      layout: {
        padding: 20
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
