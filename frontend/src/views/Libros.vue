<template>
  <div>
    <h2>Libros</h2>

    <form @submit.prevent="crearLibro">
      <input v-model="form.isbn" placeholder="ISBN" />
      <input v-model="form.titulo" placeholder="Título" />
      <input v-model="form.autor" placeholder="Autor" />
      <input v-model="form.copias_disponibles" type="number" />
      <button>Agregar</button>
    </form>

    <ul>
      <li v-for="libro in libros" :key="libro.id">{{ libro.titulo }} - {{ libro.autor }}</li>
    </ul>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '../services/api'

const libros = ref([])
const form = ref({
  isbn: '',
  titulo: '',
  autor: '',
  copias_disponibles: 1,
})

const cargarLibros = async () => {
  const res = await api.get('/libros')
  libros.value = res.data
}

const crearLibro = async () => {
  await api.post('/libros', form.value)
  cargarLibros()
}

onMounted(cargarLibros)
</script>
