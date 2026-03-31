<template>
  <nav>
    <router-link to="/">Dashboard</router-link>
    <router-link to="/libros">Libros</router-link>
    <router-link to="/usuarios">Usuarios</router-link>
    <router-link to="/prestamos">Préstamos</router-link>

    <button @click="logout">Salir</button>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/autenticacion.js'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>
