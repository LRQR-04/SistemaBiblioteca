<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'

const props = defineProps({
  usuario: Object,
})

const emit = defineEmits(['close', 'success'])

const form = ref({
  id: null,
  nombre: '',
  email: '',
  rol: '',
})

const errores = ref({
  nombre: '',
  email: '',
})

watch(
  () => props.usuario,
  (val) => {
    if (val) {
      form.value = {
        id: val.id,
        nombre: val.nombre,
        email: val.email,
        rol: val.rol,
      }
    }
  },
  { immediate: true },
)

const validar = () => {
  errores.value = {
    nombre: '',
    email: '',
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

  return !errores.value.nombre && !errores.value.email
}

watch(form, validar, { deep: true })

const guardar = async () => {
  if (!validar()) return

  try {
    const payload = {
      nombre: form.value.nombre,
      email: form.value.email,
      rol: form.value.rol,
    }

    await api.put(`/usuarios/${form.value.id}`, payload)

    emit('success', 'Usuario actualizado correctamente')
    emit('close')
  } catch (err) {
    const msg = err.response?.data?.detail
    console.log(msg)

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
      <!-- Header -->
      <div class="header">
        <h3>Editar Usuario</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- Nombre -->
      <div class="field">
        <input
          v-model="form.nombre"
          placeholder="Nombre completo"
          :class="{ inputError: errores.nombre }"
        />
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

      <!-- Rol -->
      <div class="field">
        <select v-model="form.rol">
          <option value="estudiante">Estudiante</option>
          <option value="profesor">Profesor</option>
          <option value="admin">Admin</option>
        </select>
      </div>

      <!-- Acciones -->
      <div class="actions">
        <button class="btn-secondary" @click="$emit('close')">Cancelar</button>
        <button class="btn-primary" @click="guardar">Guardar cambios</button>
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
  background: none;
  font-size: 18px;
  cursor: pointer;
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
