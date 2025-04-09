import { createRouter, createWebHashHistory } from 'vue-router'

// Layout
import DashboardLayout from '@/layouts/DashboardLayout.vue'

// Views
import HomeView from '@/views/HomeView.vue'
import StudentListPage from '@/views/StudentListPage.vue'
import UploadPage from '@/views/UploadPage.vue'
import StudentProfilePage from '@/views/StudentProfilePage.vue'
import NotFound from '@/views/NotFound.vue' // Create this for a custom 404

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    children: [
      {
        path: '',
        name: 'Home',
        component: HomeView,
        meta: { title: 'Dashboard Home' },
      },
      {
        path: 'students',
        name: 'Students',
        component: StudentListPage,
        meta: { title: 'Student List' },
      },
      {
        path: 'students/:id',
        name: 'StudentProfile',
        component: StudentProfilePage,
        meta: { title: 'Student Profile' },
      },
      {
        path: 'upload',
        name: 'UploadCSV',
        component: UploadPage,
        meta: { title: 'Upload CSV' },
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

// Optionally set page title based on route meta
router.afterEach((to) => {
  if (to.meta.title) {
    document.title = `EDPS | ${to.meta.title}`
  } else {
    document.title = 'EDPS'
  }
})

export default router
