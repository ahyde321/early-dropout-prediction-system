import { createRouter, createWebHashHistory } from 'vue-router'
import DashboardLayout from '@/layouts/DashboardLayout.vue'
import DashboardPage from '@/views/DashboardPage.vue'
import StudentListPage from '@/views/StudentListPage.vue'
import UploadPage from '@/views/UploadPage.vue'
import StudentProfilePage from '@/views/StudentProfilePage.vue'

const routes = [
  {
    path: '/',
    component: DashboardLayout,
    children: [
      { path: '', name: 'Dashboard', component: DashboardPage },
      { path: 'students', name: 'Students', component: StudentListPage },
      { path: 'students/:id', name: 'StudentProfile', component: StudentProfilePage },
      { path: 'upload', name: 'Upload', component: UploadPage },
    ],
  },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes,
})

export default router
