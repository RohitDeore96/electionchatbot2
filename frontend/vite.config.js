import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [tailwindcss(), react()],
  server: {
    host: '0.0.0.0', // Binds to all network interfaces for local and Docker access
    port: 5173,
    strictPort: true, // Ensures failure if 5173 is taken, rather than silently switching ports
    watch: {
      usePolling: true, // Important for Windows/WSL/Docker volume mapping
    }
  },
  build: {
    target: 'esnext',
    minify: 'esbuild', // Faster and efficient minification
    chunkSizeWarningLimit: 500, // Enforce strict code quality metrics
    rollupOptions: {
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          firebase: ['firebase/app', 'firebase/auth', 'firebase/firestore']
        }
      }
    }
  }
});
