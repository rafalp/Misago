const path = require("path")

const MiniCssExtractPlugin = require("mini-css-extract-plugin")

module.exports = (env, argv) => {
  const isProduction = argv.mode === "production";

  return {
    mode: isProduction ? "production" : "development",
    devtool: "source-map",
    cache: false,
    entry: "./misago/admin/src/index.js",
    output: {
      path: path.resolve(__dirname, "misago", "static", "misago", "admin"),
      filename: "index.js"
    },
    module: {
      rules: [
        {
          test: /\.jsx?$/,
          exclude: /node_modules/,
          use: {
            loader: "babel-loader",
            options: {
              cacheDirectory: true,
              cacheCompression: false,
              envName: isProduction ? "production" : "development",
            },
          },
        },
        {
          test: /\.mjs/,
          resolve: {
              fullySpecified: false
          }
        },
        {
          test: /\.(sa|sc|c)ss$/,
          use: [
            MiniCssExtractPlugin.loader,
            "css-loader",
            {
              loader: "postcss-loader",
              options: {
                postcssOptions: {
                  plugins: function() {
                    return [
                      require("autoprefixer")
                    ]
                  }
                }
              }
            },
            "sass-loader"
          ]
        }
      ]
    },
    plugins: [
      new MiniCssExtractPlugin({
        filename: "index.css"
      }),
    ]
  }
}