import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/static/vue/',
  build: {
    outDir: '../static/vue',
    emptyOutDir: true,
    assetsDir: 'assets',
    rollupOptions: {
      output: {
        entryFileNames: 'assets/index.js',
        chunkFileNames: 'assets/[name].js',
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.css')) {
            return 'assets/index.css'
          }
          return 'assets/[name][extname]'
        }
      }
    }
  },
  server: {
    port: 5173,
    strictPort: true,
    proxy: {
      '/boardgames': 'http://127.0.0.1:8000',
      '/accounts': 'http://127.0.0.1:8000',
      '/community': 'http://127.0.0.1:8000',
      '/static': 'http://127.0.0.1:8000',
      '/media': 'http://127.0.0.1:8000'
    }
  }
})
