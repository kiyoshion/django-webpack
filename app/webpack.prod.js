const { merge } = require('webpack-merge')
const common = require('./webpack.common')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = merge(common, {
  mode: 'production',
  output: {
    filename: 'js/[name]-[hash].js',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          "style-loader",
          { loader: "css-loader", options: { importLoaders: 1 } },
          "postcss-loader",
        ],
      },
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: './css/[name]-[hash].css',
    }),
  ],
})
