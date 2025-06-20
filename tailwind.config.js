/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: "jit",
  content: ["./templates/**/*.{html,js}", "./static/**/*.{html,js}"],
  darkMode: "class", // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        poppins: ["Poppins", "sans-serif"],
      },
      colors: {
        skin: {
          body: "var(--color-body)",
          sidebar: "var(--color-sidebar)",
          primary: "var(--color-primary)",
          primaryMuted: "var(--color-primary-muted)",
          primaryLight: "var(--color-primary-light)",
          toggle: "var(--color-toggle)",
          text: "var(--color-text)",
          muted: "var(--color-text-muted)",
          svg: "var(--color-svg)",
          shadow: "var(--color-shadow)",
        },
      },
    },
  },
  plugins: [],
};
