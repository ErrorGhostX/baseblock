module.exports = {
  content: ["./templates/**/*.html"],
  theme: {
    extend: {
      fontFamily: {
        minecraft: ['MinecraftFont', 'sans-serif'],
      },
      colors: {
        primary: '#9d49ff',
        secondary: '#2e2e2e',
        accent: '#4909b3',
      },
      backgroundImage: {
        'minecraft-fon': "url('/static/minecraft/images/fon.png')",
      },
    },
  },
  plugins: [],
};
