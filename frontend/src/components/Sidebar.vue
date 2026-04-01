<script setup>
import { computed } from 'vue'
import { useAuthStore } from '../stores/autenticacion.js'
import { useRouter } from 'vue-router'

import { LayoutDashboard, BookOpen, Users, Repeat, LogOut } from 'lucide-vue-next'

const auth = useAuthStore()
const router = useRouter()

const rol = computed(() => auth.user?.rol)

const menu = computed(() => {
  if (rol.value === 'admin') {
    return [
      { name: 'Dashboard', path: '/', icon: LayoutDashboard },
      { name: 'Libros', path: '/libros', icon: BookOpen },
      { name: 'Usuarios', path: '/usuarios', icon: Users },
      { name: 'Préstamos', path: '/prestamos', icon: Repeat },
    ]
  }

  if (rol.value === 'profesor' || rol.value === 'estudiante') {
    return [
      { name: 'Dashboard', path: '/', icon: LayoutDashboard },
      { name: 'Libros', path: '/libros', icon: BookOpen },
      { name: 'Préstamos', path: '/prestamos', icon: Repeat },
    ]
  }
})

const logout = () => {
  auth.logout()
  router.push('/login')
}
</script>

<template>
  <aside class="sidebar">
    <div class="logo">Biblioteca</div>

    <nav>
      <router-link v-for="item in menu" :key="item.path" :to="item.path" class="link">
        <component :is="item.icon" size="18" />
        <span>{{ item.name }}</span>
      </router-link>
    </nav>

    <div class="footer">
      <div class="user">
        {{ auth.user?.sub }}
        <small>{{ rol }}</small>
      </div>

      <button @click="logout">
        <LogOut size="16" />
        Salir
      </button>
    </div>
  </aside>
</template>

<style scoped>
.sidebar {
  width: 200px;
  height: 100vh;
  background: #1f2937;
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 20px;
}

.logo {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 25px;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.link {
  display: flex;
  align-items: center;
  gap: 10px;
  color: white;
  text-decoration: none;
  padding: 10px;
  border-radius: 8px;
  transition: 0.2s;
}

.link:hover {
  background: #374151;
}

.link.router-link-active {
  background: #6366f1;
}

.footer {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user {
  font-size: 14px;
}

small {
  display: block;
  opacity: 0.7;
}

button {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #ef4444;
  border: none;
  padding: 10px;
  color: white;
  border-radius: 6px;
  cursor: pointer;
}

button:hover {
  background: #dc2626;
}
</style>
