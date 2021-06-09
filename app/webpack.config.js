const path = require('path')
const BudnleTracker = require('webpack-bundle-tracker')

module.exports = {
  mode: 'development',
  context: __dirname,
  entry: './assets/js/main.js',
  output: {
    path: path.resolve(__dirname, './dist'),
    filename: 'js/[name]-[hash].js',
  },
  plugins: [
    new BudnleTracker({
      filename: './webpack-stats.json'
    }),
  ],
  module: {},
}
