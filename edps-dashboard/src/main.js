// main.js
import { createApp } from 'vue'
import App from './App.vue'
import router from './router'

// 1) Import Vuetify styles
import 'vuetify/styles'

// 2) Import createVuetify
import { createVuetify } from 'vuetify'
// If you need all components globally, import them:
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'

// 3) Create Vuetify instance
const vuetify = createVuetify({
  components,
  directives,
  // You can customize icons, themes, etc. here
})

// 4) Create and mount the Vue app
const app = createApp(App)
app.use(router)    // Your router
app.use(vuetify)   // Register Vuetify plugin
app.mount('#app')
