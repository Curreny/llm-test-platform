<!-- 
	This is a simple layout, used for cover page (with navigation bar and footer).
 -->

<template>
	<div>
		<!-- Simple Layout -->
		<a-layout class="layout-default" id="layout-default" :class="[layoutClass]">
			
			<!-- 左侧固定导航 -->
			<a-layout-sider 
				class="side-nav"
				theme="light"
				width="250" 
				:collapsed-width="64"
				:trigger="null"
				collapsible
				:style="{height: '100%', position: 'fixed', left: 0}"
			>

				<div class="side-nav-items">
					<div class="side-nav-header">
						<img src="/images/logo-ct-black.png" alt="Logo">
						<span>飞舞不会coding</span>
					</div>
				
					<div class="nav-divider"></div>
					<router-link to="/question-generate" class="side-nav-item">
						<div class="side-nav-icon icon-primary">
							<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M9 16H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>观测题库生成</span>
					</router-link>
					
					<router-link to="/question-expansion" class="side-nav-item">
						<div class="side-nav-icon icon-purple">
							<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M8 3V5M16 3V5M7 21H17C19.2091 21 21 19.2091 21 17V9C21 6.79086 19.2091 5 17 5H7C4.79086 5 3 6.79086 3 9V17C3 19.2091 4.79086 21 7 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M8 9H16M8 13H14M8 17H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>观测题库拓展</span>
					</router-link>
					<router-link to="/data-audit#header-data-audit" class="side-nav-item">
						<div class="side-nav-icon icon-success">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>模型响应检测</span>
					</router-link>
					
					<router-link to="/data-audit#results-preview" class="side-nav-item">
						<div class="side-nav-icon icon-warning">
							<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="nav-svg">
								<path d="M21 21H4C3.44772 21 3 20.5523 3 20V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M7 14L11 10L15 14L21 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M21 8V14H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>检测结果预览</span>
					</router-link>
					
					<router-link to="/data-audit#report-generation" class="side-nav-item">
						<div class="side-nav-icon icon-info">
							<svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="nav-svg">
								<path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M7 12H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
								<path d="M7 17H13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>报告生成与预览</span>
					</router-link>
				
					
					<router-link to="/api-integration" class="side-nav-item">
						<div class="side-nav-icon icon-danger">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M10 20L14 4M18 8L22 12L18 16M6 16L2 12L6 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>观测调用形式</span>
					</router-link>
					
					<div class="nav-divider"></div>
					
					<router-link to="/" class="side-nav-item" exact>
						<div class="side-nav-icon icon-primary">
							<svg width="24" height="24" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
								<path d="M3 12L5 10M5 10L12 3L19 10M5 10V20C5 20.5523 5.44772 21 6 21H9M19 10L21 12M19 10V20C19 20.5523 18.5523 21 18 21H15M9 21C9.55228 21 10 20.5523 10 20V16C10 15.4477 10.4477 15 11 15H13C13.5523 15 14 15.4477 14 16V20C14 20.5523 14.4477 21 15 21M9 21H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
							</svg>
						</div>
						<span>返回主页</span>
					</router-link>
				</div>
			</a-layout-sider>

			<a-layout class="main-content">
				<!-- 页眉 -->
				<a-layout-header class="header">
					<a-row type="flex">
						<!-- 面包屑与页面标题 -->
						<a-col :span="24" :md="8">
							<a-breadcrumb>
								<a-breadcrumb-item><router-link to="/"> Pages</router-link></a-breadcrumb-item>
								<a-breadcrumb-item>{{ $route.name }}</a-breadcrumb-item>
							</a-breadcrumb>
							
							<div class="page-header-heading">
								<span class="page-header-heading-title">{{ $route.name }}</span>
							</div>
						</a-col>
						
						<!-- 控制区域 -->
						<a-col :span="24" :md="16" class="header-control">
							<!-- 搜索框 -->
							<a-input-search class="header-search" placeholder="输入搜索内容...">
								<svg slot="prefix" width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path fill-rule="evenodd" clip-rule="evenodd" d="M8 4C5.79086 4 4 5.79086 4 8C4 10.2091 5.79086 12 8 12C10.2091 12 12 10.2091 12 8C12 5.79086 10.2091 4 8 4ZM2 8C2 4.68629 4.68629 2 8 2C11.3137 2 14 4.68629 14 8C14 9.29583 13.5892 10.4957 12.8907 11.4765L17.7071 16.2929C18.0976 16.6834 18.0976 17.3166 17.7071 17.7071C17.3166 18.0976 16.6834 18.0976 16.2929 17.7071L11.4765 12.8907C10.4957 13.5892 9.29583 14 8 14C4.68629 14 2 11.3137 2 8Z" fill="#111827"/>
								</svg>
							</a-input-search>
							
							<!-- 通知按钮 -->
							<a-dropdown overlayClassName="header-notifications-dropdown">
								<a-badge count="2">
									<a class="ant-dropdown-link">
										<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
											<path d="M10 2C6.68632 2 4.00003 4.68629 4.00003 8V11.5858L3.29292 12.2929C3.00692 12.5789 2.92137 13.009 3.07615 13.3827C3.23093 13.7564 3.59557 14 4.00003 14H16C16.4045 14 16.7691 13.7564 16.9239 13.3827C17.0787 13.009 16.9931 12.5789 16.7071 12.2929L16 11.5858V8C16 4.68629 13.3137 2 10 2Z" fill="#111827"/>
											<path d="M10 18C8.34315 18 7 16.6569 7 15H13C13 16.6569 11.6569 18 10 18Z" fill="#111827"/>
										</svg>
									</a>
								</a-badge>
							</a-dropdown>
							
							<!-- 用户登录按钮 -->
							<router-link to="/sign-in" class="btn-sign-in">
								<svg width="20" height="20" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
									<path fill-rule="evenodd" clip-rule="evenodd" d="M18 10C18 14.4183 14.4183 18 10 18C5.58172 18 2 14.4183 2 10C2 5.58172 5.58172 2 10 2C14.4183 2 18 5.58172 18 10ZM12 7C12 8.10457 11.1046 9 10 9C8.89543 9 8 8.10457 8 7C8 5.89543 8.89543 5 10 5C11.1046 5 12 5.89543 12 7ZM9.99993 11C7.98239 11 6.24394 12.195 5.45374 13.9157C6.55403 15.192 8.18265 16 9.99998 16C11.8173 16 13.4459 15.1921 14.5462 13.9158C13.756 12.195 12.0175 11 9.99993 11Z" fill="#111827"/>
								</svg>
								<span>登录</span>
							</router-link>
						</a-col>
					</a-row>
				</a-layout-header>

				<!-- Page Content -->
				<a-layout-content class="content-container">
					<router-view />
				</a-layout-content>
				<!-- / Page Content -->

				
			</a-layout>
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
/* 整体布局样式 */
.layout-default {
	display: flex;
	min-height: 100vh;
}

