<template>
  <div class="bg-gradient-to-br from-cyan-50/80 to-cyan-50/40 p-5 rounded-2xl shadow-lg border border-cyan-100/50 transition-all duration-200 hover:shadow-xl hover:scale-[1.02]">
    <!-- Header -->
    <div class="mb-3">
      <div class="flex items-center gap-2.5 mb-1">
        <div class="p-2 rounded-lg bg-gradient-to-br from-cyan-100 to-cyan-50 text-cyan-600">
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
      <div class="flex items-center gap-1.5 transition-opacity duration-200 hover:opacity-75">
        <span class="inline-block w-1.5 h-1.5 rounded-full bg-cyan-500"></span>
        Low Risk
      </div>
      <div class="flex items-center gap-1.5 transition-opacity duration-200 hover:opacity-75">
        <span class="inline-block w-1.5 h-1.5 rounded-full bg-amber-400"></span>
        Moderate Risk
      </div>
      <div class="flex items-center gap-1.5 transition-opacity duration-200 hover:opacity-75">
        <span class="inline-block w-1.5 h-1.5 rounded-full bg-red-400"></span>
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
  CategoryScale
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
  CategoryScale
)

const LineChart = Line
const chartData = ref({ labels: [], datasets: [] })

const chartOptions = {
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
        title: (tooltipItems) => {
          return `Phase: ${tooltipItems[0].label}`
        },
        label: (context) => {
          const value = context.parsed.y
          return `${context.dataset.label}: ${value.toLocaleString()}`
        }
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      border: { display: false },
      grid: {
        color: '#f0f1f3',
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
      borderWidth: 2,
      tension: 0.4
    },
    point: {
      radius: 3,
      hoverRadius: 5,
      borderWidth: 2,
      borderColor: 'white',
      hoverBorderWidth: 2,
      hoverBorderColor: 'white'
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
        borderColor: '#06b6d4',
        tension: 0.4
      },
      {
        label: 'Moderate Risk',
        data: phases.map(p => data[p].moderate || 0),
        borderColor: '#fbbf24',
        tension: 0.4
      },
      {
        label: 'High Risk',
        data: phases.map(p => data[p].high || 0),
        borderColor: '#f87171',
        tension: 0.4
      }
    ]

    chartData.value = { 
      labels: phases.map(p => p.charAt(0).toUpperCase() + p.slice(1)), 
      datasets 
    }
  } catch (error) {
    console.error('Error fetching trend data:', error)
    chartData.value = { labels: [], datasets: [] }
  }
}

onMounted(fetchTrendData)
</script>