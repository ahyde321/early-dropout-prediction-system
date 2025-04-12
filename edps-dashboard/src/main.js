import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css'
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'
import { createPinia } from 'pinia'
import { useAuthStore } from '@/stores/authStore'


const app = createApp(App)
const pinia = createPinia()

app.use(pinia)
app.use(router)

app.use(Toast, {
    timeout: 4000,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
    draggablePercent: 0.6,
    showCloseButtonOnHover: false,
    hideProgressBar: false,
    position: 'top-right',
    transition: 'Vue-Toastification__fade'
  })

const authStore = useAuthStore()
authStore.tryAutoLogin().then(() => {
  app.mount('#app')
})
