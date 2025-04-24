<template>
  <div class="bg-gradient-to-br from-purple-50/80 to-purple-50/40 p-5 rounded-2xl shadow-lg border border-purple-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">
    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-purple-100 to-purple-50 text-purple-600">
          <BarChart2 class="w-3.5 h-3.5" />
        </div>
        <h3 class="text-sm font-semibold text-gray-900">
          Risk Score Spread
        </h3>
      </div>
      <p class="text-xs text-gray-500 ml-[38px]">Distribution</p>
    </div>

    <!-- Chart -->
    <div class="mb-3">
      <div class="h-[240px]">
        <BarChart
          v-if="chartData.labels.length && !hasNoData"
          :key="renderKey"
          :data="chartData"
          :options="chartOptions"
          class="w-full h-full"
        />
        <div v-else class="h-full flex items-center justify-center text-gray-400 text-sm italic">
          No risk score data available.
        </div>
      </div>
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
import { computed } from 'vue'

const hasNoData = computed(() => {
  return chartData.value.datasets.length === 0 ||
    chartData.value.datasets[0].data.every(value => value === 0)
})


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
        hoverBackgroundColor: '#7c3aed',
        borderRadius: 6,
        borderWidth: 2,
        borderColor: '#7c3aed',
        barPercentage: 0.65
      }
    ]

    chartOptions.value = {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false },
        tooltip: {
          backgroundColor: 'white',
          titleColor: '#374151',
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
            title: ctx => `Risk Score: ${ctx[0].label}`,
            label: ctx => `${ctx.raw.toLocaleString()} students`
          }
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          suggestedMax: roundedMax,
          border: { display: false },
          grid: {
            color: '#f0f1f3',
            lineWidth: 1
          },
          ticks: {
            padding: 4,
            color: '#9ca3af',
            font: { size: 10 },
            precision: 0,
            callback: value => value.toLocaleString()
          }
        },
        x: {
          border: { display: false },
          grid: { display: false },
          title: {
            display: true,
            text: 'Risk Score Range',
            color: '#6b7280',
            font: { size: 11, weight: '500' },
            padding: { top: 8 }
          },
          ticks: {
            padding: 4,
            color: '#9ca3af',
            font: { size: 10 },
            maxRotation: 0,
            minRotation: 0
          }
        }
      }
    }

    renderKey.value = Date.now()
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
  