import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
<<<<<<< HEAD
import './assets/main.css'
import Vue3Toastify from 'vue3-toastify'

const app = createApp(App)
app.use(createPinia())
app.use(Vue3Toastify, {
  autoClose: 3000,
})
=======

import './assets/main.css'

const app = createApp(App)
app.use(createPinia())
>>>>>>> ced46b1f93a5b50e33740fd558e6068556dac573
app.use(router)
app.mount('#app')
