const MiniCssExtractPlugin = require("mini-css-extract-plugin")
const StyleLintPlugin = require('stylelint-webpack-plugin')
const path = require("path")


module.exports = {
  cache: false,
  entry: "./misago/admin/src/index.js",
  output: {
    path: path.resolve(__dirname, "misago", "static", "misago", "admin-new"),
    filename: "index.js"
  },
  module: {
    rules: [{
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
    }]
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