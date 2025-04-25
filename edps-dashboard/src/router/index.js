import { useAuthStore } from '@/stores/authStore';
import { createRouter, createWebHistory } from 'vue-router';

import LoginView from '@/components/LoginView.vue';
import DashboardLayout from '@/layouts/DashboardLayout.vue';
import AdminView from '@/views/AdminView.vue';
import HomeView from '@/views/HomeView.vue';
import ModelInsightsView from '@/views/ModelInsightsView.vue';
import NotFound from '@/views/NotFound.vue';
import PredictionsView from '@/views/PredictionsView.vue';
import StudentListPage from '@/views/StudentListPage.vue';
import StudentProfile from '@/views/StudentProfileView.vue';
import UploadPage from '@/views/UploadPage.vue';

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
        meta: { title: 'Dashboard', requiresAuth: true },
      },
      {
        path: 'students',
        name: 'Students',
        component: StudentListPage,
        meta: { title: 'Student List', requiresAuth: true },
      },
      {
        path: 'students/:student_number',
        name: 'StudentProfile',
        component: StudentProfile,
        meta: { title: 'Student Profile', requiresAuth: true },
      },
      {
        path: 'upload',
        name: 'UploadCSV',
        component: UploadPage,
        meta: { title: 'Upload Data', requiresAuth: true },
      },
      {
        path: 'insights',
        name: 'ModelInsights',
        component: ModelInsightsView,
        meta: { title: 'Model Insights', requiresAuth: true },
      },
      {
        path: 'admin',
        name: 'Admin',
        component: AdminView,
        meta: { title: 'Admin Panel', requiresAuth: true, requiresAdmin: true },
      },
      {
        path: 'predictions',
        name: 'Predictions',
        component: PredictionsView,
        meta: { title: 'Predictions', requiresAuth: true },
      }
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: { title: 'Page Not Found' },
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Navigation Guards
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const token = localStorage.getItem('token');
  const expiry = localStorage.getItem('token_expiry');

  if (token && expiry && Date.now() > parseInt(expiry)) {
    authStore.logout();
    return next('/login');
  }

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login');
  }

  if (to.meta.requiresAdmin && !authStore.isAdmin) {
    return next('/'); // redirect non-admins to home
  }

  next();
});

// Dynamic Title
router.afterEach((to) => {
  document.title = to.meta.title ? `EDPS | ${to.meta.title}` : 'EDPS';
});

export default router;
