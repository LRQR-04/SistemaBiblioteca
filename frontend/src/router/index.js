import { createRouter, createWebHistory } from 'vue-router'
import AuthLayout from '../layouts/LayoutAuth.vue'
import MainLayout from '../layouts/MainLayout.vue'

import Login from '../views/Login.vue'
import Dashboard from '../views/Dashboard.vue'
import Libros from '../views/Libros.vue'
import Usuarios from '../views/Usuarios.vue'
import Prestamos from '../views/Prestamos.vue'
import Registro from '../views/Registro.vue'

const routes = [
  {
    path: '/',
    component: MainLayout,
    children: [
      { path: '', component: Dashboard, meta: { requiresAuth: true } },
      { path: '/libros', component: Libros, meta: { requiresAuth: true } },
      {
        path: '/usuarios',
        component: Usuarios,
        meta: { requiresAuth: true, roles: ['admin'] },
      },
      { path: '/prestamos', component: Prestamos, meta: { requiresAuth: true } },
    ],
  },
  {
    path: '/',
    component: AuthLayout,
    children: [
      { path: 'login', component: Login },
      { path: 'registro', component: Registro },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (!token && to.meta.requiresAuth) {
    return next('/login')
  }

  const user = token ? JSON.parse(atob(token.split('.')[1])) : null

  if (to.meta.roles && !to.meta.roles.includes(user?.rol)) {
    return next('/')
  }

  next()
})

export default router
