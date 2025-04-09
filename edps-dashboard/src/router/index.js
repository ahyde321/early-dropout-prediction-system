import { createRouter, createWebHistory } from 'vue-router'
import StudentListView from '../views/StudentListView.vue';

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/HomeView.vue')
  },
  {
    path: '/students/list',
    name: 'StudentList',
    component: StudentListView
  }
  
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
