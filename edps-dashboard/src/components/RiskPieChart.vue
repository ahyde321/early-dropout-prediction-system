<template>
  <div class="bg-gradient-to-br from-indigo-50/80 to-indigo-50/40 p-5 rounded-2xl shadow-lg border border-indigo-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">
    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-indigo-100 to-indigo-50 text-indigo-600">
          <PieChart class="w-3.5 h-3.5" />
        </div>
        <h3 class="text-sm font-semibold text-gray-900">
          Risk Distribution
        </h3>
      </div>
      <p class="text-xs text-gray-500 ml-[38px]">Overview</p>
    </div>

    <div class="mb-3">
      <div v-if="hasNoData" class="h-[200px] flex items-center justify-center text-gray-400 text-sm">
        No risk data available.
      </div>
      <div v-else class="h-[200px]">
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

// Register components
Chart.register(PieController, ArcElement, Tooltip, Legend, Title)

// Props
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

// Canvas & chart ref
const canvasRef = ref(null)
let chartInstance = null

import { computed } from 'vue'

const hasNoData = computed(() => {
  const s = props.summary
  return (!s.low?.count && !s.moderate?.count && !s.high?.count)
})

const createChart = () => {
  if (!canvasRef.value) return
  if (chartInstance) chartInstance.destroy()

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
      datasets: [{
        data,
        backgroundColor: ['#10b981', '#f59e0b', '#ef4444'], // unified palette
        borderColor: '#ffffff',
        borderWidth: 2,
        hoverBorderColor: '#ffffff',
        hoverBorderWidth: 3,
        hoverOffset: 8,
        spacing: 2
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      animation: {
        animateScale: true,
        animateRotate: true,
        duration: 600
      },
      plugins: {
        legend: {
          position: 'bottom',
          labels: {
            color: '#374151',
            boxWidth: 10,
            boxHeight: 10,
            padding: 12,
            borderRadius: 3,
            font: {
              size: 12,
              family: "'Inter', sans-serif",
              weight: '500'
            },
            generateLabels: (chart) => {
              const dataset = chart.data.datasets[0]
              return chart.data.labels.map((label, i) => ({
                text: label,
                fillStyle: dataset.backgroundColor[i],
                strokeStyle: dataset.backgroundColor[i],
                lineWidth: 0,
                hidden: false,
                index: i
              }))
            }
          }
        },
        tooltip: {
          backgroundColor: '#ffffff',
          titleColor: '#111827',
          bodyColor: '#374151',
          borderColor: '#e5e7eb',
          borderWidth: 1,
          padding: 10,
          cornerRadius: 6,
          titleFont: {
            size: 12,
            weight: 600
          },
          bodyFont: {
            size: 11
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
      layout: { padding: 20 },
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

watch(() => props.summary, () => nextTick(createChart), { immediate: true })
onMounted(() => nextTick(createChart))
</script>
