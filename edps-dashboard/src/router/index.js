import LoginView from '@/components/LoginView.vue'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import { useAuthStore } from '@/stores/authStore'; // make sure this store exists
import HomeView from '@/views/HomeView.vue'
import ModelInsightsView from "@/views/ModelInsightsView.vue"
import NotFound from '@/views/NotFound.vue'
import StudentListPage from '@/views/StudentListPage.vue'
import StudentProfilePage from '@/views/StudentProfilePage.vue'
import UploadPage from '@/views/UploadPage.vue'
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { title: 'Login' },
  },
  {
    path: '/',
    component: DashboardLayout,
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Home',
        component: HomeView,
        meta: { title: 'Dashboard Home', requiresAuth: true },
      },
      {
        path: 'students',
        name: 'Students',
        component: StudentListPage,
        meta: { title: 'Student List', requiresAuth: true },
      },
      {
        path: 'students/:id',
        name: 'StudentProfile',
        component: StudentProfilePage,
        meta: { title: 'Student Profile', requiresAuth: true },
      },
      {
        path: 'upload',
        name: 'UploadCSV',
        component: UploadPage,
        meta: { title: 'Upload CSV', requiresAuth: true },
      },
      {
        path: "/insights",
        name: "ModelInsights",
        component: ModelInsightsView,
        meta: { requiresAuth: true }
      },
      {
        path: 'admin',
        name: 'Admin',
        component: () => import('@/views/AdminView.vue'),
        meta: { title: 'Admin Panel', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: '/predictions',
        name: 'Predictions',
        component: () => import('@/views/PredictionsView.vue')  // you'll create this file next
      }
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Page Not Found' },
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  const token = localStorage.getItem('token')
  const tokenExpiry = localStorage.getItem('token_expiry')

  if (token && tokenExpiry && Date.now() > parseInt(tokenExpiry)) {
    authStore.logout()
    return next('/login')
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  next()
})

router.afterEach((to) => {
  document.title = to.meta.title ? `EDPS | ${to.meta.title}` : 'EDPS'
})

export default router