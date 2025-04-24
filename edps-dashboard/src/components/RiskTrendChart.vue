<template>
<div class="bg-gradient-to-br from-blue-50/80 to-blue-50/40 p-5 rounded-2xl shadow-lg border border-blue-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-blue-100 to-blue-50 text-blue-600">
          <LineChartIcon class="w-3.5 h-3.5" />
        </div>
        <h3 class="text-sm font-semibold text-gray-900">
          Risk Categories Over Time
        </h3>
      </div>
      <p class="text-xs text-gray-500 ml-[38px]">Historical Trend</p>
    </div>

    <!-- Chart -->
    <div class="mb-3">
      <div class="h-[200px]">
        <LineChart
          v-if="chartData.datasets.length"
          :data="chartData"
          :options="chartOptions"
          class="w-full h-full"
        />
      </div>
    </div>

    <!-- Legend -->
    <div class="flex justify-center gap-4 items-center text-xs text-gray-700">
      <div class="flex items-center gap-1.5 hover:opacity-75 transition-opacity">
        <span class="inline-block w-2 h-2 rounded-full bg-emerald-500"></span>
        Low Risk
      </div>
      <div class="flex items-center gap-1.5 hover:opacity-75 transition-opacity">
        <span class="inline-block w-2 h-2 rounded-full bg-amber-500"></span>
        Moderate Risk
      </div>
      <div class="flex items-center gap-1.5 hover:opacity-75 transition-opacity">
        <span class="inline-block w-2 h-2 rounded-full bg-rose-500"></span>
        High Risk
      </div>
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
import { LineChart as LineChartIcon } from 'lucide-vue-next'
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
const chartData = ref({ labels: [], datasets: [] })

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
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
        title: (items) => `Phase: ${items[0].label}`,
        label: (ctx) => `${ctx.dataset.label}: ${ctx.parsed.y.toLocaleString()}`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      border: { display: false },
      grid: {
        color: '#f0f1f3'
      },
      ticks: {
        padding: 4,
        color: '#9ca3af',
        font: { size: 10 }
      }
    },
    x: {
      border: { display: false },
      grid: { display: false },
      ticks: {
        padding: 4,
        color: '#9ca3af',
        font: { size: 10 }
      }
    }
  },
  elements: {
    line: {
      borderWidth: 3,
      tension: 0.4,
      fill: true
    },
    point: {
      radius: 4,
      hoverRadius: 6,
      borderWidth: 2,
      borderColor: 'white'
    }
  },
  interaction: {
    intersect: false,
    mode: 'index'
  }
}

const fetchTrendData = async () => {
  try {
    const { data } = await api.get('/students/summary-by-phase')
    const phases = Object.keys(data)
    const datasets = [
      {
        label: 'Low Risk',
        data: phases.map(p => data[p].low || 0),
        borderColor: '#10b981',
        backgroundColor: 'rgba(16, 185, 129, 0.15)',
        fill: false
      },
      {
        label: 'Moderate Risk',
        data: phases.map(p => data[p].moderate || 0),
        borderColor: '#f59e0b',
        backgroundColor: 'rgba(245, 158, 11, 0.15)',
        fill: false
      },
      {
        label: 'High Risk',
        data: phases.map(p => data[p].high || 0),
        borderColor: '#ef4444',
        backgroundColor: 'rgba(239, 68, 68, 0.15)',
        fill: false
      }
    ]

    chartData.value = {
      labels: phases.map(p => p.charAt(0).toUpperCase() + p.slice(1)),
      datasets
    }
  } catch (error) {
    console.error('❌ Error fetching trend data:', error)
    chartData.value = { labels: [], datasets: [] }
  }
}

onMounted(fetchTrendData)
</script>
