import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/chat': {
        target: 'http://192.168.1.4:7000',
        changeOrigin: true,
      },
      '/protocols': {
        target: 'http://192.168.1.4:7000',
        changeOrigin: true,
      }
    }
  }
})
