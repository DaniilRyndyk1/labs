var packageJSON = require('./package.json');
var path = require('path');
var webpack = require('webpack');

module.exports = {
    entry: './index.js',
    output: {
        path: path.join(__dirname, 'generated'),
        filename: 'bundle.js'},
    resolve: {extensions: ['.js', '.jsx']},
    module: {
        rules: [
            {
                test: /\.jsx$/,
                loader: 'babel-loader',
                exclude: /node_modules/
	       }
        ]
    },
    devServer: {
        static: path.resolve(__dirname, 'dist'),
        port: 9000
    },
}