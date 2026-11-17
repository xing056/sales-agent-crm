import { defineConfig, mergeConfig } from 'vite'
import base from './vite.config.js'

/**
 * 预览用配置：`npm run preview` 走的是构建产物，
 * 需要自己声明 proxy（vite.config.js 里只配了 dev server 的 proxy）。
 *
 * 用法：
 *   vite build --outDir dist-theme --emptyOutDir false
 *   vite preview --config vite.preview.config.mjs --outDir dist-theme
 */
export default mergeConfig(
  base,
  defineConfig({
    preview: {
      host: '127.0.0.1',
      port: 5180,
      strictPort: true,
      proxy: {
        '/api': { target: 'http://127.0.0.1:8000', changeOrigin: true },
        '/media': { target: 'http://127.0.0.1:8000', changeOrigin: true },
      },
    },
  })
)
