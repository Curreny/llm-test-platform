<template>
  <div class="cover-container">
    <!-- 全屏Hero区域，包含导航栏和标题介绍 -->
    <div class="hero-fullscreen">
      <!-- 导航栏部分 -->
      <div class="hero-navbar">
        <div class="navbar-brand">
          <h3>飞舞不会coding</h3>
        </div>
        <div class="navbar-links">
          <a href="#" class="nav-link active">主页</a>
          <a href="#" class="nav-link">成果</a>
          <a href="#" class="nav-link">关于</a>
          <a href="#" class="nav-link">博客</a>
          <a href="#" class="nav-link">联系</a>
        </div>
        <div class="navbar-actions">
          <a href="#" class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="nav-svg">
              <path d="M15 17H20L18.5951 15.5951C18.2141 15.2141 18 14.6973 18 14.1585V11C18 8.38757 16.3304 6.16509 14 5.34142V5C14 3.89543 13.1046 3 12 3C10.8954 3 10 3.89543 10 5V5.34142C7.66962 6.16509 6 8.38757 6 11V14.1585C6 14.6973 5.78595 15.2141 5.40493 15.5951L4 17H9M15 17V18C15 19.6569 13.6569 21 12 21C10.3431 21 9 19.6569 9 18V17M15 17H9" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <a href="#" class="nav-icon">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="nav-svg">
              <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15M17 10L12 15M12 15L7 10M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </a>
          <a-button type="primary" shape="round" class="signup-btn">登录/注册</a-button>
        </div>
      </div>
      
      <!-- 标题介绍部分 -->
      <div class="hero-content">
        <div class="hero-left">
          <div class="platform-icon mb-10">
          </div>
          <h1 class="hero-title">大模型综合观测展示平台</h1>

          <p class="hero-description">多维度、全流程的安全性和能力观测方法</p>
          <div class="hero-actions">
            <a-button type="primary" size="large" shape="round" class="hero-btn" @click="navigateToDashboard">
              <span>立即开始</span>
              <svg class="ml-5" width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path fill-rule="evenodd" clip-rule="evenodd" d="M7.29289 14.7071C6.90237 14.3166 6.90237 13.6834 7.29289 13.2929L10.5858 10L7.29289 6.70711C6.90237 6.31658 6.90237 5.68342 7.29289 5.29289C7.68342 4.90237 8.31658 4.90237 8.70711 5.29289L12.7071 9.29289C13.0976 9.68342 13.0976 10.3166 12.7071 10.7071L8.70711 14.7071C8.31658 15.0976 7.68342 15.0976 7.29289 14.7071Z" fill="#ffffff"/>
              </svg>
            </a-button>
          </div>
        </div>
        <div class="hero-right">
          <img src="/images/info-card-1.jpg" alt="大模型综合观测展示平台" class="hero-image">
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-section">
      <div class="cover-content">
        <!-- 问题说明卡片 -->
        <a-row :gutter="24" class="mb-24">
          <a-col :span="24">
            <a-card :bordered="false" class="problem-card gradient-bg">
              <div class="card-header mb-15">
                <h2 class="font-bold">问题说明</h2>
                <div class="header-line"></div>
              </div>
              <p class="problem-text">
                随着大模型技术的发展，性能漂移、数据泄露、结果不可控、数据偏见、AI幻觉等问题日益凸显，引发了全球范围内对AI安全的关注。为了应对这些挑战，国内外政策、法规迎来了新的探索与实践，安全行业也在积极探讨如何确保大模型性能与合规性。大模型能力与安全观测需要多维度、全流程的安全性和能力观测方法。
              </p>
            </a-card>
          </a-col>
        </a-row>

        <!-- 特色统计卡片 -->
        <a-row :gutter="24" class="mb-24">
          <a-col :span="24" :lg="8" class="mb-24">
            <a-card :bordered="false" class="widget-1 widget-1-blue">
              <a-statistic
                title="安全观测能力"
                :value="100"
                suffix="%"
                :precision="1"
                class="text-success"
              >
              </a-statistic>
              <div class="icon">
                <svg width="22" height="22" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 6C9 7.65685 7.65685 9 6 9C4.34315 9 3 7.65685 3 6C3 4.34315 4.34315 3 6 3C7.65685 3 9 4.34315 9 6Z" fill="#1890FF"/>
                  <path d="M17 6C17 7.65685 15.6569 9 14 9C12.3431 9 11 7.65685 11 6C11 4.34315 12.3431 3 14 3C15.6569 3 17 4.34315 17 6Z" fill="#1890FF"/>
                  <path d="M12.9291 17C12.9758 16.6734 13 16.3395 13 16C13 14.3648 12.4393 12.8606 11.4998 11.6691C12.2352 11.2435 13.0892 11 14 11C16.7614 11 19 13.2386 19 16V17H12.9291Z" fill="#1890FF"/>
                  <path d="M6 11C8.76142 11 11 13.2386 11 16V17H1V16C1 13.2386 3.23858 11 6 11Z" fill="#1890FF"/>
                </svg>
              </div>
            </a-card>
          </a-col>
          <a-col :span="24" :lg="8" class="mb-24">
            <a-card :bordered="false" class="widget-1 widget-1-purple">
              <a-statistic
                title="题库容量"
                :value="500"
                suffix="+"
                :precision="0"
                class="text-primary"
              >
              </a-statistic>
              <div class="icon">
                <svg width="22" height="22" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M3.17157 5.17157C4.73367 3.60948 7.26633 3.60948 8.82843 5.17157L10 6.34315L11.1716 5.17157C12.7337 3.60948 15.2663 3.60948 16.8284 5.17157C18.3905 6.73367 18.3905 9.26633 16.8284 10.8284L10 17.6569L3.17157 10.8284C1.60948 9.26633 1.60948 6.73367 3.17157 5.17157Z" fill="#B37FEB"/>
                </svg>
              </div>
            </a-card>
          </a-col>
          <a-col :span="24" :lg="8" class="mb-24">
            <a-card :bordered="false" class="widget-1 widget-1-green">
              <a-statistic
                title="审核成功率"
                :value="90"
                suffix="%"
                :precision="0"
                class="text-success"
              >
              </a-statistic>
              <div class="icon">
                <svg width="22" height="22" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18ZM13.7071 8.70711C14.0976 8.31658 14.0976 7.68342 13.7071 7.29289C13.3166 6.90237 12.6834 6.90237 12.2929 7.29289L9 10.5858L7.70711 9.29289C7.31658 8.90237 6.68342 8.90237 6.29289 9.29289C5.90237 9.68342 5.90237 10.3166 6.29289 10.7071L8.29289 12.7071C8.68342 13.0976 9.31658 13.0976 9.70711 12.7071L13.7071 8.70711Z" fill="#52C41A"/>
                </svg>
              </div>
            </a-card>
          </a-col>
        </a-row>

        <!-- 用户期望部分 - 六个卡片 -->
        <div class="card-header mb-15">
          <h2 class="font-bold">用户期望</h2>
          <div class="header-line"></div>
        </div>
        <a-row :gutter="24" type="flex" align="stretch">
          <!-- 观测题库生成模块 -->
          <a-col :span="24" :md="12" :xl="8" class="mb-24">
            <router-link to="/question-generate" class="card-link">
              <a-card :bordered="false" class="feature-card feature-primary">
                <div class="feature-icon mb-4 icon-primary">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M9 12H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M9 16H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="font-bold mb-2">观测题库生成模块</h3>
                <p>能够根据用户输入，自动化生成大模型性能观测题库，题目形式不限于选择、简答与判断等，题目内容来源不限于爬虫、模型生成等，观测题库生成形式不限，测试题库不低于500题。</p>
                <div class="card-footer">
                  <a-tag color="blue">自动生成</a-tag>
                  <a-tag color="cyan">500+题目</a-tag>
                </div>
              </a-card>
            </router-link>
          </a-col>

          <!-- 观测题库拓展模块 -->
          <a-col :span="24" :md="12" :xl="8" class="mb-24">
            <router-link to="/question-expansion" class="card-link">
              <a-card :bordered="false" class="feature-card feature-purple">
                <div class="feature-icon mb-4 icon-purple">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 3V5M16 3V5M7 21H17C19.2091 21 21 19.2091 21 17V9C21 6.79086 19.2091 5 17 5H7C4.79086 5 3 6.79086 3 9V17C3 19.2091 4.79086 21 7 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M8 9H16M8 13H14M8 17H12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="font-bold mb-2">观测题库拓展模块</h3>
                <p>能够自动化拓展测试题库，根据生成的测试题库，能够对测试题库进行"变形"，变形方式不低于5种，需展示变形过程，展现形式不限，变形后的题目有效性不低于90%。</p>
                <div class="card-footer">
                  <a-tag color="purple">5+变形方式</a-tag>
                  <a-tag color="magenta">90%有效性</a-tag>
                </div>
              </a-card>
            </router-link>
          </a-col>

          <!-- 数据审核模块 -->
          <a-col :span="24" :md="12" :xl="8" class="mb-24">
            <router-link to="/" class="card-link">
              <a-card :bordered="false" class="feature-card feature-success">
                <div class="feature-icon mb-4 icon-success">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="font-bold mb-2">数据审核模块</h3>
                <p>针对大模型测试结果，平台能够自动审核测试结果，并将大模型输入、输出与判定结果进行页面展示，需支持多种审核模式，且自动化判定审核成功率大于90%。</p>
                <div class="card-footer">
                  <a-tag color="green">多审核模式</a-tag>
                  <a-tag color="lime">实时判定</a-tag>
                </div>
              </a-card>
            </router-link>
          </a-col>

          <!-- 结果生成模块 -->
          <a-col :span="24" :md="12" :xl="8" class="mb-24">
            <router-link to="/" class="card-link">
              <a-card :bordered="false" class="feature-card feature-warning">
                <div class="feature-icon mb-4 icon-warning">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="nav-svg">
                    <path d="M21 21H4C3.44772 21 3 20.5523 3 20V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 14L11 10L15 14L21 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M21 8V14H15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="font-bold mb-2">结果生成模块</h3>
                <p>平台根据数据审核能力，自动化生成测试总体结果，结果包括模型的性能、安全性、推理速度、精度、内存和计算资源的消耗情况等，结果展现形式不唯一，多样化的呈现方式。</p>
                <div class="card-footer">
                  <a-tag color="orange">多维度分析</a-tag>
                  <a-tag color="gold">精确统计</a-tag>
                </div>
              </a-card>
            </router-link>
          </a-col>

          <!-- 自动化报告生成 -->
          <a-col :span="24" :md="12" :xl="8" class="mb-24">
            <router-link to="/" class="card-link">
              <a-card :bordered="false" class="feature-card feature-info">
                <div class="feature-icon mb-4 icon-info">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="nav-svg">
                    <path d="M19 3H5C3.89543 3 3 3.89543 3 5V19C3 20.1046 3.89543 21 5 21H19C20.1046 21 21 20.1046 21 19V5C21 3.89543 20.1046 3 19 3Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 7H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 12H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 17H13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="font-bold mb-2">自动化报告生成</h3>
                <p>支持自动生成性能与安全性观测报告，供用户下载和审阅。</p>
                <div class="card-footer">
                  <a-tag color="#13C2C2">PDF报告</a-tag>
                  <a-tag color="#08979C">可视化图表</a-tag>
                </div>
              </a-card>
            </router-link>
          </a-col>

          <!-- 观测调用形式 -->
          <a-col :span="24" :md="12" :xl="8" class="mb-24">
            <router-link to="/" class="card-link">
              <a-card :bordered="false" class="feature-card feature-danger">
                <div class="feature-icon mb-4 icon-danger">
                  <svg width="40" height="40" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M10 20L14 4M18 8L22 12L18 16M6 16L2 12L6 8" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <h3 class="font-bold mb-2">观测调用形式</h3>
                <p>支持多样化平台调用形式，包括但不限于SDK、Saas等。</p>
                <div class="card-footer">
                  <a-tag color="red">API接口</a-tag>
                  <a-tag color="volcano">SDK包</a-tag>
                  <a-tag color="orange">SaaS服务</a-tag>
                </div>
              </a-card>
            </router-link>
          </a-col>
        
          <a-col :span="24" class="mb-50">
            <a-card :bordered="false" class="card-info">
              <a-row type="flex">
                <a-col class="col-content" :span="24" :xl="14">
                  <div class="card-content">
                    <h6>立即开始</h6>
                    <h5>体验飞舞不会coding团队平台</h5>
                    <p>我们的平台提供了完整的团队协作解决方案，支持多维度、全流程的项目管理与开发。</p>
                  </div>
                  <div class="card-footer">
                    <a-button type="primary" size="large" shape="round" @click="navigateToDashboard">
                      <span>开始体验</span>
                      <svg class="ml-5" width="16" height="16" viewBox="0 0 20 20" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M7.29289 14.7071C6.90237 14.3166 6.90237 13.6834 7.29289 13.2929L10.5858 10L7.29289 6.70711C6.90237 6.31658 6.90237 5.68342 7.29289 5.29289C7.68342 4.90237 8.31658 4.90237 8.70711 5.29289L12.7071 9.29289C13.0976 9.68342 13.0976 10.3166 12.7071 10.7071L8.70711 14.7071C8.31658 15.0976 7.68342 15.0976 7.29289 14.7071Z" fill="#ffffff"/>
                      </svg>
                    </a-button>
                  </div>
                </a-col>
                <a-col class="col-img" :span="24" :xl="10">
                  <div class="card-img-bg">
                    <img src="images/info-card-2.jpg" alt="">
                  </div>
                </a-col>
              </a-row>
            </a-card>
          </a-col>
        </a-row>
      </div>
    </div>

    <!-- 新的页脚样式 -->
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
  </div>
