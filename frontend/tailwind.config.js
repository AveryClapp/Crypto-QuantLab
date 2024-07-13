/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./src/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        euclid: ["Euclid Circular A", "Poppins", "sans-serif"],
      },
    },
  },
  variants: {
    extend: {
      opacity: ["swiper-slide-active"],
      translate: ["swiper-slide-active"],
    },
  },
  plugins: [],
};
