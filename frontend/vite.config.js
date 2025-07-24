import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

// https://vite.dev/config/
export default defineConfig({
<<<<<<< HEAD
<<<<<<< HEAD
  plugins: [vue(), vueDevTools()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    proxy: {
      '/api': 'http://localhost:5000',
=======
=======
>>>>>>> 2d1d0c920faaca06cb384ea213bfb7256909cb6e
  plugins: [
    vue(),
    vueDevTools(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
<<<<<<< HEAD
>>>>>>> ced46b1f93a5b50e33740fd558e6068556dac573
=======
>>>>>>> 2d1d0c920faaca06cb384ea213bfb7256909cb6e
    },
  },
})
