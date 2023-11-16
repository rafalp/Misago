import path from "path"
import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

// https://vitejs.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      "~bootstrap": path.resolve(__dirname, "node_modules/bootstrap"),
    },
  },
  build: {
    rollupOptions: {
      input: "/src/index.js",
      output: {
        assetFileNames: "[name][extname]",
        dir: "../misago/static/misago/admin",
        entryFileNames: "[name].js",
        format: "iife",
      },
    },
    sourcemap: true,
  },
  plugins: [react()],
})
