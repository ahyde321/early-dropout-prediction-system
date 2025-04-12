<template>
  <div class="flex h-screen bg-gray-50 text-gray-900">
    <SideBar />

    <div class="flex-1 flex flex-col overflow-hidden">
      <TopBar />

      <main class="flex-1 overflow-y-auto px-6 py-4">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import SideBar from '@/components/SideBar.vue'
import TopBar from '@/components/TopBar.vue'
</script>
