<template>
    <Bar :data="chartData" :options="chartOptions" />
  </template>
  
  <script setup>
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
  
  import { computed } from 'vue'
  
  ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)
  
  const props = defineProps({
    data: Object
  })
  
  const chartData = computed(() => ({
    labels: Object.keys(props.data || {}),
    datasets: [
      {
        label: "Feature Importance",
        data: Object.values(props.data || {}),
        backgroundColor: "#3B82F6"
      }
    ]
  }))
  
  const chartOptions = {
    responsive: true,
    plugins: {
      legend: { display: false },
      title: { display: false }
    },
    scales: {
      y: { beginAtZero: true }
    }
  }
  </script>
  