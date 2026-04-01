<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'

const emit = defineEmits(['close', 'success'])

const form = ref({
  isbn: '',
  titulo: '',
  autor: '',
  estado: 'disponible',
  copias_disponibles: '',
})

const errores = ref({
  isbn: '',
  titulo: '',
  autor: '',
  copias_disponibles: '',
})

const validar = () => {
  errores.value = {
    isbn: '',
    titulo: '',
    autor: '',
    copias_disponibles: '',
  }

  // ISBN
  if (!form.value.isbn) {
    errores.value.isbn = 'El campo es obligatorio'
  } else if (form.value.isbn.length < 10 || form.value.isbn.length > 13) {
    errores.value.isbn = 'Debe tener entre 10 y 13 caracteres'
  }

  // Título
  if (!form.value.titulo) {
    errores.value.titulo = 'El campo es obligatorio'
  } else if (form.value.titulo.length < 3 || form.value.titulo.length > 100) {
    errores.value.titulo = 'Debe tener entre 3 y 100 caracteres'
  }

  // Autor
  if (!form.value.autor) {
    errores.value.autor = 'El campo es obligatorio'
  } else if (form.value.autor.length < 3 || form.value.autor.length > 100) {
    errores.value.autor = 'Debe tener entre 3 y 100 caracteres'
  }

  // Copias
  const copias = Number(form.value.copias_disponibles)

  if (form.value.copias_disponibles === '' || form.value.copias_disponibles === null) {
    errores.value.copias_disponibles = 'El campo es obligatorio'
  } else if (isNaN(copias)) {
    errores.value.copias_disponibles = 'Ingrese un número válido'
  } else if (copias <= 0) {
    errores.value.copias_disponibles = 'La cantidad debe ser mayor a 0'
  } else if (copias > 10) {
    errores.value.copias_disponibles = 'La cantidad no puede superar las 10 copias'
  }

  return (
    !errores.value.isbn &&
    !errores.value.titulo &&
    !errores.value.autor &&
    !errores.value.copias_disponibles
  )
}

watch(form, validar, { deep: true })

const guardar = async () => {
  if (!validar()) return

  try {
    await api.post('/libros', form.value)
    emit('success', 'Libro agregado correctamente')
    emit('close')
  } catch (err) {
    const msg = err.response?.data?.detail

    if (msg === 'El ISBN ya está registrado') {
      errores.value.isbn = 'El ISBN ya está registrado'
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
        <h3>Crear Libro</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- ISBN -->
      <div class="field">
        <input v-model="form.isbn" placeholder="ISBN" :class="{ inputError: errores.isbn }" />
        <span class="error-text">{{ errores.isbn }}</span>
      </div>

      <!-- Título -->
      <div class="field">
        <input
          v-model="form.titulo"
          type="text"
          placeholder="Título"
          :class="{ inputError: errores.titulo }"
        />
        <span class="error-text">{{ errores.titulo }}</span>
      </div>

      <!-- Autor -->
      <div class="field">
        <input
          v-model="form.autor"
          type="text"
          placeholder="Autor"
          :class="{ inputError: errores.autor }"
        />
        <span class="error-text">{{ errores.autor }}</span>
      </div>

      <!-- Estatus -->
      <div class="field">
        <select v-model="form.estado">
          <option value="disponible">Disponible</option>
          <option value="prestado">Prestado</option>
          <option value="reparacion">Reparación</option>
        </select>
      </div>

      <!-- Copias disponibles -->
      <div class="field">
        <input
          type="number"
          v-model.number="form.copias_disponibles"
          min="1"
          max="10"
          step="1"
          placeholder="Copias disponibles"
        />
        <span class="error-text">{{ errores.copias_disponibles }}</span>
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
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 999;
}

.modal-card {
  background: white;
  padding: 20px;
  width: 360px;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  animation: fadeIn 0.2s ease;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.close-btn {
  border: none;
  background: #f1f5f9;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  cursor: pointer;
  transition: 0.2s;
}

.close-btn:hover {
  background: #e2e8f0;
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
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.2);
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
  background: linear-gradient(135deg, #0ea5e9, #2563eb);
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
}

.btn-secondary {
  background: #e5e7eb;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
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
