<template>
    <aside class="w-64 bg-white border-r shadow-md hidden sm:block">
      <div class="h-full flex flex-col p-4">
        <h2 class="text-xl font-bold mb-6">EDPS</h2>
        <nav class="space-y-2">
          <RouterLink to="/" class="block px-3 py-2 rounded hover:bg-blue-100">Dashboard</RouterLink>
          <RouterLink to="/students" class="block px-3 py-2 rounded hover:bg-blue-100">Students</RouterLink>
          <RouterLink to="/upload" class="block px-3 py-2 rounded hover:bg-blue-100">Upload CSV</RouterLink>
        </nav>
      </div>
    </aside>
  </template>
  