<template>
  <div class="question-generate-container">
    <!-- 页面标题部分 -->
    <a-row :gutter="24" class="mb-24">
      <a-col :span="24">
        <a-card :bordered="false" class="header-card gradient-bg">
          <div class="card-header mb-15">
            <h2 class="font-bold">观测题库生成模块</h2>
            <div class="header-line"></div>
          </div>
          <p class="problem-text">
            自动化生成大模型性能观测题库，支持多种题型和生成方式，提供500+高质量测试题目。
          </p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="24" class="mb-24">
      <!-- 左侧控制面板 -->
      <a-col :span="24" :lg="8" class="mb-24">
        <a-card :bordered="false" class="control-panel">
          <div class="card-header mb-15">
            <h3 class="font-bold">题库生成设置</h3>
            <div class="header-line"></div>
          </div>
          
          <!-- 题目数量设置 -->
          <div class="form-item">
            <div class="form-label">
              <span class="icon-wrapper">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 7H5M3 12H5M3 17H5M8 7H21M8 12H21M8 17H21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              生成题目数量
            </div>
            <a-slider
              v-model="questionCount"
              :min="500"
              :max="1000"
              :step="10"
              show-tooltip
            />
            <div class="slider-value">{{questionCount}}题</div>
          </div>
          
          <!-- 题目类型选择 -->
          <div class="form-item">
            <div class="form-label">
              <span class="icon-wrapper">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              题目类型选择
            </div>
            <a-checkbox-group v-model="selectedTypes" class="data-source-group">
              <a-checkbox value="single">选择题</a-checkbox>
              <a-checkbox value="essay">问答题</a-checkbox>
            </a-checkbox-group>
          </div>
          
          <!-- 题目来源选择 -->
          <div class="form-item">
            <div class="form-label">
              <span class="icon-wrapper">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 3.32997V20.67C9 21.4 9.98 21.67 10.43 21.07L17.86 13.64C18.34 13.16 18.34 12.37 17.86 11.89L10.43 4.45997C9.98 3.85997 9 4.12997 9 4.84997V3.32997Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              题目来源选择
            </div>
            <a-checkbox-group v-model="dataSources" class="data-source-group">
              <a-checkbox value="safetyBench">SafetyBench数据集</a-checkbox>
              <a-checkbox value="poisonMpts">100PoisonMpts数据集</a-checkbox>
              <a-checkbox value="cValues">CValues数据集</a-checkbox>
              <a-checkbox value="instructionAttack">指令攻击数据集</a-checkbox>
              <a-checkbox value="typicalSafety">典型安全数据集</a-checkbox>
            </a-checkbox-group>
          </div>
          
          <!-- 题目领域筛选 -->
          <div class="form-item">
            <div class="form-label">
              <span class="icon-wrapper">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M3 7.8C3 6.11984 3 5.27976 3.32698 4.63803C3.6146 4.07354 4.07354 3.6146 4.63803 3.32698C5.27976 3 6.11984 3 7.8 3H16.2C17.8802 3 18.7202 3 19.362 3.32698C19.9265 3.6146 20.3854 4.07354 20.673 4.63803C21 5.27976 21 6.11984 21 7.8V16.2C21 17.8802 21 18.7202 20.673 19.362C20.3854 19.9265 19.9265 20.3854 19.362 20.673C18.7202 21 17.8802 21 16.2 21H7.8C6.11984 21 5.27976 21 4.63803 20.673C4.07354 20.3854 3.6146 19.9265 3.32698 19.362C3 18.7202 3 17.8802 3 16.2V7.8Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M9 12L12 15L15 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 9V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              题目分类
            </div>
            <div class="tip-text">题目分类由数据集决定，无需指定</div>
          </div>
          
          <!-- 生成按钮 -->
          <a-button 
            type="primary" 
            size="large" 
            block 
            @click="generateQuestions" 
            :loading="isGenerating"
            class="generate-btn"
          >
            <span class="btn-content">
              <svg v-if="!isGenerating" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 22C17.5228 22 22 17.5228 22 12C22 6.47715 17.5228 2 12 2C6.47715 2 2 6.47715 2 12C2 17.5228 6.47715 22 12 22Z" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M12 8V16" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M8 12H16" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              {{ isGenerating ? '正在生成中...' : '生成题库' }}
            </span>
          </a-button>
          
          <!-- 导出选项 -->
          <div class="export-options" v-if="questions.length > 0">
            <div class="form-label mb-10">
              <span class="icon-wrapper">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              导出选项
            </div>
            <a-row :gutter="16">
              <a-col :span="12">
                <a-button 
                  type="default" 
                  block 
                  @click="exportToJson" 
                  class="export-btn"
                  :disabled="isGenerating"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="export-icon">
                    <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  导出为JSON
                </a-button>
              </a-col>
              <a-col :span="12">
                <a-button 
                  type="default" 
                  block 
                  @click="exportToExcel" 
                  class="export-btn"
                  :disabled="isGenerating"
                >
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="export-icon">
                    <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                  导出为Excel
                </a-button>
              </a-col>
            </a-row>
          </div>
        </a-card>
        
        <!-- 统计卡片 -->
        <div v-if="questions.length > 0" class="stats-cards mb-24">
          <a-row :gutter="16">
            <a-col :span="8">
              <a-card :bordered="false" class="widget-1 widget-1-blue">
                <a-statistic
                  title="总题目数"
                  :value="questions.length"
                  class="text-primary"
                >
                </a-statistic>
                <div class="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="#1890ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card :bordered="false" class="widget-1 widget-1-purple">
                <a-statistic
                  :title="getTopDomain"
                  :value="getTopDomainCount"
                  class="text-purple"
                >
                </a-statistic>
                <div class="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 3V5M16 3V5M7 21H17C19.2091 21 21 19.2091 21 17V9C21 6.79086 19.2091 5 17 5H7C4.79086 5 3 6.79086 3 9V17C3 19.2091 4.79086 21 7 21Z" stroke="#722ed1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card :bordered="false" class="widget-1 widget-1-green">
                <a-statistic
                  :title="getTopType"
                  :value="getTopTypeCount"
                  class="text-success"
                >
                </a-statistic>
                <div class="icon">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#52c41a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
              </a-card>
            </a-col>
          </a-row>
        </div>
      </a-col>
      
      <!-- 右侧题目展示区 -->
      <a-col :span="24" :lg="16">
        <a-card :bordered="false" class="questions-display">
          <div class="card-header mb-15">
            <h3 class="font-bold">生成结果</h3>
            <div class="header-line"></div>
          </div>
          
          <!-- 筛选工具栏 -->
          <div v-if="questions.length > 0" class="filter-toolbar mb-15">
            <a-row :gutter="16" type="flex" align="middle">
              <a-col :span="8">
                <a-input-search
                  placeholder="搜索题目关键词"
                  v-model="searchKeyword"
                  @search="handleSearch"
                  class="search-input"
                />
              </a-col>
              <a-col :span="8">
                <a-select v-model="filterType" style="width: 100%" placeholder="按题型筛选">
                  <a-select-option value="">全部题型</a-select-option>
                  <a-select-option value="single">选择题</a-select-option>
                  <a-select-option value="essay">问答题</a-select-option>
                </a-select>
              </a-col>
              <a-col :span="8">
                <a-select v-model="filterDomain" style="width: 100%" placeholder="按领域筛选">
                  <a-select-option value="">全部领域</a-select-option>
                  <a-select-option v-for="domain in domainStats" :key="domain.name" :value="domain.name">
                    {{domain.name}} ({{domain.count}})
                  </a-select-option>
                </a-select>
              </a-col>
            </a-row>
          </div>
          
          <!-- 题目列表 -->
          <div v-if="questions.length > 0" class="questions-list">
            <a-collapse accordion :bordered="false">
              <a-collapse-panel 
                v-for="(question, index) in paginatedQuestions" 
                :key="index" 
                :header="`问题 ${(currentPage - 1) * pageSize + index + 1}: ${question.prompt ? (question.prompt.length > 50 ? question.prompt.substring(0, 50) + '...' : question.prompt) : '无标题'}`"
                class="question-panel"
              >
                <div class="question-content">
                  <div class="question-tags">
                    <a-tag :color="getTypeColor(question.type)">{{getTypeName(question.type)}}</a-tag>
                    <a-tag color="blue">{{question.category || '未分类'}}</a-tag>
                    <a-tag color="purple">{{getSourceName(question.source)}}</a-tag>
                    <a-tag color="green">ID: {{question.id}}</a-tag>
                  </div>
                  
                  <div class="question-prompt">
                    <div class="label">问题:</div>
                    <div class="content">{{question.prompt}}</div>
                  </div>
                  
                  <div v-if="question.options && question.options.length > 0" class="question-options">
                    <div class="label">选项:</div>
                    <div class="options-list">
                      <div v-for="(option, optIndex) in question.options" :key="optIndex" class="option-item" 
                      :class="{'option-selected': isOptionSelected(question, optIndex)}">
                        <span class="option-letter">{{optionLetters[optIndex]}}</span>
                        <span class="option-text">{{option}}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div class="question-answer">
                    <div class="label">答案:</div>
                    <div class="content answer-content">{{question.answer}}</div>
                  </div>
                  
                  <div v-if="question.explanation" class="question-explanation">
                    <div class="label">解析:</div>
                    <div class="content">{{question.explanation}}</div>
                  </div>
                </div>
              </a-collapse-panel>
            </a-collapse>
            
            <!-- 分页器 -->
            <div class="pagination-container">
              <a-pagination
                v-model="currentPage"
                :total="filteredQuestions.length"
                :pageSize="pageSize"
                @change="handlePageChange"
                show-quick-jumper
                show-size-changer
                :pageSizeOptions="['10', '20', '50', '100', '200']"
                @showSizeChange="onShowSizeChange"
              />
              <div class="pagination-info">
                共 {{filteredQuestions.length}} 题，当前显示第 {{(currentPage-1)*pageSize+1}} - {{Math.min(currentPage*pageSize, filteredQuestions.length)}} 题
              </div>
            </div>
          </div>
          
          <!-- 空状态 -->
          <div v-else class="empty-state">
            <a-empty description="暂无生成的题目，请点击左侧「生成题库」按钮" />
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
export default {
  name: "QuestionGenerate",
  components: {},
  data() {
    return {
      // 生成设置
      questionCount: 10,
      selectedTypes: ['single', 'essay'],
      dataSources: ['safetyBench', 'poisonMpts', 'cValues', 'instructionAttack', 'typicalSafety'],
      selectedDomains: [],
      
      // 生成状态
      isGenerating: false,
      
      // 题目数据
      questions: [],
      originalQuestions: [],
      
      // 筛选相关
      searchKeyword: '',
      filterType: '',
      filterDomain: '',
      
      // 分页相关
      currentPage: 1,
      pageSize: 10,
      
      // 其他
      optionLetters: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    };
  },
  computed: {
    filteredQuestions() {
      let result = [...this.questions];
      
      // 关键词搜索
      if (this.searchKeyword) {
        const keyword = this.searchKeyword.toLowerCase();
        result = result.filter(q => 
          (q.prompt && q.prompt.toLowerCase().includes(keyword)) || 
          (q.answer && q.answer.toLowerCase().includes(keyword)) || 
          (q.explanation && q.explanation.toLowerCase().includes(keyword))
        );
      }
      
      // 按题型筛选
      if (this.filterType) {
        result = result.filter(q => q.type === this.filterType);
      }
      
      // 按领域筛选
      if (this.filterDomain) {
        result = result.filter(q => q.category === this.filterDomain);
      }
      
      return result;
    },
    
    // 添加分页后的题目计算属性
    paginatedQuestions() {
      const startIndex = (this.currentPage - 1) * this.pageSize;
      const endIndex = startIndex + this.pageSize;
      return this.filteredQuestions.slice(startIndex, endIndex);
    },
    domainStats() {
      const domains = {};
      this.questions.forEach(q => {
        const domain = q.category || '未分类';
        domains[domain] = (domains[domain] || 0) + 1;
      });
      
      return Object.keys(domains).map(name => ({
        name,
        count: domains[name]
      })).sort((a, b) => b.count - a.count);
    },
    getTopDomain() {
      return this.domainStats.length > 0 ? this.domainStats[0].name : '热门领域';
    },
    getTopDomainCount() {
      return this.domainStats.length > 0 ? this.domainStats[0].count : 0;
    },
    typeStats() {
      const types = {};
      this.questions.forEach(q => {
        const type = q.type || 'unknown';
        types[type] = (types[type] || 0) + 1;
      });
      
      return Object.keys(types).map(name => ({
        name,
        count: types[name]
      })).sort((a, b) => b.count - a.count);
    },
    getTopType() {
      if (this.typeStats.length === 0) return '热门题型';
      return this.getTypeName(this.typeStats[0].name);
    },
    getTopTypeCount() {
      return this.typeStats.length > 0 ? this.typeStats[0].count : 0;
    }
  },
  methods: {
    // 生成题目
    async generateQuestions() {
      if (this.selectedTypes.length === 0) {
        this.$message.error('请至少选择一种题目类型');
        return;
      }
      
      if (this.dataSources.length === 0) {
        this.$message.error('请至少选择一个题目来源');
        return;
      }
      
      this.isGenerating = true;
      
      try {
        const response = await fetch('http://localhost:5000/api/questions/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            questionCount: this.questionCount,
            types: this.selectedTypes,
            sources: this.dataSources,
            domains: this.selectedDomains
          })
        });
        
        const result = await response.json();
        
        if (result.success) {
          this.questions = result.data;
          this.originalQuestions = [...this.questions];
          this.$message.success(`成功生成${this.questions.length}道题目`);
        } else {
          throw new Error(result.message);
        }
      } catch (error) {
        console.error('生成题目失败:', error);
        this.$message.error('生成题目失败，请重试');
      } finally {
        this.isGenerating = false;
        this.currentPage = 1;
      }
    },
    
    // 判断选项是否被选中（用于多选题和选择题）
    isOptionSelected(question, optionIndex) {
      const optionLetter = this.optionLetters[optionIndex];
      
      if (question.type === 'single') {
        return question.answer === optionLetter;
      } else if (question.type === 'multiple') {
        return question.answer.split(',').includes(optionLetter);
      }
      
      return false;
    },
    
    // 获取题型名称
    getTypeName(type) {
      const typeNames = {
        'single': '选择题',
        'essay': '问答题',
        'unknown': '未知类型'
      };
      
      return typeNames[type] || '未知类型';
    },
    
    // 获取题型颜色
    getTypeColor(type) {
      const typeColors = {
        'single': 'blue',
        'essay': 'purple',
        'unknown': 'default'
      };
      
      return typeColors[type] || 'default';
    },
    
    // 获取来源名称
    getSourceName(source) {
      const sourceNames = {
        'safetyBench': 'SafetyBench',
        'poisonMpts': '100PoisonMpts',
        'cValues': 'CValues',
        'instructionAttack': '指令攻击',
        'typicalSafety': '典型安全',
        'unknown': '未知来源'
      };
      
      return sourceNames[source] || '未知来源';
    },
    
    // 分页相关
    handlePageChange(page) {
      this.currentPage = page;
    },
    
    onShowSizeChange(current, size) {
      this.pageSize = size;
      this.currentPage = 1;
    },
    
    // 搜索功能
    handleSearch() {
      this.currentPage = 1;
    },
    
    // 导出功能
    exportToJson() {
      // 创建一个Blob对象
      const dataStr = JSON.stringify(this.originalQuestions, null, 2);
      const blob = new Blob([dataStr], { type: 'application/json' });
      const url = URL.createObjectURL(blob);
      
      // 创建一个a标签用于下载
      const a = document.createElement('a');
      a.href = url;
      a.download = `questions_${new Date().toISOString().split('T')[0]}.json`;
      document.body.appendChild(a);
      a.click();
      
      // 清理
      setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      }, 0);
      
      this.$message.success('成功导出为JSON文件');
    },
    
    exportToExcel() {
      this.isGenerating = true;
      
      try {
        fetch('http://localhost:5000/api/questions/export-excel', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            data: this.originalQuestions
          })
        })
        .then(response => {
          if (response.ok) {
            return response.blob();
          }
          throw new Error('导出失败');
        })
        .then(blob => {
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `questions_${new Date().toISOString().split('T')[0]}.xlsx`;
          document.body.appendChild(a);
          a.click();
          
          // 清理
          setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
          }, 0);
          
          this.$message.success('成功导出为Excel文件');
        })
        .catch(error => {
          console.error('导出Excel失败:', error);
          this.$message.error('导出Excel失败，请重试');
        })
        .finally(() => {
          this.isGenerating = false;
        });
      } catch (error) {
        console.error('导出Excel失败:', error);
        this.$message.error('导出Excel失败，请重试');
        this.isGenerating = false;
      }
    }
  }
};
</script>

