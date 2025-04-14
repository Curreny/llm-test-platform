module.exports = {
	runtimeCompiler: true,

	chainWebpack: config => {
		config
			.plugin('html')
			.tap(args => {
				args[0].title = 'llm-test-platform'
				return args
			})
	},

	devServer: {
		port: 8081,
		proxy: {
			'/api': {
				target: 'http://localhost:5000',
				changeOrigin: true
			}
		}
	},

	// 设置生产环境构建输出目录为dist
	outputDir: 'dist',

	// 确保API路径正确
	publicPath: '/'
}
