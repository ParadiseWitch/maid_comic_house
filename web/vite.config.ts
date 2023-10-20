import * as path from 'path'

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import UnoCSS from 'unocss/vite'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react(), UnoCSS()],
  resolve: {
    alias: {
      '/@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    port: 3000,
    open: false, // 自动打开
    base: './ ', // 生产环境路径
    proxy: {
      '/api': {
        // https://github.com/vitejs/vite/discussions/7620
        // nodev17以后要用127.0.0.1
        target: 'http://127.0.0.1:8000/',
        // followRedirects需要为true，不然会有奇怪的重定向问题
        followRedirects: true,
        changeOrigin: true,
        rewrite: path => path.replace(/^\/api/, ''),
      },
    },
  },
})
