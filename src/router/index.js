import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/HomePage.vue'
const routes = [
  {
    path: '/',
    name: 'home',
    component: HomePage
  },

  {
    path: '/admin_login',
    name: 'admin_login',
    component: () => import( '@/components/AdminLogin.vue')

  },

  {
    path: '/user_login',
    name: 'user_login',
    component: () => import( '@/components/UserLogin.vue')

  },

  {
    path: '/user_signup',
    name: 'user_signup',
    component: () => import( '@/components/UserSignup.vue')

  },

  {
    path: '/admin_dashboard',
    name: 'admin_dashboard',
    component: () => import( '@/components/AdminDashboard.vue')

  },

  {
    path: '/customer_dashboard',
    name: 'customer_dashboard',
    component: () => import( '@/components/CustomerDashboard.vue')

  },

  {
    path: '/service_professional_dashboard',
    name: 'service_professional_dashboard',
    component: () => import( '@/components/ServiceProfessionalDashboard.vue')

  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router