const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    client: {
      overlay: {
        errors: true,
        warnings: false,
        runtimeErrors: true,
      },
    },
  },
  configureWebpack:{
    mode: 'development',
    devtool: false,
    optimization: {
      splitChunks: {
        chunks: 'all',
        minSize: 15000,
        maxSize: 250000,
        maxAsyncRequests: 30,
        maxInitialRequests: 30,
        enforceSizeThreshold: 50000,
        
      },
    },

  }
})
