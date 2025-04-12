<template>
  <div
    class="bg-gradient-to-br from-white to-gray-50 p-6 rounded-3xl shadow-md border border-gray-200 hover:shadow-xl hover:scale-[1.01] transition-transform duration-300 relative"
  >
    <!-- Header + Filters -->
    <div class="flex justify-between items-center mb-4">
      <div class="flex items-center gap-4">
        <div class="p-2 rounded-full bg-sky-100 text-sky-600 shadow-inner ring-2 ring-sky-300">
          <TrendingUp class="w-6 h-6" />
        </div>
        <div>
          <h2 class="text-sm font-semibold text-gray-500 uppercase tracking-wide">
            Historical Trend
          </h2>
          <h3 class="text-xl font-bold bg-gradient-to-r from-gray-800 to-gray-600 bg-clip-text text-transparent tracking-tight">
            Risk Categories Over Time
          </h3>
        </div>
      </div>

      <!-- Reusable FilterPopover Component -->
      <FilterPopover
        v-model="filters"
        :fields="filterFields"
        :format="formatValue"
      >
        <template #icon>
          <svg class="w-4 h-4 text-sky-500" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707v5.172a1 1 0 01-1.447.894l-2-1A1 1 0 0110 17.172V12a1 1 0 00-.293-.707L3.293 6.707A1 1 0 013 6V4z" />
          </svg>
          <span>Filters</span>
        </template>
      </FilterPopover>
    </div>

    <!-- Legend -->
    <div class="flex justify-start gap-6 items-center text-sm font-medium text-gray-600 px-1 mb-2">
      <div class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full" style="background-color: #34d399"></span>
        Low Risk
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full" style="background-color: #fbbf24"></span>
        Moderate Risk
      </div>
      <div class="flex items-center gap-2">
        <span class="inline-block w-3 h-3 rounded-full" style="background-color: #f87171"></span>
        High Risk
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
import { ref, watch, onMounted } from 'vue'
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
import FilterPopover from '@/components/FilterPopover.vue'

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

const filters = ref({ field: '', value: '' })

const filterFields = {
  gender: 'Gender',
  scholarship_holder: 'Scholarship Holder',
  tuition_fees_up_to_date: 'Tuition Paid',
  daytime_evening_attendance: 'Attendance Mode',
  debtor: 'Debtor Status',
  marital_status: 'Marital Status'
}

const formatValue = (val) => {
  if (filters.value.field === 'gender') {
    return val === 1 ? 'Male' : val === 0 ? 'Female' : val
  }
  if (val === 1) return 'Yes'
  if (val === 0) return 'No'
  return val
}

const fetchTrendData = async () => {
  try {
    const params = {}
    if (filters.value.field && filters.value.value !== '') {
      params.filter_field = filters.value.field
      params.filter_value = filters.value.value
    }

    const { data } = await api.get('/students/summary-by-phase', { params })
    const phases = Object.keys(data)
    const datasets = [
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

    const hasData = datasets.some(ds => ds.data.some(v => v > 0))

    chartData.value = hasData
      ? { labels: phases.map(p => p.charAt(0).toUpperCase() + p.slice(1)), datasets }
      : { labels: [], datasets: [] }
  } catch (error) {
    console.error('❌ Error fetching trend data:', error)
    chartData.value = { labels: [], datasets: [] }
  }
}

watch(filters, fetchTrendData)
onMounted(fetchTrendData)

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: { display: false },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: '#1f2937',
      titleColor: '#fff',
      bodyColor: '#d1d5db',
      borderColor: '#4b5563',
      borderWidth: 1,
      padding: 10,
      displayColors: false,
      callbacks: {
        label: (context) => `${context.dataset.label}: ${context.parsed.y}`
      }
    }
  },
  scales: {
    y: {
      beginAtZero: true,
      ticks: { color: '#6b7280' },
      grid: { color: '#e5e7eb' }
    },
    x: {
      ticks: { color: '#6b7280' },
      grid: { display: false }
    }
  }
}
</script>