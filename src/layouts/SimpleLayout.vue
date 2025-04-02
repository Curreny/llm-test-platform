<!-- 
	This is a simple layout, used for cover page (with navigation bar and footer).
 -->

<template>
	<div>
		<!-- Simple Layout -->
		<a-layout class="layout-default" id="layout-default" :class="[layoutClass]">
	
			<!-- 左侧浮动导航目录 -->
			<div class="side-nav-menu">
				<div class="side-nav-header">
					<img src="/images/logo-ct-black.png" alt="Logo">
					<span>飞舞不会coding</span>
				</div>

				<div class="side-nav-items">
					<router-link to="/question-generate" class="side-nav-item">
						<div class="side-nav-icon icon-primary">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>观测题库生成</span>
					</router-link>
					
					<router-link to="/question-bank" class="side-nav-item">
						<div class="side-nav-icon icon-purple">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M8 3V5M16 3V5M7 21H17C19.2091 21 21 19.2091 21 17V9C21 6.79086 19.2091 5 17 5H7C4.79086 5 3 6.79086 3 9V17C3 19.2091 4.79086 21 7 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>观测题库查看</span>
					</router-link>
					
					<router-link to="/data-audit" class="side-nav-item">
						<div class="side-nav-icon icon-success">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>数据审核模块</span>
					</router-link>
					
					<router-link to="/results" class="side-nav-item">
						<div class="side-nav-icon icon-warning">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M21 21H4C3.44772 21 3 20.5523 3 20V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M7 14L11 10L15 14L21 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>结果生成模块</span>
					</router-link>
					
					<router-link to="/reports" class="side-nav-item">
						<div class="side-nav-icon icon-info">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>自动化报告生成</span>
					</router-link>
					
					<router-link to="/api" class="side-nav-item">
						<div class="side-nav-icon icon-danger">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M10 20L14 4M18 8L22 12L18 16M6 16L2 12L6 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>观测调用形式</span>
					</router-link>
				</div>
			</div>

			<!-- Page Content -->
			<a-layout-content class="content-with-sidebar">
				<router-view />
			</a-layout-content>
			<!-- / Page Content -->

			<!-- 页脚部分 -->
			<div class="footer-section">
				<div class="footer-content">
					<div class="footer-column-header">
						<h3 class="footer-title">飞舞不会coding团队</h3>
						<p class="footer-desc">致力于提供全面的大模型性能与安全观测解决方案，通过多维度评估、实时监控和智能分析，帮助用户全方位了解和优化大模型的表现与合规性。</p>
					</div>
					<div class="footer-column">
						<h3 class="footer-title">关于我们</h3>
						<ul class="footer-links">
							<li><a href="#">平台介绍</a></li>
							<li><a href="#">技术白皮书</a></li>
							<li><a href="#">研究成果</a></li>
							<li><a href="#">技术支持</a></li>
						</ul>
					</div>
					<div class="footer-column">
						<h3 class="footer-title">服务范围</h3>
						<ul class="footer-links">
							<li><a href="#">能力评估</a></li>
							<li><a href="#">安全审核</a></li>
							<li><a href="#">性能监控</a></li>
							<li><a href="#">合规认证</a></li>
						</ul>
					</div>
					<div class="footer-column">
						<h3 class="footer-title">联系方式</h3>
						<p class="footer-address">翻斗大街翻斗花园2号楼1001室</br>中国宇宙省星际市银河区太阳街八里香胡同11号</p>
					</div>
				</div>
				<div class="footer-bottom">
					<p class="copyright">版权所有 © 2024 飞舞不会coding</p>
					<div class="contact">
						<span>全天候服务热线: 400-800-8888</span>
						<span class="contact-icon">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="currentColor" stroke-width="1.5" />
								<path d="M8 13V7L16 17V11" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
							</svg>
						</span>
						<span class="contact-icon">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M17 2H7C4.23858 2 2 4.23858 2 7V17C2 19.7614 4.23858 22 7 22H17C19.7614 22 22 19.7614 22 17V7C22 4.23858 19.7614 2 17 2Z" stroke="currentColor" stroke-width="1.5" />
								<path d="M16 11.3698C16.1234 12.2021 15.9812 13.052 15.5937 13.7989C15.2062 14.5458 14.5931 15.1512 13.8416 15.5295C13.0901 15.9077 12.2384 16.0394 11.4077 15.9057C10.5771 15.7721 9.80971 15.3799 9.21479 14.785C8.61987 14.1901 8.22768 13.4227 8.09402 12.592C7.96035 11.7614 8.09202 10.9097 8.47028 10.1582C8.84854 9.40667 9.45394 8.79355 10.2009 8.40605C10.9478 8.01856 11.7977 7.8764 12.63 7.99981C13.4789 8.1257 14.2648 8.52128 14.8716 9.12812C15.4785 9.73496 15.8741 10.5209 16 11.3698Z" stroke="currentColor" stroke-width="1.5" />
								<path d="M17.5 6.5H17.51" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
							</svg>
						</span>
						<span class="contact-icon">
							<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M15 3.99988H9C7.34315 3.99988 6 5.34303 6 6.99988V18.9999C6 20.6567 7.34315 21.9999 9 21.9999H15C16.6569 21.9999 18 20.6567 18 18.9999V6.99988C18 5.34303 16.6569 3.99988 15 3.99988Z" stroke="currentColor" stroke-width="1.5" />
								<path d="M12 18.0001H12.01" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" />
							</svg>
						</span>
					</div>
				</div>
			</div>
		</a-layout>
		<!-- / Simple Layout -->
	</div>
