const path = require('path')
const BudnleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')
const VueLoaderPlugin = require('vue-loader/lib/plugin')

module.exports = {
  context: __dirname,
  entry: './assets/js/main',
  output: {
    path: path.resolve(__dirname, './dist'),
  },
  plugins: [
    new BudnleTracker({
      filename: './webpack-stats.json'
    }),
    new CleanWebpackPlugin(),
    new VueLoaderPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: 'vue-loader',
      },
    ],
  },
  resolve: {
    extensions: ['.js', '.vue'],
    alias: {
      'vue$': path.resolve('./node_modules/vue/dist/vue.js')
    }
  }
}
