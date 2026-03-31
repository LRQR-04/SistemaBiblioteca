<template>
  <div>
    <h2>Usuarios</h2>

    <form @submit.prevent="crearUsuario">
      <input v-model="form.nombre" placeholder="Nombre" />
      <input v-model="form.email" placeholder="Email" />
      <input v-model="form.password" type="password" />
      <select v-model="form.tipo">
        <option value="estudiante">Estudiante</option>
        <option value="profesor">Profesor</option>
      </select>
      <button>Crear</button>
    </form>

    <ul>
      <li v-for="usuario in usuarios" :key="usuario.id">
        {{ usuario.nombre }} - {{ usuario.email }}
      </li>
    </ul>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const usuarios = ref([])
const form = ref({
  nombre: '',
  email: '',
  password: '',
  tipo: 'estudiante',
})

const crearUsuario = async () => {
  await api.post('/usuarios', form.value)
  alert('Usuario creado')
}
</script>
