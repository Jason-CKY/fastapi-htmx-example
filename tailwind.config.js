/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  darkMode: 'class',
  plugins: [require("daisyui")],
  daisyui: {
    themes: ["garden", "dracula"],
  },
}

