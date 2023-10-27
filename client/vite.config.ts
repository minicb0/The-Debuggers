import { defineConfig } from "vite";
import { port } from "./config";
import react from "@vitejs/plugin-react";

// https://vitejs.dev/config/
export default defineConfig({
	plugins: [react()],
	server: {
		port: port
	}
});
