import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  preview: {
    allowedHosts: [
      'student-roster-production.up.railway.app',
      'friendly-youthfulness-production.up.railway.app',
    ],
  },
})