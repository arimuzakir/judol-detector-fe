<template>
  <!-- Full lebar & tinggi -->
  <div class="flex h-screen w-screen">
    <!-- Sidebar: 20% -->
    <aside class="w-1/5 h-full bg-blue-700 text-white p-4">
      <Sidebar />
    </aside>

    <!-- Konten: 80% -->
    <main class="w-4/5 h-full bg-gray-100 overflow-y-auto p-6">
      <router-view />
    </main>
  </div>
</template>

<script setup>
// import Sidebar from '@/components/Sidebar.vue'
import Sidebar from './Sidebar.vue'
</script>
