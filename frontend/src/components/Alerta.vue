<template>
  <div v-if="message" :class="['alert', type]">
    {{ message }}
  </div>
</template>

<script setup>
defineProps({
  message: String,
  type: String, // success | error
})
</script>

<style scoped>
.alert {
  position: fixed;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  padding: 10px 20px;
  border-radius: 8px;
  color: white;
  z-index: 999;
}

.success {
  background: #22c55e;
}

.error {
  background: #ef4444;
}
</style>
