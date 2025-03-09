import { defineConfig, loadEnv } from 'vite';
import react from '@vitejs/plugin-react';
import getConfig from './src/config/env/config.main.js';

export default defineConfig(({ mode }) => {
    // Load environment variables (optional, if needed)
    const env = loadEnv(mode, process.cwd());

    // Get dynamic configuration based on the mode
    const config = getConfig(mode);


    return {
        plugins: [react()],
        server: {
            proxy: {
                '/api': {
                    target: config.serverConfig.apiBaseUrl,
                    changeOrigin: true,
                    secure: false,
                },
            },
        },
        define: {
            'process.env': env, // Allows access to env variables in client code
        },
    };
});
