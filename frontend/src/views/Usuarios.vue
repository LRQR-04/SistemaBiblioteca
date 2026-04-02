<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import ModalCrearUsuario from '../components/ModalCrearUsuario.vue'
import ModalEditarUsuario from '../components/ModalEditarUsuario.vue'
import Alerta from '../components/Alerta.vue'
import { useAuthStore } from '../stores/autenticacion.js'
import { Pencil } from 'lucide-vue-next'

const auth = useAuthStore()

const usuarios = ref([])
const page = ref(1)
const total = ref(0)

const search = ref('')
const status = ref('all')

const modalCrear = ref(false)
const modalEditar = ref(false)
const usuarioSeleccionado = ref(null)

const alertMsg = ref('')
const alertType = ref('success')

/* Cargar usuarios */
const cargar = async () => {
  const res = await api.get('/usuarios', {
    params: {
      search: search.value,
      status: status.value,
      page: page.value,
      limit: 10,
    },
  })

  usuarios.value = res.data.data
  total.value = res.data.total
}

onMounted(cargar)

/* Buscar */
const buscar = () => {
  page.value = 1
  cargar()
}

/* Crear */
const nuevo = () => {
  usuarioSeleccionado.value = null
  modalCrear.value = true
}

/* Editar */
const editar = (u) => {
  if (u.rol === 'admin' && u.id !== auth.user.user_id) return
  usuarioSeleccionado.value = u
  modalEditar.value = true
}

/* Cambio estado */
const toggleEstado = async (e, usuario) => {
  const nuevoEstado = e.target.checked

  if (usuario.rol === 'admin' && usuario.id !== auth.user.user_id) {
    e.target.checked = !nuevoEstado
    mostrarAlerta('No puedes modificar otro administrador', 'error')
    return
  }

  const confirmacion = confirm(
    `¿Seguro que deseas ${nuevoEstado ? 'activar' : 'suspender'} este usuario?`,
  )

  if (!confirmacion) {
    e.target.checked = !nuevoEstado
    return
  }

  try {
    await api.patch(`/usuarios/${usuario.id}/estado`)
    mostrarAlerta('Estado actualizado correctamente')

    await cargar()
  } catch (error) {
    e.target.checked = !nuevoEstado

    const msg = error.response?.data?.detail || 'Error al actualizar estado'
    mostrarAlerta(msg, 'error')
  }
}

/* Alertas */
const mostrarAlerta = (msg, type = 'success') => {
  alertMsg.value = msg
  alertType.value = type

  setTimeout(() => (alertMsg.value = ''), 3000)
}

/* Paginación */
const totalPages = computed(() => Math.ceil(total.value / 10))

const handleSuccess = async (msg, type = 'success') => {
  mostrarAlerta(msg, type)

  // Actualizar tabla
  await cargar()
}
</script>

<template>
  <div class="container">
    <Alerta :message="alertMsg" :type="alertType" />

    <div class="header">
      <h2>Usuarios</h2>
      <button class="btn-primary" @click="nuevo">+ Nuevo</button>
    </div>

    <!-- Filtros -->
    <div class="filters">
      <input v-model="search" placeholder="Buscar usuario..." @input="buscar" />

      <select v-model="status" @change="buscar">
        <option value="all">Todos</option>
        <option value="activo">Activos</option>
        <option value="suspendido">Suspendidos</option>
      </select>
    </div>

    <div class="table-container">
      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Nombre</th>
            <th>Email</th>
            <th>Rol</th>
            <th>Préstamos disponibles</th>
            <th>Estatus</th>
            <th>Acciones</th>
          </tr>
        </thead>

        <tbody>
          <tr v-for="(usuario, index) in usuarios" :key="usuario.id">
            <td>{{ index + 1 }}</td>
            <td class="user-cell">
              <div class="avatar">
                {{ usuario.nombre.charAt(0).toUpperCase() }}
              </div>
              {{ usuario.nombre }}
            </td>
            <td>{{ usuario.email }}</td>
            <td>
              <span class="badge">{{ usuario.rol }}</span>
            </td>
            <td>{{ usuario.prestamos_disponibles }}</td>
            <td>
              <label class="switch">
                <input
                  type="checkbox"
                  :checked="usuario.estado === 'activo'"
                  @change="(e) => toggleEstado(e, usuario)"
                />
                <span class="slider"></span>
              </label>
            </td>
            <td>
              <button class="icon-btn" @click="editar(usuario)">
                <Pencil size="16" />
              </button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-if="usuarios.length === 0" class="empty">No se encontraron resultados</p>
    </div>

    <!-- Paginación -->
    <div class="pagination">
      <button @click="page--" :disabled="page === 1">←</button>
      <span>{{ page }} / {{ totalPages }}</span>
      <button @click="page++" :disabled="page === totalPages">→</button>
    </div>

    <!-- Modals -->
    <ModalCrearUsuario v-if="modalCrear" @close="modalCrear = false" @success="handleSuccess" />

    <ModalEditarUsuario
      v-if="modalEditar"
      :usuario="usuarioSeleccionado"
      @close="modalEditar = false"
      @success="handleSuccess"
    />
  </div>
</template>

<style scoped>
.container {
  padding: 10px;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.btn-primary {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  border: none;
  padding: 8px 14px;
  border-radius: 8px;
  cursor: pointer;
  transition: 0.2s;
}

.btn-primary:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(137, 85, 227, 0.25);
}

.filters {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

input,
select {
  padding: 8px;
  border-radius: 8px;
  border: 1px solid #ddd;
  transition: 0.2s;
}

input:focus,
select:focus {
  border-color: #7125eb;
  box-shadow: 0 0 0 2px rgba(137, 85, 227, 0.25);
  outline: none;
}

.table-container {
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px;
  text-align: left;
}

thead {
  background: #f9fafb;
}

tbody tr:hover {
  background: #f3f4f6;
}

.user-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  background: #6366f1;
  color: white;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.badge {
  background: #e0e7ff;
  color: #3730a3;
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
}

.switch {
  position: relative;
  display: inline-block;
  width: 40px;
  height: 20px;
}

.switch input {
  display: none;
}

.slider {
  position: absolute;
  cursor: pointer;
  background: #ccc;
  border-radius: 20px;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  transition: 0.3s;
}

.slider::before {
  content: '';
  position: absolute;
  height: 14px;
  width: 14px;
  left: 3px;
  bottom: 3px;
  background: white;
  border-radius: 50%;
  transition: 0.3s;
}

input:checked + .slider {
  background: #22c55e;
}

input:checked + .slider::before {
  transform: translateX(20px);
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  transition: 0.2s;
}

.icon-btn:hover {
  color: #4f46e5;
}

.pagination {
  margin-top: 15px;
  display: flex;
  justify-content: center;
  gap: 10px;
}

.pagination button {
  padding: 6px 10px;
  border: none;
  background: #e5e7eb;
  border-radius: 6px;
  cursor: pointer;
}

.pagination button:hover {
  background: #dbeafe;
}

.pagination button:disabled {
  opacity: 0.5;
}

.empty {
  text-align: center;
  padding: 12px;
  color: #6b7280;
}
</style>
