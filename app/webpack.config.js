const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const BudnleTracker = require('webpack-bundle-tracker')
const { CleanWebpackPlugin } = require('clean-webpack-plugin')

module.exports = (env, args) => ({
  context: __dirname,
  entry: './assets/js/main',
  output: {
    path: path.resolve(__dirname, './dist'),
    filename: 'js/[name]-[hash].js',
  },
  plugins: [
    new BudnleTracker({
      filename: './webpack-stats.json'
    }),
    new MiniCssExtractPlugin({
      filename: './css/[name]-[hash].css',
    }),
    new CleanWebpackPlugin(),
  ],
  module: {
    rules: [
      {
        test: /\.(css|sass|scss)/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          {
            loader: 'css-loader',
            options: {
              sourceMap: false,
            },
          },
          {
            loader: 'sass-loader',
          },
        ],
      },
      {
        test: /\.(png|jpg|jpeg)/,
        use: [
          {
            loader: 'file-loader',
            options: {
              esModule: false,
              name: 'img/[name]-[hash].[ext]',
              publicPath: '/',
            },
          },
          {
            loader: 'image-webpack-loader',
            options: {
              moxjpeg: {
                progressive: true,
                quality: 80,
              },
            },
          },
        ],
      },
      {
        test: /\.svg/,
        use: [
          {
            loader: 'file-loader',
            options: {
              esModule: false,
              name: 'img/[name].[ext]',
              publicPath: '/',
            },
          },
          {
            loader: 'svgo-loader',
          },
        ],
      },
    ],
  },
})
