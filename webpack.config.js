const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const path = require("path")
const StyleLintPlugin = require('stylelint-webpack-plugin')
const { ProvidePlugin } = require("webpack")

module.exports = {
  cache: false,
  entry: "./misago/admin/src/index.js",
  output: {
    path: path.resolve(__dirname, "misago", "static", "misago", "admin"),
    filename: "index.js"
  },
  resolve: {
    alias: {
      moment$: path.resolve(__dirname, "node_modules", "moment", "min", "moment.min.js")
    }
  },
  module: {
    rules: [
      {
        enforce: "pre",
        test: /\.js$/,
        exclude: /(node_modules)/,
        loader: 'eslint-loader'
      },
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        loader: 'babel-loader'
      },
      {
        test: /\.(sa|sc|c)ss$/,
        use: [
          MiniCssExtractPlugin.loader,
          "css-loader",
          {
            loader: "postcss-loader",
            options: {
              plugins: function() {
                return [
                  require("autoprefixer")
                ]
              }
            }
          },
          "sass-loader"
        ]
      }
    ]
  },
  plugins: [
    new StyleLintPlugin({
      configFile: "./node_modules/stylelint-config-twbs-bootstrap/scss/index.js"
    }),
    new MiniCssExtractPlugin({
      filename: "index.css"
    })
  ]
}