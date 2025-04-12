import { createRouter, createWebHashHistory } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import HomeView from '@/views/HomeView.vue'
import StudentListPage from '@/views/StudentListPage.vue'
import UploadPage from '@/views/UploadPage.vue'
import StudentProfilePage from '@/views/StudentProfilePage.vue'
import NotFound from '@/views/NotFound.vue'
import LoginView from '@/components/LoginView.vue'
import { useAuthStore } from '@/stores/authStore' // make sure this store exists

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
  history: createWebHashHistory(),
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