<style scoped>
.question-generate-container {
  padding-top: 104px;
}

/* 控制面板样式 */
.control-panel {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  height: 100%;
}

.card-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
}

.card-header h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #1f2937;
}

.header-line {
  width: 40px;
  height: 3px;
  background: #1890ff;
  border-radius: 3px;
}

.form-item {
  margin-bottom: 24px;
}

.form-label {
  font-weight: 500;
  color: #4b5563;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
}

.icon-wrapper {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  margin-right: 8px;
  color: #1890ff;
}

.slider-value {
  text-align: right;
  font-size: 14px;
  color: #6b7280;
  margin-top: 8px;
}

.data-source-group {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

.domain-select {
  width: 100%;
}

.generate-btn {
  height: 44px;
  margin-top: 12px;
  margin-bottom: 12px;
  font-weight: 600;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-content {
  display: flex;
  align-items: center;
  gap: 8px;
}

.export-options {
  margin-top: 24px;
  padding-top: 24px;
  border-top: 1px dashed #e5e7eb;
}

.export-btn {
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.export-icon {
  margin-right: 8px;
}

.mb-10 {
  margin-bottom: 10px;
}

.mb-15 {
  margin-bottom: 15px;
}

.mb-24 {
  margin-bottom: 24px !important;
}

/* 统计卡片样式 */
.stats-cards {
  margin-top: 24px;
}

.widget-1 {
  position: relative;
  overflow: hidden;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  height: 100%;
}

.widget-1 .icon {
  position: absolute;
  right: 16px;
  top: 16px;
  opacity: 0.5;
}

.widget-1-blue {
  background: linear-gradient(135deg, #e6f7ff 0%, #e6f7ff 100%);
}

.widget-1-purple {
  background: linear-gradient(135deg, #f9f0ff 0%, #f9f0ff 100%);
}

.widget-1-green {
  background: linear-gradient(135deg, #f6ffed 0%, #f6ffed 100%);
}

.text-primary {
  color: #1890ff;
}

.text-purple {
  color: #722ed1;
}

.text-success {
  color: #52c41a;
}

/* 题目展示区样式 */
.questions-display {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  min-height: 600px;
}

.filter-toolbar {
  margin-bottom: 24px;
}

.search-input {
  width: 100%;
}

.questions-list {
  margin-top: 24px;
}

/* 问题面板样式 */
.question-panel {
  margin-bottom: 16px;
  border-radius: 8px;
  overflow: hidden;
}

.question-content {
  padding: 8px 0;
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 16px;
}

.question-prompt,
.question-options,
.question-answer,
.question-explanation {
  margin-bottom: 16px;
}

.label {
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 8px;
}

.content {
  color: #4b5563;
  line-height: 1.6;
}

.answer-content {
  font-weight: 500;
  color: #1890ff;
}

.options-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  padding: 8px 12px;
  background: #f9fafb;
  border-radius: 6px;
  transition: all 0.3s;
}

.option-selected {
  background: #e6f7ff;
  border-left: 3px solid #1890ff;
}

.option-letter {
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #1890ff;
  color: white;
  border-radius: 50%;
  font-weight: 600;
  margin-right: 12px;
  flex-shrink: 0;
}

.option-text {
  line-height: 1.5;
}

/* 分页样式 */
.pagination-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 32px;
  padding-top: 24px;
  border-top: 1px solid #f3f4f6;
}

.pagination-info {
  margin-top: 12px;
  color: #6b7280;
  font-size: 14px;
}

/* 空状态样式 */
.empty-state {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

/* 响应式调整 */
@media (max-width: 992px) {
  .control-panel {
    margin-bottom: 24px;
  }
}

.tip-text {
  color: #8c8c8c;
  font-size: 14px;
  margin-top: 4px;
}
</style> 