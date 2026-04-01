<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <div class="layout">
    <Sidebar />
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
.layout {
  display: flex;
}

.content {
  flex: 1;
  padding: 20px;
}
</style>
