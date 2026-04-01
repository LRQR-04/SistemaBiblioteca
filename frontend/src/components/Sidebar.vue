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
        <div class="avatar">
          {{ auth.user?.sub?.charAt(0).toUpperCase() }}
        </div>
        <div>
          <strong>{{ auth.user?.sub }}</strong>
          <small>{{ rol }}</small>
        </div>
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
  width: 240px;
  height: 100vh;
  background: linear-gradient(180deg, #1f2937, #111827);
  color: white;
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  padding: 20px;
  border-right: 1px solid rgba(255, 255, 255, 0.05);
}

.logo {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 30px;
  display: flex;
  align-items: center;
  gap: 10px;
  letter-spacing: 0.5px;
}

nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.link {
  display: flex;
  align-items: center;
  gap: 12px;
  color: #d1d5db;
  text-decoration: none;
  padding: 10px 12px;
  border-radius: 10px;
  transition: all 0.25s ease;
  font-size: 14px;
}

.link:hover {
  background: rgba(255, 255, 255, 0.08);
  color: white;
  transform: translateX(4px);
}

.link.router-link-active {
  background: linear-gradient(135deg, #6366f1, #7c3aed);
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.4);
}

footer {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #6366f1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.user strong {
  font-size: 14px;
}

.user small {
  display: block;
  font-size: 12px;
  opacity: 0.6;
}

button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  background: linear-gradient(135deg, #ef4444, #dc2626);
  border: none;
  padding: 10px;
  color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: 0.3s;
  font-weight: 500;
  margin-top: 20px;
}

button:hover {
  transform: scale(1.03);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);
}
</style>