/* 左侧固定导航样式 */
.side-nav {
	height: 100%;
	background-color: #f5f5f5;
	box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
	z-index: 10;
	position: fixed;
	left: 0;
}

.side-nav-header {
	display: flex;
	align-items: center;
	padding: 16px;
	border-bottom: 1px solid #f5f5f5;
}

.side-nav-header img {
	width: 32px;
	height: 32px;
	margin-right: 12px;
	border-radius: 6px;
}

.side-nav-header span {
	font-size: 16px;
	font-weight: 600;
	white-space: nowrap;
}

.side-nav-items {
	display: flex;
	flex-direction: column;
	gap: 10px;
	padding: 6px;
	overflow-y: auto;
	height: calc(100% - 64px);
}

.side-nav-item {
	display: flex;
	align-items: center;
	padding: 12px;
	border-radius: 8px;
	color: #111827;
	text-decoration: none;
	transition: all 0.3s ease;
	font-size: 14px;
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
	margin-right: 12px;
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

/* 主内容区域样式 */
.main-content {
	flex: 1;
	background-color: #f5f5f5;
	margin-left: 250px;
}

/* 页眉样式 */
.header {
	background-color: #f5f5f5;
	padding: 16px 24px;
	height: auto;
	line-height: 1.5;
}

.page-header-heading {
	margin-top: 8px;
}

.page-header-heading-title {
	font-size: 20px;
	font-weight: 600;
	color: #111827;
}

.header-control {
	display: flex;
	align-items: center;
	justify-content: flex-end;
	gap: 16px;
}

.header-search {
	max-width: 280px;
	border-radius: 8px;
}

.btn-sign-in {
	display: flex;
	align-items: center;
	gap: 8px;
	padding: 8px 12px;
	border-radius: 6px;
	color: #111827;
	text-decoration: none;
	transition: all 0.3s ease;
	background-color: rgba(0, 0, 0, 0.02);
	
	&:hover {
		background-color: rgba(0, 0, 0, 0.05);
		color: #1890ff;
	}
	
	svg {
		margin-right: 4px;
	}
}

.content-container {
	padding: 24px;
	min-height: 280px;
}

/* 页脚样式 */
a-layout-footer {
	background-color: transparent;
	padding: 20px 24px 24px;
}

.copyright {
	font-size: 14px;
	color: #8c8c8c;
	margin-bottom: 0;
	margin-top: 12px;
}

.copyright a {
	color: #8c8c8c;
	font-weight: 600;
	text-decoration: none;
}

.copyright a:hover {
	color: #1890ff;
}

.copyright svg {
	margin: 0 3px;
	position: relative;
	top: 4px;
}

.footer-control {
	display: flex;
	justify-content: flex-end;
}

.ant-menu-horizontal {
	border-bottom: none;
	background-color: transparent;
}

.ant-menu-horizontal > .ant-menu-item {
	margin-right: 0;
	padding: 0 10px;
	color: #8c8c8c;
	border-bottom: none;
	font-size: 14px;
	line-height: 38px;
	height: 38px;
}

.ant-menu-horizontal > .ant-menu-item:hover {
	color: #1890ff;
}

@media (max-width: 768px) {
	.footer-control {
		justify-content: flex-start;
		margin-top: 12px;
	}
	
	.header-control {
		justify-content: flex-start;
		margin-top: 16px;
	}
}

.nav-divider {
	height: 1px;
	background-color: rgba(0, 0, 0, 0.1);
	margin: 8px 0;
}
</style> 
