<template>
  <div class="flex h-screen bg-gradient-to-br from-white to-slate-50 text-gray-900 overflow-hidden">
    <!-- Sidebar -->
    <div class="w-64 bg-white/70 backdrop-blur-md border-r border-gray-200 shadow-md hidden lg:block">
      <SideBar />
    </div>

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col">
      <!-- Top Bar -->
      <TopBar />

      <!-- Page Content -->
      <main class="flex-1 overflow-y-auto px-4 sm:px-6 py-6">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import SideBar from '@/components/SideBar.vue'
import TopBar from '@/components/TopBar.vue'
</script>
