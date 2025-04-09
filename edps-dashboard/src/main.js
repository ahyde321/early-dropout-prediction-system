import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css' // Tailwind CSS
import router from './router'
import Toast from 'vue-toastification'
import 'vue-toastification/dist/index.css'

const app = createApp(App)
app.use(router)
app.use(Toast)
app.mount('#app')
