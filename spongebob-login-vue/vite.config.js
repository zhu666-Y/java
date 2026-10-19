import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 开发环境：npm run dev（5173 端口）
  server: {
    port: 5173,
    strictPort: true, // 端口被占直接报错，避免悄悄换端口让人困惑
    open: true,
    // 开发环境代理：把 /api 请求转发到 Spring Boot 后端（8081 端口）
    proxy: {
      '/api': {
        target: 'http://localhost:8081',
        changeOrigin: true
      }
    }
  },
  // 预览构建产物：npm run preview（4173 端口）
  // 没有这段的话，preview 模式下 /api 请求会 404（preview 不复用 server.proxy）
  preview: {
    port: 4173,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://localhost:8081',
        changeOrigin: true
      }
    }
  }
})
