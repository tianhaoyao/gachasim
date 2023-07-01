const path = require('path');
const { defineConfig } = require('@vue/cli-service');

module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    resolve: {
      alias: {
        '@GameModule': path.resolve(__dirname, 'src/GameModule'),
        '@RarityModule': path.resolve(__dirname, 'src/RarityModule'),
        '@ItemModule': path.resolve(__dirname, 'src/ItemModule'),
        '@': path.resolve(__dirname, 'src'),
      },
      extensions: ['.js', '.ts', '.vue', '.json'],
    },
  },
});
