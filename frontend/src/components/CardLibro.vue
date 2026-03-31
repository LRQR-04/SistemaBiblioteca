<template>
  <div>
    <h3>{{ libro.titulo }}</h3>
    <p>{{ libro.autor }}</p>
  </div>
</template>

<script setup>
defineProps(['libro'])
</script>
