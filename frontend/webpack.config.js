"use strict";

const path = require('path');
const glob = require('glob');

const { ProvidePlugin } = require("webpack");
const CopyPlugin = require("copy-webpack-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const ESLintPlugin = require("eslint-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");

const misago = path.resolve(__dirname, "../misago/static/misago/");
const modules = path.resolve(__dirname, "node_modules");

const getEntries = () => {
  const entry = ["./src/index.js"];
  glob.sync("./src/initializers/**/*.js").forEach((path) => entry.push(path));
  return entry;
};

module.exports = (env, argv) => {
  const isProduction = argv.mode === "production";

  return {
    mode: isProduction ? "production" : "development",
    devtool: "source-map",
    entry: {
      misago: getEntries(),
    },
    output: {
      path: path.resolve(misago, "js"),
      filename: "[name].js",
    },
    optimization: {
      minimize: isProduction,
      minimizer: [
        "...",
        new CssMinimizerPlugin(),
      ],
      splitChunks: {
        cacheGroups: {
          vendor: {
            test: /[\\/]node_modules[\\/]/,
            name: "vendor",
            chunks: "all",
          },
          hljs: {
            test: /[\\/]highlight[\\/]/,
            name: "hljs",
            chunks: "all",
          },
        },
      },
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
          test: /\.less$/i,
          use: [
            "style-loader",
            "css-loader",
            "less-loader",
          ],
          use: [MiniCssExtractPlugin.loader, "css-loader", "less-loader"],
        },
        {
          test: /\.(woff|ttf|eot|woff2)/,
          type: "asset/resource",
          generator: {
            filename: "../fonts/[name][ext]"
          }
        },
      ],
    },
    resolve: {
      alias: {
        misago: path.resolve(__dirname, "src"),
        "at-js": path.resolve(modules, "at.js/dist/js/jquery.atwho.js"),
        "jquery-caret": path.resolve(modules, "jquery.caret/dist/jquery.caret.js"),
        highlight: path.resolve(__dirname, "highlight/highlight.js"),
      },
      extensions: [".js", ".jsx"],
    },
    plugins: [
      new ESLintPlugin(
        {
          extensions: ["js", "jsx"],
          files: "./src/"
        },
      ),
      new CopyPlugin(
        {
          patterns: [
            {
              from: "./static",
              to: misago,
            },
            {
              from: "./node_modules/zxcvbn/dist",
              to: path.resolve(misago, "js"),
            },
          ],
        }
      ),
      new MiniCssExtractPlugin(
        {
          filename: "../css/misago.css",
        }
      ),
      new ProvidePlugin({
        $: "jquery",
        "window.$": "jquery",
        jQuery: "jquery",
        "window.jQuery": "jquery",
        moment: "moment",
        "window.moment": "moment",
      }),
    ],
    watchOptions: {
      ignored: "**/node_modules",
      poll: 2000, // Check for changes every two seconds
      stdin: true,
    },
  };
};