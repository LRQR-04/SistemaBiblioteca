<template>
  <div>
    <h2>Préstamos</h2>

    <form @submit.prevent="crearPrestamo">
      <input v-model="form.libro_id" placeholder="ID Libro" />
      <input v-model="form.usuario_id" placeholder="ID Usuario" />
      <button>Prestar</button>
    </form>

    <ul>
      <li v-for="prestamo in prestamos" :key="prestamo.id">
        Libro: {{ prestamo.libro_id }} | Usuario: {{ prestamo.usuario_id }} | Estado:
        {{ prestamo.estado }}
        <button @click="devolver(p.id)">Devolver</button>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const prestamos = ref([])
const form = ref({
  libro_id: '',
  usuario_id: '',
})

const crearPrestamo = async () => {
  await api.post('/prestamos', form.value)
  alert('Préstamo realizado')
}

const devolver = async (id) => {
  await api.put(`/prestamos/devolver/${id}`)
  alert('Libro devuelto')
}
</script>