</template>

<script>
	export default ({
		components: {
		},
		data() {
			return {
			}
		},
		computed: {
			// Sets layout's element's class based on route's meta data.
			layoutClass() {
				return this.$route.meta.layoutClass;
			}
		}
	})
</script>

<style lang="scss">


/* 左侧浮动导航目录样式 */
.side-nav-menu {
	position: fixed;
	left: 0;
	top: 0;
	height: 100vh;
	background-color: #fff;
	box-shadow: 0 2px 22px 0 rgba(0, 0, 0, 0.1), 0 4px 20px 0 rgba(0, 0, 0, 0.08);
	padding: 1rem 0;
	color: #000;
	z-index: 98;
	width: 250px;
	display: flex;
	flex-direction: column;
}

.side-nav-header {
	display: flex;
	align-items: center;
	padding: 0.75rem 1.5rem;
	margin-bottom: 1rem;
	border-bottom: 1px solid rgba(0, 0, 0, 0.06);
}

.side-nav-header img {
	width: 35px;
	height: 35px;
	margin-right: 10px;
	border-radius: 6px;
}

.side-nav-header span {
	font-size: 1.1rem;
	font-weight: 600;
	white-space: nowrap;
}

.side-nav-items {
	display: flex;
	flex-direction: column;
	gap: 0.3rem;
	padding: 0 0.75rem;
	overflow-y: auto;
	flex: 1;
}

.side-nav-item {
	display: flex;
	align-items: center;
	padding: 0.75rem 0.75rem;
	border-radius: 8px;
	color: #111827;
	text-decoration: none;
	transition: all 0.3s ease;
	font-size: 0.9rem;
	font-weight: 500;
	
	&:hover {
		background-color: rgba(0, 0, 0, 0.04);
		color: #1890ff;
		
		.side-nav-icon {
			color: #1890ff;
		}
	}
	
	&.router-link-active {
		background: linear-gradient(90deg, #1890ff 0%, #096dd9 100%);
		color: #fff;
		box-shadow: 0 2px 6px rgba(24, 144, 255, 0.3);
		
		.side-nav-icon {
			color: #fff;
		}
	}
	
	span {
		white-space: nowrap;
	}
}

.side-nav-icon {
	display: inline-flex;
	align-items: center;
	justify-content: center;
	width: 24px;
	height: 24px;
	margin-right: 0.75rem;
	transition: all 0.3s ease;
	color: #111827;
	
	&.icon-primary {
		color: #1890ff;
	}
	
	&.icon-purple {
		color: #722ed1;
	}
	
	&.icon-success {
		color: #52c41a;
	}
	
	&.icon-warning {
		color: #faad14;
	}
	
	&.icon-info {
		color: #13c2c2;
	}
	
	&.icon-danger {
		color: #f5222d;
	}
}

/* 主体内容区域留出侧边栏空间 */
.content-with-sidebar {
	margin-left: 250px;
	padding-top: 1px; /* 防止margin合并问题 */
}

/* 页脚样式 */
.footer-section {
	background-color: #f5f5f5;
	padding: 3rem 2rem 1rem 2rem;
	margin-left: 250px;
}

.footer-content {
	display: flex;
	flex-wrap: wrap;
	gap: 2rem;
	margin-bottom: 2rem;
}

.footer-column-header {
	flex: 2;
	min-width: 300px;
}

.footer-column {
	flex: 1;
	min-width: 200px;
}

.footer-title {
	font-size: 1.2rem;
	font-weight: 600;
	margin-bottom: 1rem;
	color: #303133;
}

.footer-desc {
	color: #606266;
	line-height: 1.6;
}

.footer-links {
	list-style: none;
	padding: 0;
	margin: 0;
}

.footer-links li {
	margin-bottom: 0.8rem;
}

.footer-links a {
	text-decoration: none;
	color: #606266;
	transition: color 0.3s ease;
}

.footer-links a:hover {
	color: #1890ff;
}

.footer-address {
	color: #606266;
	line-height: 1.6;
}

.footer-bottom {
	display: flex;
	justify-content: space-between;
	align-items: center;
	padding-top: 1.5rem;
	border-top: 1px solid #e8e8e8;
}

.copyright {
	color: #909399;
	margin: 0;
}

.contact {
	display: flex;
	align-items: center;
	gap: 1rem;
	color: #909399;
}

.contact-icon {
	display: flex;
	align-items: center;
	justify-content: center;
	width: 32px;
	height: 32px;
	border-radius: 50%;
	background-color: #f0f0f0;
	transition: all 0.3s ease;
	cursor: pointer;
}

.contact-icon:hover {
	background-color: #e0e0e0;
}

@media (max-width: 768px) {
	.hero-navbar {
		padding: 1rem;
	}
	
	.navbar-links {
		display: none;
	}
	
	.footer-bottom {
		flex-direction: column;
		gap: 1rem;
	}
	
	.footer-content {
		flex-direction: column;
		gap: 2rem;
	}
	
	/* 移动端响应式处理 */
	.side-nav-menu {
		width: 60px;
	}
	
	.side-nav-header span, 
	.side-nav-item span {
		display: none;
	}
	
	.side-nav-item {
		justify-content: center;
	}
	
	.side-nav-icon {
		margin-right: 0;
	}
	
	.content-with-sidebar,
	.footer-section {
		margin-left: 60px;
	}
}
</style> 