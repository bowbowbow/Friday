const path = require('path');
const webpack = require('webpack');
const autoprefixer = require('autoprefixer');

const customPath = path.join(__dirname, './customPublicPath');

module.exports = {
  entry: {
    app: [customPath, path.join(__dirname, '../chrome/extension/app')],
    background: [customPath, path.join(__dirname, '../chrome/extension/background')],
    inject: [customPath, path.join(__dirname, '../chrome/extension/inject')]
  },
  output: {
    path: path.join(__dirname, '../build/js'),
    filename: '[name].bundle.js',
    chunkFilename: '[id].chunk.js',
  },
  plugins: [
    new webpack.optimize.OccurrenceOrderPlugin(),
    new webpack.IgnorePlugin(/[^/]+\/[\S]+.dev$/),
    new webpack.optimize.UglifyJsPlugin({
      comments: false,
      compressor: {
        warnings: false,
      },
    }),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production'),
      },
    }),
  ],
  resolve: {
    extensions: ['*', '.js'],
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        loader: 'babel-loader',
        exclude: /node_modules/,
        query: {
          presets: ['react-optimize'],
          plugins: [
            ['import', { libraryName: 'antd', style: 'css' }],
          ],
        },
      }, {
        test: /\.less$/,
        use: [
          'style-loader', // creates style nodes from JS strings
          'css-loader?modules&sourceMap&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]', // translates CSS into CommonJS
          {
            loader: 'less-loader', // compiles Less to CSS
          },
        ],
      },
      {
        test: /\.css/,
        use: [
          'style-loader', // creates style nodes from JS strings
          'css-loader',
          // {
          //   loader: 'postcss-loader',
          //   options: {
          //     plugins: () => [autoprefixer],
          //   },
          // },
        ],
      }],
  },
};
