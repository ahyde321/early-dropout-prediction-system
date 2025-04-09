import { createApp } from 'vue'
import App from './App.vue'
import './assets/main.css' // 👈 your Tailwind file
import router from './router'

// 4) Create and mount the Vue app
const app = createApp(App).use(router).use(router)
app.use(router)    // Your router
app.mount('#app')
