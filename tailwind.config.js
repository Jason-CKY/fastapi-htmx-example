/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/app/templates/**/*.{html,js}"],
  theme: {
    extend: {},
  },
  darkMode: 'class',
  plugins: [require("@tailwindcss/typography"), require("daisyui")],
  daisyui: {
    themes: ["garden", "dracula"],
  },
}

