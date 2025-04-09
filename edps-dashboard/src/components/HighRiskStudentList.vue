<template>
    <div class="bg-white p-4 rounded-lg shadow border">
      <h2 class="text-lg font-semibold mb-3 text-gray-800">🚨 Recent High-Risk Students</h2>
      <ul class="divide-y divide-gray-200">
        <li
          v-for="s in students"
          :key="s.id"
          class="py-2 flex justify-between items-center"
        >
          <div>
            <p class="font-medium text-gray-800">{{ s.name }}</p>
            <p class="text-sm text-gray-500">#{{ s.id }} | Risk Score: {{ s.risk }}</p>
          </div>
          <RouterLink
            :to="`/students/${s.id}`"
            class="text-sm text-blue-600 hover:underline"
          >
            View
          </RouterLink>
        </li>
      </ul>
    </div>
  </template>
  
  <script setup>
  const students = [
    { id: '40121', name: 'Anna Boyd', risk: 0.92 },
    { id: '40256', name: 'Liam Chen', risk: 0.89 },
    { id: '40388', name: 'Sara O’Neil', risk: 0.85 },
  ]
  </script>
  