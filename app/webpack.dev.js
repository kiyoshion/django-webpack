const { merge } = require('webpack-merge')
const common = require('./webpack.common')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')

module.exports = merge(common, {
  mode: 'development',
  output: {
    filename: 'js/[name].js',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          {
            loader: MiniCssExtractPlugin.loader,
          },
          { loader: "css-loader", options: { importLoaders: 1 } },
          "postcss-loader",
        ],
      },
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: './css/[name].css',
    }),
  ],
})
