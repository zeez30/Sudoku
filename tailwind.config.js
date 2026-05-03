/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg:            '#0a070e',
        surface:       '#140e1b',
        border:        '#271b36',
        accent:        '#0afbff',
        violet:        '#c346c3',
        textprimary:   '#f0f4f8',
        textsecondary: '#b2f5fa',
      },
      fontFamily: {
        display: ['Syne', 'sans-serif'],
        body:    ['DM Sans', 'sans-serif'],
        mono:    ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