</template>

<script>
export default {
  data() {
    return {
      isScrolled: false,
      lastScrollTop: 0
    };
  },
  methods: {
    navigateToDashboard() {
      this.$router.push('/dashboard');
    },
    handleScroll() {
      const navbar = document.querySelector('.hero-navbar');
      if (!navbar) return;
      
      const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
      
      // 导航栏在滚动时添加背景
      if (scrollTop > 60) {
        if (!this.isScrolled) {
          navbar.classList.add('navbar-scrolled');
          this.isScrolled = true;
        }
      } else {
        if (this.isScrolled) {
          navbar.classList.remove('navbar-scrolled');
          this.isScrolled = false;
        }
      }
      
      this.lastScrollTop = scrollTop;
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    
    this.$nextTick(() => {
      this.handleScroll();
    });
  },
  beforeDestroy() {
    window.removeEventListener('scroll', this.handleScroll);
  }
};
</script>

<style lang="scss" scoped>


.card-link {
  display: block;
  text-decoration: none;
  color: inherit;
  height: 100%;
  
  &:hover {
    .feature-card {
      transform: translateY(-5px);
      box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
    }
  }
}

.feature-card {
  height: 100%;
  transition: all 0.3s ease;
  
  // ... existing feature-card styles if any ...
}

// ... rest of existing code ...
</style>

