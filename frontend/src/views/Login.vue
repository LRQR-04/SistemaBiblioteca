<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/autenticacion.js'
import { useRouter } from 'vue-router'

const email = ref('')
const contrasenia = ref('')
const error = ref('')
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  error.value = ''

  try {
    loading.value = true
    await auth.login(email.value, contrasenia.value)
    router.push('/')
  } catch (err) {
    const msg = err.response?.data?.detail

    if (msg === 'El usuario no esta registrado') {
      error.value = 'El usuario no esta registrado'
    } else if (msg === 'Su cuenta se encuentra inactiva') {
      error.value = 'Su cuenta se encuentra inactiva'
    } else if (msg === 'Credenciales incorrectas') {
      error.value = 'Credenciales incorrectas'
    } else {
      error.value = 'Error al iniciar sesión'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-container">
    <div class="login-card">
      <h2>Bienvenid@</h2>
      <p class="subtitle">Inicia sesión para continuar</p>

      <form @submit.prevent="handleLogin">
        <div class="input-group">
          <input
            v-model="email"
            type="email"
            placeholder="Correo electrónico"
            :class="{ inputError: error }"
          />
        </div>

        <div class="input-group">
          <input v-model="contrasenia" type="password" placeholder="Contraseña" />
        </div>

        <span v-if="error" class="error-text">
          {{ error }}
        </span>

        <button type="submit" :disabled="loading">
          {{ loading ? 'Ingresando...' : 'Ingresar' }}
        </button>
      </form>

      <p class="register-text">
        ¿No tienes cuenta?
        <router-link to="/registro">Regístrate</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.login-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #4f46e5, #9333ea);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.login-card {
  background: white;
  padding: 2rem;
  width: 350px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.login-card h2 {
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.input-group {
  margin-bottom: 1rem;
}

input {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
  outline: none;
  transition: 0.3s;
}

input:focus {
  border-color: #6366f1;
  box-shadow: 0 0 5px rgba(99, 102, 241, 0.5);
}

.inputError {
  border: 1px solid red;
}

.error-text {
  color: red;
  font-size: 0.8rem;
  display: block;
  margin-bottom: 10px;
}

button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 10px;
  background: #4f46e5;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #4338ca;
  transform: scale(1.02);
}

.register-text {
  margin-top: 1rem;
  font-size: 0.85rem;
}

.register-text a {
  color: #4f46e5;
  font-weight: bold;
  text-decoration: none;
}
</style>
