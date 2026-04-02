<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '../services/api'
import ModalCrearLibro from '../components/ModalCrearLibro.vue'
import ModalEditarLibro from '../components/ModalEditarLibro.vue'
import Alerta from '../components/Alerta.vue'
import { Pencil } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/autenticacion'

const auth = useAuthStore()

const libros = ref([])
const page = ref(1)
const total = ref(0)

const search = ref('')
const status = ref('all')

const modalCrear = ref(false)
const modalEditar = ref(false)
const libroSeleccionado = ref(null)

const alertMsg = ref('')
const alertType = ref('success')

const isAdmin = computed(() => auth.user?.rol === 'admin')

const cargar = async () => {
  const res = await api.get('/libros', {
    params: {
      search: search.value,
      status: status.value,
      page: page.value,
      limit: 10,
    },
  })

  libros.value = res.data.data
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
  modalCrear.value = true
}

/* Editar */
const editar = (libro) => {
  libroSeleccionado.value = { ...libro }
  modalEditar.value = true
}

/* Alertas y actualización */
const handleSuccess = async (msg, type = 'success') => {
  alertMsg.value = msg
  alertType.value = type

  setTimeout(() => (alertMsg.value = ''), 3000)

  await cargar()
}

/* Paginación */
const totalPages = computed(() => Math.ceil(total.value / 10))
</script>

<template>
  <div class="container">
    <div class="card">
      <Alerta :message="alertMsg" :type="alertType" />

      <div class="header">
        <h2>Libros</h2>
        <button v-if="isAdmin" class="btn-primary" @click="nuevo">+ Nuevo</button>
      </div>

      <!-- Filtros -->
      <div class="filters">
        <input v-model="search" placeholder="Buscar por título o autor..." @input="buscar" />

        <select v-model="status" @change="buscar">
          <option value="all">Todos</option>
          <option value="disponible">Disponibles</option>
          <option value="prestado">Prestados</option>
          <option value="reparacion">En reparación</option>
        </select>
      </div>

      <div class="table-container">
        <table>
          <thead>
            <tr>
              <th>ISBN</th>
              <th>Título</th>
              <th>Autor</th>
              <th>Estatus</th>
              <th>Copias disponibles</th>
              <th>Acciones</th>
            </tr>
          </thead>

          <tbody>
            <tr v-for="libro in libros" :key="libro.id">
              <td>{{ libro.isbn }}</td>
              <td>{{ libro.titulo }}</td>
              <td>{{ libro.autor }}</td>
              <td>
                <span class="badge" :class="libro.estado">
                  {{ libro.estado }}
                </span>
              </td>
              <td>{{ libro.copias_disponibles }}</td>
              <td>
                <button class="icon-btn" @click="editar(libro)">
                  <Pencil size="16" />
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-if="libros.length === 0" class="empty">No se encontraron resultados</p>
      </div>

      <!-- Paginación -->
      <div class="pagination">
        <button @click="page--" :disabled="page === 1">←</button>
        <span>{{ page }} / {{ totalPages }}</span>
        <button @click="page++" :disabled="page === totalPages">→</button>
      </div>
    </div>

    <!-- Modales -->
    <ModalCrearLibro v-if="modalCrear" @close="modalCrear = false" @success="handleSuccess" />

    <ModalEditarLibro
      v-if="modalEditar"
      :libro="libroSeleccionado"
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
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.25);
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
  border-color: #2563eb;
  box-shadow: 0 0 0 2px rgba(37, 99, 235, 0.15);
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

.badge.disponible {
  background: #dcfce7;
  color: #166534;
}

.badge.prestado {
  background: #fee2e2;
  color: #991b1b;
}

.badge.reparacion {
  background: #fef9c3;
  color: #854d0e;
}

.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  color: #6b7280;
  transition: 0.2s;
}

.icon-btn:hover {
  color: #2563eb;
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
