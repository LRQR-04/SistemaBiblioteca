<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import { useAuthStore } from '../stores/autenticacion'
import ModalPrestamo from '../components/ModalPrestamo.vue'
import ModalEditarPrestamo from '../components/ModalEditarPrestamo.vue'
import Alerta from '../components/Alerta.vue'
import { Pencil, Undo2 } from 'lucide-vue-next'

const auth = useAuthStore()

const prestamos = ref([])
const page = ref(1)
const total = ref(0)

const search = ref('')
const status = ref('all')

const modalCrear = ref(false)
const modalEditar = ref(false)
const prestamoSeleccionado = ref(null)

const alertMsg = ref('')
const alertType = ref('success')

const isAdmin = computed(() => auth.user?.rol === 'admin')

const cargar = async () => {
  const endpoint = isAdmin.value ? '/prestamos' : '/prestamos/mis'

  const res = await api.get(endpoint, {
    params: {
      search: search.value,
      status: status.value,
      page: page.value,
      limit: 10,
    },
  })

  prestamos.value = res.data.data
  total.value = res.data.total
}

onMounted(cargar)

/* Buscar */
const buscar = () => {
  page.value = 1
  cargar()
}

/* Alerta */
const mostrarAlerta = async (msg, type = 'success') => {
  alertMsg.value = msg
  alertType.value = type

  setTimeout(() => (alertMsg.value = ''), 3000)
  await cargar()
}

/* Editar (admin) */
const editar = (p) => {
  prestamoSeleccionado.value = p
  modalEditar.value = true
}

/* Devolver */
const devolver = async (p) => {
  const ok = confirm('¿Deseas confirmar la devolución del libro?')
  if (!ok) return

  try {
    await api.put(`/prestamos/devolver/${p.id}`)
    mostrarAlerta('Libro devuelto')
  } catch (err) {
    mostrarAlerta(err.response?.data?.detail || 'Error', 'error')
  }
}

const totalPages = computed(() => Math.ceil(total.value / 10))
</script>

<template>
  <div class="container">
    <div class="card">
      <Alerta :message="alertMsg" :type="alertType" />

      <div class="header">
        <h2>Préstamos</h2>

        <button v-if="!isAdmin" class="btn-primary" @click="modalCrear = true">
          + Nuevo préstamo
        </button>
      </div>

      <!-- Filtros -->
      <div class="filters">
        <input
          v-model="search"
          :placeholder="isAdmin ? 'Buscar por libro o usuario...' : 'Buscar por libro'"
          @input="buscar"
        />

        <select v-model="status" @change="buscar">
          <option value="all">Todos</option>
          <option value="activo">Activo</option>
          <option value="devuelto">Devuelto</option>
          <option value="vencido">Vencido</option>
        </select>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>#</th>
              <th v-if="isAdmin">Usuario</th>
              <th>Libro</th>
              <th>Fecha préstamo</th>
              <th>Fecha devolución</th>
              <th>Estado</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="(prestamo, index) in prestamos" :key="prestamo.id">
              <td>{{ index + 1 }}</td>
              <td v-if="isAdmin">{{ prestamo.usuario || '-' }}</td>
              <td>{{ prestamo.libro }}</td>
              <td>{{ prestamo.fecha_prestamo }}</td>
              <td>{{ prestamo.fecha_devolucion }}</td>
              <td>
                <span class="badge" :class="prestamo.estado">
                  {{ prestamo.estado }}
                </span>
              </td>
              <td>
                <!-- Admin -->
                <button v-if="isAdmin" class="icon-btn" @click="editar(prestamo)">
                  <Pencil size="16" />
                </button>
                <!-- User -->
                <button
                  v-if="!isAdmin && prestamo.estado !== 'devuelto'"
                  class="icon-btn danger"
                  @click="devolver(prestamo)"
                >
                  <Undo2 size="16" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="prestamos.length === 0" class="empty">No se encontraron resultados</p>
      </div>

      <!-- Paginación -->
      <div class="pagination">
        <button @click="page--" :disabled="page === 1">←</button>
        <span>{{ page }} / {{ totalPages }}</span>
        <button @click="page++" :disabled="page === totalPages">→</button>
      </div>
    </div>

    <!-- Modales -->
    <ModalPrestamo v-if="modalCrear" @close="modalCrear = false" @success="mostrarAlerta" />

    <ModalEditarPrestamo
      v-if="modalEditar"
      :prestamo="prestamoSeleccionado"
      @close="modalEditar = false"
      @success="mostrarAlerta"
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
  border-color: #22c55e;
  box-shadow: 0 0 0 2px rgba(34, 197, 94, 0.2);
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

.badge {
  padding: 4px 8px;
  border-radius: 6px;
  font-size: 12px;
  text-transform: capitalize;
}

.badge.activo {
  background: #dcfce7;
  color: #166534;
}

.badge.devuelto {
  background: #e5e7eb;
  color: #374151;
}

.badge.vencido {
  background: #fee2e2;
  color: #991b1b;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  transition: 0.2s;
}

.icon-btn:hover {
  color: #16a34a;
}

.icon-btn.danger:hover {
  color: #dc2626;
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
  background: #dcfce7;
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
