import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#0f172a",
        card: "#1e293b",
        text: "#e2e8f0",
        accent: "#3b82f6",
        success: "#10b981",
        error: "#ef4444",
      },
    },
  },
  plugins: [],
};
export default config;
