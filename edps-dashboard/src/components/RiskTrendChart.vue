<template>
  <div
    class="bg-gradient-to-br from-white to-gray-50 p-6 rounded-3xl shadow-md border border-gray-200 hover:shadow-xl hover:scale-[1.01] transition-transform duration-300"
  >
    <!-- Header -->
    <div class="flex items-center gap-4 mb-5">
      <div class="p-2 rounded-full bg-sky-100 text-sky-600 shadow-inner ring-2 ring-sky-300">
        <TrendingUp class="w-6 h-6" />
      </div>
      <div>
        <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">
          Historical Trend
        </h2>
        <h3 class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent tracking-tight">
          Risk Over Time
        </h3>
      </div>
    </div>

    <!-- Chart -->
    <div class="h-64">
      <LineChart
        v-if="chartData.datasets.length"
        :data="chartData"
        :options="chartOptions"
        class="w-full h-full"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler
} from 'chart.js'
import { TrendingUp } from 'lucide-vue-next'
import api from '@/services/api'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Filler
)

const LineChart = Line
const chartData = ref({
  labels: [],
  datasets: []
})

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  animation: {
    duration: 600,
    easing: 'easeOutQuad'
  },
  plugins: {
    legend: {
      position: 'bottom',
      labels: {
        color: '#4b5563',
        boxWidth: 12,
        boxHeight: 12,
        borderRadius: 999,
        usePointStyle: true,
        pointStyle: 'circle',
        padding: 20,
        font: {
          size: 13,
          weight: '500'
        }
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: '#1f2937', // dark gray
      titleColor: '#fff',
      bodyColor: '#d1d5db', // lighter gray
      borderColor: '#4b5563',
      borderWidth: 1,
      padding: 10,
      displayColors: false,
      callbacks: {
        label: (context) => {
          const label = context.dataset.label || ''
          const value = context.parsed.y || 0
          return `${label}: ${value}`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      suggestedMin: 0,
      suggestedMax: 1000,
      ticks: {
        stepSize: 200,
        color: '#6b7280',
        callback: (value) => value
      },
      grid: {
        color: '#e5e7eb'
      }
    },
    x: {
      ticks: { color: '#6b7280' },
      grid: { display: false }
    }
  }
}

const fetchTrendData = async () => {
  try {
    const { data } = await api.get('/students/summary-by-phase')

    const phases = Object.keys(data)
    chartData.value.labels = phases.map(p => p.charAt(0).toUpperCase() + p.slice(1))

    chartData.value.datasets = [
      {
        label: 'Low Risk',
        data: phases.map(p => data[p].low || 0),
        borderColor: '#34d399',
        backgroundColor: 'rgba(52, 211, 153, 0.2)',
        tension: 0.4,
        fill: false
      },
      {
        label: 'Moderate Risk',
        data: phases.map(p => data[p].moderate || 0),
        borderColor: '#fbbf24',
        backgroundColor: 'rgba(251, 191, 36, 0.2)',
        tension: 0.4,
        fill: false
      },
      {
        label: 'High Risk',
        data: phases.map(p => data[p].high || 0),
        borderColor: '#f87171',
        backgroundColor: 'rgba(248, 113, 113, 0.2)',
        tension: 0.4,
        fill: false
      }
    ]
  } catch (error) {
    console.error('❌ Error fetching trend data:', error)
  }
}

onMounted(fetchTrendData)
</script>
