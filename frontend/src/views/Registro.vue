<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'
import { useRouter } from 'vue-router'

const nombre = ref('')
const correo = ref('')
const contrasenia = ref('')
const rol = ref('estudiante')

const errores = ref({
  nombre: '',
  correo: '',
  contrasenia: '',
})

const router = useRouter()

const validar = () => {
  errores.value = {
    nombre: '',
    correo: '',
    contrasenia: '',
  }

  // Nombre
  if (!nombre.value) {
    errores.value.nombre = 'El campo es obligatorio'
  } else if (nombre.value.length < 3 || nombre.value.length > 100) {
    errores.value.nombre = 'Debe tener entre 3 y 100 caracteres'
  }

  // Correo
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!correo.value) {
    errores.value.correo = 'El campo es obligatorio'
  } else if (!emailRegex.test(correo.value)) {
    errores.value.correo = 'Correo inválido'
  }

  // Password
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#_-]).{8,}$/

  if (!contrasenia.value) {
    errores.value.contrasenia = 'El campo es obligatorio'
  } else if (!passwordRegex.test(contrasenia.value)) {
    errores.value.contrasenia = 'Debe tener 8 caracteres, mayúscula, minúscula, número y símbolo'
  }

  return !errores.value.nombre && !errores.value.correo && !errores.value.contrasenia
}

watch([nombre, correo, contrasenia], () => {
  validar()
})

const registro = async () => {
  if (!validar()) return

  try {
    await api.post('/auth/registro', {
      nombre: nombre.value,
      email: correo.value,
      contrasenia: contrasenia.value,
      rol: rol.value,
    })
    alert('Registro exitoso')
    router.push('/login')
  } catch (err) {
    const msg = err.response?.data?.detail

    if (msg === 'El correo ya está registrado') {
      errores.value.correo = 'El correo ya está registrado'
    } else {
      errores.value.correo = 'Error al registrar usuario'
    }
  }
}
</script>

<template>
  <div class="register-container">
    <div class="register-card">
      <h2>Crear cuenta</h2>
      <p class="subtitle">Completa los datos para registrarte</p>

      <div class="field">
        <input v-model="nombre" placeholder="Nombre" :class="{ inputError: errores.nombre }" />
        <span class="error-text">{{ errores.nombre }}</span>
      </div>

      <div class="field">
        <input
          v-model="correo"
          type="email"
          placeholder="Correo electrónico"
          :class="{ inputError: errores.correo }"
        />
        <span class="error-text">{{ errores.correo }}</span>
      </div>

      <div class="field">
        <input
          v-model="contrasenia"
          type="password"
          placeholder="Contraseña"
          :class="{ inputError: errores.contrasenia }"
        />
        <span class="error-text">{{ errores.contrasenia }}</span>
      </div>

      <div class="field">
        <select v-model="rol">
          <option value="estudiante">Estudiante</option>
          <option value="profesor">Profesor</option>
        </select>
      </div>

      <button @click="registro">Registrarse</button>

      <p class="login-text">
        ¿Ya tienes cuenta?
        <router-link to="/login">Inicia sesión</router-link>
      </p>
    </div>
  </div>
</template>

<style scoped>
.register-container {
  height: 100vh;
  padding: 30px 0;
  display: flex;
  justify-content: center;
  align-items: center;
  background: linear-gradient(135deg, #9333ea, #4f46e5);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.register-card {
  background: white;
  padding: 2rem;
  width: 360px;
  border-radius: 16px;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.register-card h2 {
  margin-bottom: 0.5rem;
}

.subtitle {
  font-size: 0.9rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.field {
  display: flex;
  flex-direction: column;
  margin-bottom: 1rem;
}

input,
select {
  width: 100%;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
  outline: none;
  transition: 0.3s;
}

input:focus,
select:focus {
  border-color: #7c3aed;
  box-shadow: 0 0 5px rgba(124, 58, 237, 0.5);
}

.inputError {
  border: 1px solid red;
}

.error-text {
  color: red;
  font-size: 12px;
}

button {
  width: 100%;
  padding: 10px;
  border: none;
  border-radius: 10px;
  background: #7c3aed;
  color: white;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

button:hover {
  background: #6d28d9;
  transform: scale(1.02);
}

.login-text {
  margin-top: 1rem;
  font-size: 0.85rem;
}

.login-text a {
  color: #7c3aed;
  font-weight: bold;
  text-decoration: none;
}
</style>
