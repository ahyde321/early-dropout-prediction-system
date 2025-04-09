<template>
    <aside class="w-64 h-full bg-white shadow-lg flex flex-col">
      <div class="p-6 border-b border-gray-200">
        <h1 class="text-2xl font-bold text-gray-800">EDPS</h1>
        <p class="text-sm text-gray-500">Advisor Dashboard</p>
      </div>
      <nav class="flex flex-col gap-2 p-4 text-gray-700">
        <RouterLink
          to="/"
          class="block px-4 py-2 rounded hover:bg-blue-100"
          active-class="bg-blue-100 font-semibold text-blue-700"
          exact
        >
          Dashboard
        </RouterLink>
        <RouterLink
          to="/students"
          class="block px-4 py-2 rounded hover:bg-blue-100"
          active-class="bg-blue-100 font-semibold text-blue-700"
        >
          Students
        </RouterLink>
        <RouterLink
          to="/upload"
          class="block px-4 py-2 rounded hover:bg-blue-100"
          active-class="bg-blue-100 font-semibold text-blue-700"
        >
          Upload CSV
        </RouterLink>
      </nav>
    </aside>
  </template>
  