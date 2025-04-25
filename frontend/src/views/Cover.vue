<template>
  <div class="cover-container">
    <!-- 全屏Hero区域，包含导航栏和标题介绍 -->
    <div class="hero-fullscreen" id="home">
      <!-- 导航栏部分 -->
      <div class="hero-navbar">
        <div class="navbar-brand">
          <h3><img src="/images/logo-ct-white.png" style="width: 35px; height: 35px;">飞舞不会coding</h3>
        </div>
        <div class="navbar-links">
          <router-link to="/" class="nav-link active">主页</router-link>
          <router-link to="/question-generate" class="nav-link">观测题库生成</router-link>
          <router-link to="/question-expansion" class="nav-link">观测题库拓展</router-link>
          <router-link to="/data-audit" class="nav-link">模型响应检测</router-link>
          <router-link @click.native="navigateTo('/data-audit#results-preview')" to="/data-audit" class="nav-link">检测结果预览</router-link>
          <router-link @click.native="navigateTo('/data-audit#report-generation')" to="/data-audit" class="nav-link">报告生成与预览</router-link>
          <router-link to="/api-integration" class="nav-link">观测调用</router-link>
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
          <a-button href="/Sign-In" type="primary" shape="round" class="signup-btn">登录/注册</a-button>
        </div>
      </div>
      
      <!-- 标题介绍部分 -->
      <div class="hero-content">
        <div class="hero-left">
          <div class="platform-icon mb-10">
          </div>
          <h1 class="hero-title">天枢智评&nbsp;—</h1>
          <h1 class="hero-title">大模型综合观测展示平台</h1>

          <div class="hero-actions">
            <a-button @click="scrollToElement('#product')" type="primary" size="large" shape="round" class="hero-btn">
              <span>立即开始&nbsp;🚀&nbsp;🚀</span>
            </a-button>
          </div>
        </div>
        <div class="hero-right">
          <img src="/images/bg.png" alt="大模型综合观测展示平台" class="hero-image">
        </div>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="content-section">
      <div class="cover-content">
        <!-- 问题说明卡片 -->
        <a-row :gutter="24" class="mb-24">
          <a-col :span="24">
            <a-card :bordered="false" class="problem-card gradient-bg scroll-animation">
              <div class="card-header mb-15">
                <h2 class="font-bold">📢平台介绍</h2>
              </div>
              <p class="problem-text">
              &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;随着大模型技术的快速发展，性能漂移、数据泄露、安全合规等问题日益凸显，成为AI产业健康发展的关键挑战。本平台提供了全面的大模型能力与安全观测解决方案，通过题库生成、自动化测试、模型响应检测和报告生成等功能，帮助您全方位评估大模型的性能、安全性与合规性。使用我们的平台，您可以轻松发现模型潜在风险，获取专业评估报告，确保AI应用安全可控、合规可信。立即开始，提升您的大模型质量与安全水平！
              </p>
            </a-card>
          </a-col>
        </a-row>

        <!-- 特色统计卡片 -->
        <a-row :gutter="24" class="mb-24 scroll-animation">
          <a-col :span="24" :lg="8" class="mb-24">
            <a-card :bordered="false" class="widget-1">
              <a-statistic
                title="安全观测能力"
                :value="93"
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
            <a-card :bordered="false" class="widget-1">
              <a-statistic
                title="题库容量"
                :value="150000"
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
            <a-card :bordered="false" class="widget-1">
              <a-statistic
                title="审核成功率"
                :value="98.34"
                suffix="%"
                :precision="2"
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

        <div class="scroll-animation">
          <!-- 用户期望部分 - 六个卡片 -->
          <div class="card-header mb-15" id="product">
            <h2 class="font-bold">📊平台总览</h2>
          </div>
          <a-row :gutter="24" type="flex" align="stretch">
            <!-- 观测题库生成模块 -->
            <a-col :span="24" :md="12" :xl="8" class="mb-24">
              <router-link to="/question-generate" class="card-link">
                <a-card :bordered="false" class="feature-card feature-primary">
                  <h4 class="font-bold mb-2 ">📚&nbsp;观测题库生成</h4>
                  <p>能够根据用户输入，自动化生成大模型性能观测题库，题目形式不限于选择、简答与判断等，题目内容来源丰富，测试题库单次可生成3000题。</p>
                  <div class="card-footer">
                    <a-tag color="blue">自动生成</a-tag>
                    <a-tag color="cyan">3000+题目</a-tag>
                  </div>
                </a-card>
              </router-link>
            </a-col>

            <!-- 观测题库拓展模块 -->
            <a-col :span="24" :md="12" :xl="8" class="mb-24">
              <router-link to="/question-expansion" class="card-link">
                <a-card :bordered="false" class="feature-card feature-purple">
                  <h4 class="font-bold mb-2">🛠️&nbsp;观测题库拓展</h4>
                  <p>能够自动化拓展测试题库，根据生成的测试题库，能够对测试题库进行"变形"，变形方式可任选6种，变形后的题目有效性达95%。</p>
                  <div class="card-footer">
                    <a-tag color="purple">6种变形方式</a-tag>
                    <a-tag color="magenta">95%有效性</a-tag>
                  </div>
                </a-card>
              </router-link>
            </a-col>

            <!-- 模型响应检测模块 -->
            <a-col :span="24" :md="12" :xl="8" class="mb-24">
              <router-link to="/data-audit#header-data-audit" class="card-link">
                <a-card :bordered="false" class="feature-card feature-success">

                  <h4 class="font-bold mb-2">📶&nbsp;模型响应检测</h4>
                  <p>针对大模型测试结果，平台能够自动审核测试结果，并将大模型输入、输出与判定结果进行页面展示，支持规则匹配和模型辅助2种审核模式，且自动化判定审核成功率大于90%。</p>
                  <div class="card-footer">
                    <a-tag color="green">多审核模式</a-tag>
                    <a-tag color="lime">实时判定</a-tag>
                  </div>
                </a-card>
              </router-link>
            </a-col>

            <!-- 结果生成模块 -->
            <a-col :span="24" :md="12" :xl="8" class="mb-24">
              <router-link to="/data-audit#results-preview" class="card-link">
                <a-card :bordered="false" class="feature-card feature-warning">

                  <h4 class="font-bold mb-2">📊&nbsp;检测结果预览</h4>
                  <p>平台根据模型响应检测能力，自动化生成测试总体结果，结果包括模型的性能、安全性、推理速度、精度、内存和计算资源的消耗情况等。</p>
                  <div class="card-footer">
                    <a-tag color="orange">多维度分析</a-tag>
                    <a-tag color="gold">精确统计</a-tag>
                  </div>
                </a-card>
              </router-link>
            </a-col>

            <!-- 自动化报告生成 -->
            <a-col :span="24" :md="12" :xl="8" class="mb-24">
              <router-link to="/data-audit#report-generation" class="card-link">
                <a-card :bordered="false" class="feature-card feature-info">

                  <h4 class="font-bold mb-2">📝&nbsp;报告生成与预览</h4>
                  <p>平台支持自动生成性能与安全性观测报告，包括HTML、PDF格式，供用户下载和审阅。</p>
                  <div class="card-footer">
                    <a-tag color="#13C2C2">PDF报告</a-tag>
                    <a-tag color="#08979C">可视化图表</a-tag>
                  </div>
                </a-card>
              </router-link>
            </a-col>

            <!-- 观测调用形式 -->
            <a-col :span="24" :md="12" :xl="8" class="mb-24">
              <router-link to="/api-integration" class="card-link">
                <a-card :bordered="false" class="feature-card feature-danger">
                  <h4 class="font-bold mb-2">🧩&nbsp;观测调用</h4>
                  <p>支持多样化平台调用形式，包括但不限于SDK、Saas等。</p>
                  <div class="card-footer">
                    <a-tag color="red">API接口</a-tag>
                    <a-tag color="volcano">SDK包</a-tag>
                    <a-tag color="orange">SaaS服务</a-tag>
                  </div>
                </a-card>
              </router-link>
            </a-col>
          </a-row>
        </div>

        <a-row :gutter="24" type="flex" align="stretch" class="scroll-animation">
          <a-col :span="24" class="mb-50">
            <a-card :bordered="false" class="team-card">
              <div class="card-header mb-15">
                <h2 class="font-bold">🤝我们的团队</h2>
              </div>
              <div class="team-members">
                <a-row :gutter="[48, 48]" type="flex" justify="center">
                  <a-col :span="24" :sm="12" :md="8" :lg="4" class="text-center">
                    <div class="team-member">
                      <div class="member-avatar">
                        <img src="/images/avatar-1.png">
                      </div>
                      <h3 class="member-name">小沈</h3>
                      <p class="member-role">项目负责人</p>
                      <p class="member-desc">项目整体规划</p>
                      <p class="member-desc">项目架构设计</p>
                    </div>
                  </a-col>
                  <a-col :span="24" :sm="12" :md="8" :lg="4" class="text-center">
                    <div class="team-member">
                      <div class="member-avatar">
                        <img src="/images/avatar-2.png">
                      </div>
                      <h3 class="member-name">小孙</h3>
                      <p class="member-role">前后端开发</p>
                      <p class="member-desc">用户界面与交互设计</p>
                      <p class="member-desc">后端代码性能调试</p>
                    </div>
                  </a-col>
                  <a-col :span="24" :sm="12" :md="8" :lg="4" class="text-center">
                    <div class="team-member">
                      <div class="member-avatar">
                        <img src="/images/avatar-3.png">
                      </div>
                      <h3 class="member-name">小邱</h3>
                      <p class="member-role">技术总监</p>
                      <p class="member-desc">策划方案制定</p>
                      <p class="member-desc">架构设计</p>
                    </div>
                  </a-col>
                  <a-col :span="24" :sm="12" :md="8" :lg="4" class="text-center">
                    <div class="team-member">
                      <div class="member-avatar">
                        <img src="/images/avatar-4.png">
                      </div>
                      <h3 class="member-name">小平</h3>
                      <p class="member-role">系统开发</p>
                      <p class="member-desc">数据逻辑存储</p>
                      <p class="member-desc">界面设计</p>
                    </div>
                  </a-col>
                  <a-col :span="24" :sm="12" :md="8" :lg="4" class="text-center">
                    <div class="team-member">
                      <div class="member-avatar">
                        <img src="/images/avatar-5.png">
                      </div>
                      <h3 class="member-name">小陈</h3>
                      <p class="member-role">数据分析师</p>
                      <p class="member-desc">观测数据集收集</p>
                      <p class="member-desc">观测数据集清洗整理</p>
                    </div>
                  </a-col>
                </a-row>
              </div>
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
        <p class="copyright">版权所有 © 2025 飞舞不会coding</p>
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
import WidgetCounter from '../components/Widgets/WidgetCounter';
export default {
  name: 'Cover',
  components: {
    WidgetCounter
  },
  data() {
    return {
      isScrolled: false,
      lastScrollTop: 0
    };
  },
  methods: {
    scrollToElement(selector) {
      const element = document.querySelector(selector);
      if (element) {
        window.scrollTo({
          top: element.offsetTop + 1000,
          behavior: 'smooth'
        });
      }
    },
    navigateTo(path) {
      if (path.includes('#')) {
        const parts = path.split('#');
        if (parts[0] === '' || parts[0] === '/') {
          // 如果是当前页面内的锚点
          this.scrollToElement('#' + parts[1]);
        } else {
          // 如果是其他页面的锚点
          this.$router.push(path);
        }
      } else {
        this.$rouer.push(path);
      }
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
      
      // 检查元素是否在可视区域内，如果是则添加动画类
      this.checkScrollAnimation();
    },
    
    // 添加检查滚动动画的方法
    checkScrollAnimation() {
      const animatedElements = document.querySelectorAll('.scroll-animation:not(.animated)');
      
      animatedElements.forEach(element => {
        const elementTop = element.getBoundingClientRect().top;
        const elementVisible = 150; // 元素顶部距离视口底部的触发距离
        
        if (elementTop < window.innerHeight - elementVisible) {
          element.classList.add('animated');
        }
      });
    },
    initScrollAnimation() {
      // 初始检查一次，处理页面加载时已在视口内的元素
      this.checkScrollAnimation();
    }
  },
  mounted() {
    window.addEventListener('scroll', this.handleScroll);
    
    this.$nextTick(() => {
      this.handleScroll();
    });
    
    // 添加滚动监听
    this.initScrollAnimation();
    window.addEventListener('scroll', this.checkScrollAnimation);
  },
  beforeDestroy() {
    // 移除滚动监听，防止内存泄漏
    window.removeEventListener('scroll', this.checkScrollAnimation);
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

.navbar-links a {
  cursor: pointer;
}

.team-card {
  padding: 0px;
  border-radius: 12px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.08);
  background-color: #fff;
  margin-top: 20px;
}

.team-members {
  margin-top: 32px;
  margin-bottom: 30px;
}

.team-member {
  display: flex;
  flex-direction: column;
  align-items: center;
  transition: all 0.3s ease;
}

.team-member:hover {
  transform: translateY(-5px);
  cursor: pointer;
}

.member-avatar {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  margin: 0 auto 24px;
  overflow: hidden;
  border: 3px solid #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.member-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.member-avatar:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.15);
}

.avatar-text {
  font-size: 40px;
  font-weight: bold;
  color: #fff;
}

.member-name {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 8px;
  color: #333;
}

.member-role {
  font-size: 16px;
  color: #1890ff;
  margin-bottom: 10px;
  font-weight: 500;
  background-color: rgba(24, 144, 255, 0.1);
  padding: 4px 12px;
  border-radius: 12px;
}

.member-desc {
  font-size: 14px;
  color: #666;
  text-align: center;
  max-width: 180px;
  margin: 0 auto;
  line-height: 1.5;
}

.card-header {
  text-align: center;
  margin-bottom: 24px;
}

.card-header h2 {
  font-size: 28px;
  color: #333;
  margin-bottom: 16px;
}

.header-line {
  height: 3px;
  width: 60px;
  background: linear-gradient(90deg, #1890ff, #722ed1);
  margin: 0 auto;
  border-radius: 3px;
}

// 平台介绍卡片美化样式
.problem-card.gradient-bg {
  position: relative;
  border-radius: 16px !important;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  border: none !important;
  background: linear-gradient(135deg, #f5f7fa, #ebf0f6);
  
  .card-header {
    z-index: 1;
    margin-bottom: 20px;
    text-align: center;
    
    h2 {
      font-size: 28px;
      font-weight: 600;
      color: #222;
      margin-bottom: 5px;
      
    }
  }
  
  .problem-text {
    position: relative;
    z-index: 1;
    font-size: 16px;
    line-height: 1.8;
    color: rgba(0, 0, 0, 0.75);
    margin-bottom: 0;
    text-align: justify;
    padding: 5px 0;
    
  }
  
  
  // 添加悬停效果
  &:hover {
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.12);
    transform: translateY(-3px);
    transition: all 0.3s ease;
    cursor: pointer;
  }
}

/* 滚动动画相关样式 */
.scroll-animation {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.5s ease-out;
}

.scroll-animation.animated {
  opacity: 1;
  transform: translateY(0);
}

/* 为不同元素设置不同的延迟，实现错落动画效果 */
.problem-card.scroll-animation {
  transition-delay: 0.1s;
}

.feature-card.scroll-animation {
  transition-delay: 0.1s;
}

.team-card.scroll-animation {
  transition-delay: 0.1s;
}

.team-member.scroll-animation {
  transition-delay: 0.1s;
}

.widget-1:hover{
  transform: scale(1.03);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
}
</style>

