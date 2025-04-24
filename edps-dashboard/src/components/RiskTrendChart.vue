<template>
  <div class="bg-cyan-50/50 p-6 rounded-3xl shadow-sm transition-all duration-200 hover:shadow-md hover:bg-cyan-50/70">
    <!-- Header -->
    <div class="mb-4">
      <div class="flex items-center gap-3 mb-1">
        <div class="p-2 rounded-lg bg-cyan-100 text-cyan-600 transition-colors duration-200 group-hover:bg-cyan-200">
          <LineChartIcon class="w-4 h-4" />
        </div>
        <h3 class="text-[15px] font-semibold text-gray-900">
          Risk Categories Over Time
        </h3>
      </div>
      <p class="text-sm text-gray-500 ml-9">Historical Trend</p>
    </div>

    <!-- Chart -->
    <div class="mb-6">
      <div class="h-[240px]">
        <LineChart
          v-if="chartData.datasets.length"
          :data="chartData"
          :options="chartOptions"
          class="w-full h-full"
        />
      </div>
    </div>

    <!-- Legend -->
    <div class="flex justify-center gap-6 items-center text-[13px] text-gray-700">
      <div class="flex items-center gap-2 transition-opacity duration-200 hover:opacity-75">
        <span class="inline-block w-2 h-2 rounded-full bg-cyan-500"></span>
        Low Risk
      </div>
      <div class="flex items-center gap-2 transition-opacity duration-200 hover:opacity-75">
        <span class="inline-block w-2 h-2 rounded-full bg-amber-400"></span>
        Moderate Risk
      </div>
      <div class="flex items-center gap-2 transition-opacity duration-200 hover:opacity-75">
        <span class="inline-block w-2 h-2 rounded-full bg-red-400"></span>
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
      padding: 12,
      displayColors: true,
      boxPadding: 6,
      cornerRadius: 8,
      usePointStyle: true,
      titleFont: {
        size: 13,
        weight: 600
      },
      bodyFont: {
        size: 12
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
        padding: 6,
        color: '#9ca3af',
        font: { size: 11 }
      }
    },
    x: {
      border: { display: false },
      grid: { display: false },
      ticks: {
        padding: 6,
        color: '#9ca3af',
        font: { size: 11 }
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
      hoverBorderWidth: 2,
      hoverBorderColor: 'white'
    }
  },
  interaction: {
    intersect: false,
    mode: 'index'
  },
  hover: {
    mode: 'index',
    intersect: false
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
        borderColor: '#06b6d4',  // cyan-500
        backgroundColor: '#06b6d4'
      },
      {
        label: 'Moderate Risk',
        data: phases.map(p => data[p].moderate || 0),
        borderColor: '#fbbf24',
        backgroundColor: '#fbbf24'
      },
      {
        label: 'High Risk',
        data: phases.map(p => data[p].high || 0),
        borderColor: '#f87171',
        backgroundColor: '#f87171'
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