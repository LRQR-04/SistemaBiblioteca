<script setup>
import { ref, watch } from 'vue'
import api from '../services/api'

const props = defineProps({
  prestamo: Object,
})

const emit = defineEmits(['close', 'success'])

const form = ref({
  estado: '',
  fecha_devolucion: '',
})

const errores = ref({
  estado: '',
  fecha_devolucion: '',
  general: '',
})

watch(
  () => props.prestamo,
  (val) => {
    if (val) {
      form.value = {
        estado: val.estado,
        fecha_devolucion: val.fecha_devolucion,
      }
    }
  },
  { immediate: true },
)

const validar = () => {
  errores.value = {
    estado: '',
    fecha_devolucion: '',
    general: '',
  }

  if (!form.value.estado) {
    errores.value.estado = 'Selecciona un estado'
  }

  if (!form.value.fecha_devolucion) {
    errores.value.fecha_devolucion = 'Selecciona una fecha'
  }

  return !errores.value.estado && !errores.value.fecha_devolucion
}

watch(form, validar, { deep: true })

const guardar = async () => {
  if (!validar()) return

  const confirmacion = confirm('¿Confirmar cambios en el préstamo?')
  if (!confirmacion) return

  try {
    await api.patch(`/prestamos/${props.prestamo.id}`, {
      estado: form.value.estado,
      fecha_devolucion: form.value.fecha_devolucion,
    })

    emit('success', 'Préstamo actualizado')
    emit('close')
  } catch (err) {
    const msg = err.response?.data?.detail || 'Error al actualizar'

    if (msg.includes('fecha')) {
      errores.value.fecha_devolucion = msg
    } else if (msg.includes('Estado')) {
      errores.value.estado = msg
    } else {
      errores.value.general = msg
    }
  }
}
</script>

<template>
  <div class="overlay" @click.self="$emit('close')">
    <div class="modal-card">
      <div class="header">
        <h3>Editar Préstamo</h3>
        <button class="close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- Estado -->
      <div class="field">
        <select v-model="form.estado" :class="{ inputError: errores.estado }">
          <option value="">Selecciona estado</option>
          <option value="activo">Activo</option>
          <option value="devuelto">Devuelto</option>
          <option value="vencido">Vencido</option>
        </select>
        <span class="error-text">{{ errores.estado }}</span>
      </div>

      <!-- Fecha devolución -->
      <div class="field">
        <input
          type="date"
          v-model="form.fecha_devolucion"
          :class="{ inputError: errores.fecha_devolucion }"
        />
        <span class="error-text">{{ errores.fecha_devolucion }}</span>
      </div>

      <!-- Error general -->
      <span v-if="errores.general" class="error-box">
        {{ errores.general }}
      </span>

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
  border-color: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
}

.inputError {
  border: 1px solid red;
}

.error-text {
  color: red;
  font-size: 0.75rem;
}

.error-box {
  background: #fee2e2;
  color: #991b1b;
  padding: 8px;
  border-radius: 6px;
  font-size: 12px;
}

.actions {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  margin-top: 10px;
}

.btn-primary {
  background: linear-gradient(135deg, #22c55e, #16a34a);
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
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
