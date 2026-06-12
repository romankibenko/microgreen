import { fileURLToPath, URL } from 'node:url'

import vue from '@vitejs/plugin-vue'
import { defineConfig } from 'vite'
import vuetify from 'vite-plugin-vuetify'

// В проде админка раздаётся с подпути /admin/ (за nginx), в dev — с корня.
export default defineConfig(({ mode }) => ({
  base: mode === 'production' ? '/admin/' : '/',
  plugins: [vue(), vuetify({ autoImport: true })],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5174,
  },
}))
