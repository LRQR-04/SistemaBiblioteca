<script setup>
import Sidebar from '../components/Sidebar.vue'
</script>

<template>
  <div class="layout">
    <Sidebar class="sidebar" />
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<style>
.layout {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 250px;
  flex-shrink: 0;
  background-color: #f4f4f4;
}

.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
