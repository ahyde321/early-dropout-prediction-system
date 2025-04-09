<template>
    <div class="flex h-screen bg-gray-100 text-gray-900">
      <!-- Sidebar -->
      <SideBar />
  
      <!-- Main Content -->
      <div class="flex-1 flex flex-col overflow-hidden">
        <!-- Topbar -->
        <TopBar />
  
        <!-- Page Content -->
        <main class="flex-1 overflow-y-auto p-6">
          <router-view />
        </main>
      </div>
    </div>
  </template>
  
  <script setup>
  import SideBar from '@/components/SideBar.vue'
  import TopBar from '@/components/TopBar.vue'
  </script>
  