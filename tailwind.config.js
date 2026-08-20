/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{ts,tsx}'],
  theme: {
    extend: {
      colors: {
        bg:        '#101913',
        surface:   '#140e1b',
        hairline:  '#271b36',
        line:      '#344b07',
        primary:   '#edf7b5',
        accent:    '#b05f1c',
        danger:    '#aa2422',
        secondary: '#b2f5fa',
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
