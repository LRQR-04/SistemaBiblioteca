<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'

const emit = defineEmits(['close', 'success'])

const form = ref({
  nombre: '',
  email: '',
  contrasenia: '',
  rol: 'estudiante',
})

const errores = ref({
  nombre: '',
  email: '',
  contrasenia: '',
})

/* Validación */
const validar = () => {
  errores.value = {
    nombre: '',
    email: '',
    contrasenia: '',
  }

  // Nombre
  if (!form.value.nombre) {
    errores.value.nombre = 'El campo es obligatorio'
  } else if (form.value.nombre.length < 3 || form.value.nombre.length > 100) {
    errores.value.nombre = 'Debe tener entre 3 y 100 caracteres'
  }

  // Email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.value.email) {
    errores.value.email = 'El campo es obligatorio'
  } else if (!emailRegex.test(form.value.email)) {
    errores.value.email = 'Correo inválido'
  }

  // Contraseña
  const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.#_-]).{8,}$/
  if (!form.value.contrasenia) {
    errores.value.contrasenia = 'El campo es obligatorio'
  } else if (!passwordRegex.test(form.value.contrasenia)) {
    errores.value.contrasenia = 'Debe tener 8 caracteres, mayúscula, minúscula, número y símbolo'
  }

  return !errores.value.nombre && !errores.value.email && !errores.value.contrasenia
}

/* Validación en tiempo real */
watch(form, validar, { deep: true })

const guardar = async () => {
  if (!validar()) return

  try {
    await api.post('/usuarios', form.value)

    emit('success', 'Usuario creado correctamente')
    emit('close')
  } catch (err) {
    const msg = err.response?.data?.detail

    if (msg === 'El correo ya está registrado') {
      errores.value.email = 'Este correo ya está en uso'
    } else {
      emit('success', msg || 'Error', 'error')
    }
  }
}
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="header">
        <h3>Crear Usuario</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- Nombre -->
      <div class="field">
        <input v-model="form.nombre" placeholder="Nombre" :class="{ inputError: errores.nombre }" />
        <span class="error-text">{{ errores.nombre }}</span>
      </div>

      <!-- Email -->
      <div class="field">
        <input
          v-model="form.email"
          type="email"
          placeholder="Correo electrónico"
          :class="{ inputError: errores.email }"
        />
        <span class="error-text">{{ errores.email }}</span>
      </div>

      <!-- Password -->
      <div class="field">
        <input
          v-model="form.contrasenia"
          type="password"
          placeholder="Contraseña"
          :class="{ inputError: errores.contrasenia }"
        />
        <span class="error-text">{{ errores.contrasenia }}</span>
      </div>

      <!-- Rol -->
      <div class="field">
        <select v-model="form.rol">
          <option value="estudiante">Estudiante</option>
          <option value="profesor">Profesor</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <!-- Botones -->
      <div class="actions">
        <button class="btn-secondary" @click="$emit('close')">Cancelar</button>
        <button class="btn-primary" @click="guardar">Guardar</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
  backdrop-filter: blur(4px);
}

.modal-card {
  background: white;
  padding: 20px;
  width: 350px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.2s ease;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  border: none;
  background: #f3f4f6;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  cursor: pointer;
  transition: 0.2s;
}

.close-btn:hover {
  background: #e5e7eb;
}

.field {
  display: flex;
  flex-direction: column;
  margin-bottom: 12px;
}

input,
select {
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #ddd;
  outline: none;
  transition: 0.3s;
}

input:focus,
select:focus {
  border-color: #6366f1;
  box-shadow: 0 0 5px rgba(99, 102, 241, 0.5);
}

.inputError {
  border: 1px solid red;
}

.error-text {
  color: red;
  font-size: 0.75rem;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.btn-secondary {
  background: #e5e7eb;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.btn-secondary:hover {
  background: #d1d5db;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>
