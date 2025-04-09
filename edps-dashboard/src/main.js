import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css' // Tailwind CSS
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)
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
app.mount('#app')
