<template>
  <div v-if="visible">
    <h3>Nuevo préstamo</h3>

    <input v-model="libro_id" placeholder="Libro ID" />
    <input v-model="usuario_id" placeholder="Usuario ID" />

    <button @click="emitir">Confirmar</button>
    <button @click="$emit('close')">Cancelar</button>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps(['visible'])
const emit = defineEmits(['crear', 'close'])

const libro_id = ref('')
const usuario_id = ref('')

const emitir = () => {
  emit('crear', { libro_id: libro_id.value, usuario_id: usuario_id.value })
}
</script>
