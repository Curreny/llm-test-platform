<template>
  <div class="question-generate-container">
    <!-- 页面标题部分 -->
    <a-row :gutter="24" class="mb-24">
      <a-col :span="24">
        <a-card :bordered="false" class="header-card">
          <div class="card-header mb-15">
            <h2 class="font-bold">观测题库生成模块</h2>
          </div>
          <p class="problem-text">
            自动化生成大模型性能观测题库，支持多种题型和生成方式，提供500+高质量测试题目。
          </p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="24" class="mb-24">
      <!-- 左侧控制面板 -->
      <a-col :span="24" :lg="12" class="mb-24">
        <a-card :bordered="false" class="control-panel" style="height: 350px;">
          <div class="card-header mb-15">
            <h3 class="font-bold">题库生成设置</h3>
          </div>
          
          <!-- 题目类型选择 -->
          <div class="form-item">
            <div class="form-label">
              <span class="icon-wrapper">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </span>
              题目类型及数量
            </div>
            <a-row :gutter="16">
              <a-col :span="8" :lg="8" :md="8" :sm="24" :xs="24">
                <div class="type-count-card">
                  <div class="type-card-header">
                    <a-checkbox class="type-checkbox" v-model="selectedTypes.single">选择题</a-checkbox>
                  </div>
                  <div class="type-card-content" v-if="selectedTypes.single">
                    <div class="count-input-group">
                      <span class="count-label">数量：</span>
                      <a-input-number 
                        v-model="typeCount.single" 
                        :min="1" 
                        :max="500"
                        class="count-input"
                      />
                      <span class="count-suffix">题</span>
                    </div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :lg="8" :md="8" :sm="24" :xs="24">
                <div class="type-count-card">
                  <div class="type-card-header">
                    <a-checkbox class="type-checkbox" v-model="selectedTypes.judge">判断题</a-checkbox>
                  </div>
                  <div class="type-card-content" v-if="selectedTypes.judge">
                    <div class="count-input-group">
                      <span class="count-label">数量：</span>
                      <a-input-number 
                        v-model="typeCount.judge" 
                        :min="1" 
                        :max="500"
                        class="count-input"
                      />
                      <span class="count-suffix">题</span>
                    </div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :lg="8" :md="8" :sm="24" :xs="24">
                <div class="type-count-card">
                  <div class="type-card-header">
                    <a-checkbox class="type-checkbox" v-model="selectedTypes.essay">问答题</a-checkbox>
                  </div>
                  <div class="type-card-content" v-if="selectedTypes.essay">
                    <div class="count-input-group">
                      <span class="count-label">数量：</span>
                      <a-input-number 
                        v-model="typeCount.essay" 
                        :min="1" 
                        :max="2000"
                        class="count-input"
                      />
                      <span class="count-suffix">题</span>
                    </div>
                  </div>
                </div>
              </a-col>
            </a-row>
            <div class="slider-value total-count-tip">总计: {{getTotalQuestionCount}}题</div>
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
          
        </a-card>
      </a-col>

      <!-- 右侧数据集统计卡片 -->
      <a-col :span="24" :lg="12" class="mb-24">
        <a-card :bordered="false" class="dataset-stats" style="height: 350px;">
          <div class="card-header mb-15">
            <h3 class="font-bold">题库数据集来源</h3>
          </div>

            <a-row :gutter="16">
              <a-col :span="8" :xs="12">
                <div class="dataset-item dataset-item-blue">
                  <div class="dataset-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#1890ff" aria-hidden="true">
                      <path d="M19 5v14H5V5h14m0-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2z"/>
                      <path d="M14 17H7v-2h7v2zm3-4H7v-2h10v2zm0-4H7V7h10v2z"/>
                    </svg>
                  </div>
                  <div class="dataset-info">
                    <div class="dataset-name">SafetyBench选择题</div>
                    <div class="dataset-tag"><a-tag color="blue">单选题</a-tag></div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :xs="12">
                <div class="dataset-item dataset-item-orange">
                  <div class="dataset-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#fa8c16" aria-hidden="true">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                      <path d="M9.29 16.29L5.7 12.7a.996.996 0 111.41-1.41L10 14.17l6.88-6.88a.996.996 0 111.41 1.41l-7.59 7.59a.996.996 0 01-1.41 0z"/>
                    </svg>
                  </div>
                  <div class="dataset-info">
                    <div class="dataset-name">SafetyBench判断题</div>
                    <div class="dataset-tag"><a-tag color="orange">判断题</a-tag></div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :xs="12">
                <div class="dataset-item dataset-item-purple">
                  <div class="dataset-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#722ed1" aria-hidden="true">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                      <path d="M12 17c.55 0 1-.45 1-1s-.45-1-1-1-1 .45-1 1 .45 1 1 1zm1-5h-2V7h2v5z"/>
                    </svg>
                  </div>
                  <div class="dataset-info">
                    <div class="dataset-name">100PoisonMpts</div>
                    <div class="dataset-tag"><a-tag color="purple">问答题</a-tag></div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :xs="12">
                <div class="dataset-item dataset-item-green">
                  <div class="dataset-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#52c41a" aria-hidden="true">
                      <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4z"/>
                      <path d="M10 17l-4-4 1.41-1.41L10 14.17l6.59-6.59L18 9l-8 8z" fill="#fff"/>
                    </svg>
                  </div>
                  <div class="dataset-info">
                    <div class="dataset-name">CValues-Comparison</div>
                    <div class="dataset-tag"><a-tag color="green">问答题</a-tag></div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :xs="12">
                <div class="dataset-item dataset-item-cyan">
                  <div class="dataset-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#13c2c2" aria-hidden="true">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
                    </svg>
                  </div>
                  <div class="dataset-info">
                    <div class="dataset-name">Instruction Attack</div>
                    <div class="dataset-tag"><a-tag color="cyan">问答题</a-tag></div>
                  </div>
                </div>
              </a-col>
              <a-col :span="8" :xs="12">
                <div class="dataset-item dataset-item-red">
                  <div class="dataset-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#f5222d" aria-hidden="true">
                      <path d="M11 15h2v2h-2v-2zm0-8h2v6h-2V7zm1-5C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8z"/>
                    </svg>
                  </div>
                  <div class="dataset-info">
                    <div class="dataset-name">Typical Safety</div>
                    <div class="dataset-tag"><a-tag color="red">问答题</a-tag></div>
                  </div>
                </div>
              </a-col>
            </a-row>
        </a-card>
      </a-col>

      <!-- 右侧题目展示区 -->
      <a-col :span="24" :lg="24">
        <a-card :bordered="false" class="questions-display">
          <div class="card-header mb-15">
            <h3 class="font-bold">大模型性能观测题库预览</h3>
          </div>
          
          <!-- 筛选工具栏 -->
          <div v-if="questions.length > 0" class="filter-toolbar mb-15">
            <a-row :gutter="16" type="flex" align="middle">
              <a-col :span="6">
                <a-input-search
                  placeholder="搜索题目关键词"
                  v-model="searchKeyword"
                  @search="handleSearch"
                  class="search-input"
                />
              </a-col>
              <a-col :span="6">
                <a-select v-model="filterType" style="width: 100%" placeholder="按题型筛选">
                  <a-select-option value="">全部题型</a-select-option>
                  <a-select-option value="single">选择题</a-select-option>
                  <a-select-option value="judge">判断题</a-select-option>
                  <a-select-option value="essay">问答题</a-select-option>
                </a-select>
              </a-col>
              <a-col :span="6">
                <a-select v-model="filterDomain" style="width: 100%" placeholder="按领域筛选">
                  <a-select-option value="">全部领域</a-select-option>
                  <a-select-option v-for="domain in domainStats" :key="domain.name" :value="domain.name">
                    {{domain.name}} ({{domain.count}})
                  </a-select-option>
                </a-select>
              </a-col>
              <a-col :span="6">
                <a-select v-model="filterSource" style="width: 100%" placeholder="按数据集来源筛选">
                  <a-select-option value="">全部来源</a-select-option>
                  <a-select-option v-for="source in sourceStats" :key="source.name" :value="source.name">
                    {{source.name}} ({{source.count}})
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
                    <a-tag color="blue">{{question.domain || '未分类'}}</a-tag>
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
              <div class="pagination-wrapper">
                <div class="pagination-left">
                  <a-pagination
                    v-model="currentPage"
                    :total="filteredQuestions.length"
                    :pageSize="pageSize"
                    @change="handlePageChange"
                    show-quick-jumper
                    show-size-changer
                    :pageSizeOptions="['10']"
                    @showSizeChange="onShowSizeChange"
                  />
                  <div class="pagination-info">
                    共 {{filteredQuestions.length}} 题，当前显示第 {{(currentPage-1)*pageSize+1}} - {{Math.min(currentPage*pageSize, filteredQuestions.length)}} 题
                  </div>
                </div>
                
                <!-- 清空题库按钮 -->
                <div class="pagination-right">
                  <a-button 
                    type="danger" 
                    @click="resetQuestions" 
                    class="reset-btn" 
                    size="small"
                    :disabled="isGenerating"
                  >
                    <svg viewBox="64 64 896 896" focusable="false" data-icon="delete" width="16" height="16" fill="currentColor" aria-hidden="true" class="export-icon">
                      <path d="M360 184h-8c4.4 0 8-3.6 8-8v8h304v-8c0 4.4 3.6 8 8 8h-8v72h72v-80c0-35.3-28.7-64-64-64H352c-35.3 0-64 28.7-64 64v80h72v-72zm504 72H160c-17.7 0-32 14.3-32 32v32c0 4.4 3.6 8 8 8h60.4l24.7 523c1.6 34.1 29.8 61 63.9 61h454c34.2 0 62.3-26.8 63.9-61l24.7-523H888c4.4 0 8-3.6 8-8v-32c0-17.7-14.3-32-32-32zM731.3 840H292.7l-24.2-512h487l-24.2 512z"></path>
                    </svg>
                    清空题库
                  </a-button>
                </div>
              </div>
            </div>
            
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
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="export-icon">
                      <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    导出观测题库为JSON
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
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="export-icon">
                      <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    导出观测题库为Excel
                  </a-button>
                </a-col>
              </a-row>
            </div>
          </div>
          <!-- 空状态 -->
          <div v-else class="empty-state">
            <div class="empty-content">
              <svg viewBox="64 64 896 896" focusable="false" data-icon="read" width="64" height="64" fill="#bfbfbf" aria-hidden="true">
                <path d="M928 161H699.2c-49.1 0-97.1 14.1-138.4 40.7L512 233l-48.8-31.3A255.2 255.2 0 00324.8 161H96c-17.7 0-32 14.3-32 32v568c0 17.7 14.3 32 32 32h228.8c49.1 0 97.1 14.1 138.4 40.7l44.4 28.6c1.3.8 2.8 1.3 4.3 1.3s3-.4 4.3-1.3l44.4-28.6C602 807.1 650.1 793 699.2 793H928c17.7 0 32-14.3 32-32V193c0-17.7-14.3-32-32-32zM324.8 721H136V233h188.8c35.4 0 69.8 10.1 99.5 29.2l48.8 31.3 6.9 4.5v462c-47.6-25.6-100.8-39-155.2-39zm563.2 0H699.2c-54.4 0-107.6 13.4-155.2 39V298l6.9-4.5 48.8-31.3c29.7-19.1 64.1-29.2 99.5-29.2H888v488zM396.9 361H211.1c-3.9 0-7.1 3.4-7.1 7.5v45c0 4.1 3.2 7.5 7.1 7.5h185.7c3.9 0 7.1-3.4 7.1-7.5v-45c.1-4.1-3.1-7.5-7-7.5zm223.1 7.5v45c0 4.1 3.2 7.5 7.1 7.5h185.7c3.9 0 7.1-3.4 7.1-7.5v-45c0-4.1-3.2-7.5-7.1-7.5H627.1c-3.9 0-7.1 3.4-7.1 7.5zM396.9 501H211.1c-3.9 0-7.1 3.4-7.1 7.5v45c0 4.1 3.2 7.5 7.1 7.5h185.7c3.9 0 7.1-3.4 7.1-7.5v-45c.1-4.1-3.1-7.5-7-7.5zm416 0H627.1c-3.9 0-7.1 3.4-7.1 7.5v45c0 4.1 3.2 7.5 7.1 7.5h185.7c3.9 0 7.1-3.4 7.1-7.5v-45c.1-4.1-3.1-7.5-7-7.5z"></path>
              </svg>
              <p class="empty-text">暂无生成的题目<br/>请点击上方「生成题库」按钮开始生成</p>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "QuestionGenerate",
  components: {},
  data() {
    return {
      // 生成设置
      selectedTypes: {
        single: true,
        judge: true,
        essay: true
      },
      typeCount: {
        single: 200,
        judge: 100,
        essay: 200
      },
      
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
      filterSource: '',
      
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
        result = result.filter(q => q.domain === this.filterDomain);
      }
      
      // 按数据集来源筛选
      if (this.filterSource) {
        result = result.filter(q => q.source === this.filterSource);
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
        const domain = q.domain || '未分类';
        domains[domain] = (domains[domain] || 0) + 1;
      });
      
      return Object.keys(domains).map(name => ({
        name,
        count: domains[name]
      })).sort((a, b) => b.count - a.count);
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
    getTotalQuestionCount() {
      let total = 0;
      if (this.selectedTypes.single) total += this.typeCount.single;
      if (this.selectedTypes.judge) total += this.typeCount.judge;
      if (this.selectedTypes.essay) total += this.typeCount.essay;
      return total;
    },
    sourceStats() {
      const sources = {};
      this.questions.forEach(q => {
        const source = q.source;
        sources[source] = (sources[source] || 0) + 1;
      });
      
      return Object.keys(sources).map(name => ({
        name,
        count: sources[name]
      })).sort((a, b) => b.count - a.count);
    }
  },
  created() {
    // 组件创建时，从会话存储中加载题库
    this.loadSessionData();
  },
  methods: {
    // 从会话存储中加载数据
    loadSessionData() {
      try {
        const sessionData = sessionStorage.getItem('questionBank');
        if (sessionData) {
          this.questions = JSON.parse(sessionData);
          this.originalQuestions = [...this.questions];
          console.log(`已从会话中恢复${this.questions.length}道题目`);
        } 
      } catch (error) {
        console.error('从会话加载数据失败:', error);
      }
    },
    
    // 生成题目
    async generateQuestions() {
      if (!this.selectedTypes.single && !this.selectedTypes.judge && !this.selectedTypes.essay) {
        this.$message.error('请至少选择一种题目类型');
        return;
      }
      
      if (this.getTotalQuestionCount === 0) {
        this.$message.error('题目总数不能为0');
        return;
      }
      
      this.isGenerating = true;
      
      try {
        const typesRequest = [];
        if (this.selectedTypes.single) {
          typesRequest.push({
            type: 'single',
            count: this.typeCount.single
          });
        }
        if (this.selectedTypes.judge) {
          typesRequest.push({
            type: 'judge',
            count: this.typeCount.judge
          });
        }
        if (this.selectedTypes.essay) {
          typesRequest.push({
            type: 'essay',
            count: this.typeCount.essay
          });
        }
        
        const response = await fetch('http://starvii.tpddns.cn:9004/api/questions/generate', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            typesRequest: typesRequest,
            domains: this.selectedDomains,
          })
        });
        
        const result = await response.json();
        
        if (result.success) {
          this.questions = result.data;
          this.originalQuestions = [...this.questions];
          
          // 将新生成的题目保存到会话存储
          sessionStorage.setItem('questionBank', JSON.stringify(this.questions));
          
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
        'judge': '判断题',
        'essay': '问答题',
        'unknown': '未知类型'
      };
      
      return typeNames[type] || '未知类型';
    },
    
    // 获取题型颜色
    getTypeColor(type) {
      const typeColors = {
        'single': 'blue',
        'judge': 'orange',
        'essay': 'purple',
        'unknown': 'default'
      };
      
      return typeColors[type] || 'default';
    },
    
    // 获取来源名称
    getSourceName(source) {
      const sourceNames = {
        '100PoisonMpts': '100PoisonMpts',
        'CValues-Comparison': 'CValues-Comparison',
        'instruction_attack': 'instruction_attack',
        'SafetyBench_choice': 'SafetyBench_choice',
        'SafetyBench_judge': 'SafetyBench_judge',
        'typical_safety': 'typical_safety'
      };
      
      return sourceNames[source];
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
    async exportQuestions(format) {
      this.isGenerating = true;
      try {
        const response = await fetch(`http://starvii.tpddns.cn:9004/api/questions/export-${format}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            data: this.originalQuestions
          })
        });

        if (!response.ok) throw new Error('导出失败');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;

        // 使用与后端一致的命名格式：题库_年月日_时分秒
        const now = new Date();
        const formatter = (num) => num.toString().padStart(2, '0');
        const timestamp = `${now.getFullYear()}${formatter(now.getMonth() + 1)}${formatter(now.getDate())}_${formatter(now.getHours())}${formatter(now.getMinutes())}${formatter(now.getSeconds())}`;
        a.download = `题库_${timestamp}.${format}`;
        document.body.appendChild(a);
        a.click();

        // 清理
        setTimeout(() => {
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        }, 0);

        this.$message.success(`成功导出为${format.toUpperCase()}文件`);
      } catch (error) {
        console.error(`导出${format.toUpperCase()}失败:`, error);
        this.$message.error(`导出${format.toUpperCase()}失败，请重试`);
      } finally {
        this.isGenerating = false;
      }
    },
    exportToJson() {
      this.exportQuestions('json');
    },
    exportToExcel() {
      this.exportQuestions('xlsx');
    },
    resetQuestions() {
      this.$confirm({
        title: '确认清空题库',
        content: '清空操作将会移除所有已生成的题目，确定要继续吗？',
        okText: '确认清空',
        okType: 'danger',
        cancelText: '取消',
        onOk: async () => {
          try {
            // 调用API清空题库
            const response = await axios.post('http://starvii.tpddns.cn:9004/api/questions/clear-bank');
            
            if (response.data.success) {
              // 重置所有相关状态
              this.selectedTypes = {
                single: true,
                judge: true,
                essay: true
              };
              this.typeCount = {
                single: 200,
                judge: 100,
                essay: 200
              };
              this.selectedDomains = [];
              this.questions = [];
              this.originalQuestions = [];
              this.currentPage = 1;
              this.pageSize = 10;
              this.searchKeyword = '';
              this.filterType = '';
              this.filterDomain = '';
              this.filterSource = '';
              
              // 从会话存储中清除题库数据
              sessionStorage.removeItem('questionBank');
              
              this.$message.success('题库已清空');
            } else {
              this.$message.error(response.data.message || '清空题库失败');
            }
          } catch (error) {
            console.error('清空题库失败:', error);
            this.$message.error('清空题库失败，请重试');
          }
        }
      });
    },
    // 添加主题示例
    addTopicExample(example) {
      if (!this.selectedTopics.includes(example)) {
        this.selectedTopics.push(example);
      }
    }
  }
};
</script>

<style scoped>
.question-generate-container {
  padding: 10px;
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
  text-align: center;
}

.header-line {
  width: 40px;
  height: 3px;
  background: #1890ff;
  border-radius: 3px;
}

.form-item {
  margin-bottom: 0px;
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
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 15px;
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
  position: relative;
}

.pagination-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
}

.pagination-left {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.pagination-right {
  position: absolute;
  right: 10px;
  top: 20px;
}

.reset-btn {
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
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

.empty-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px;
}

.empty-text {
  margin-top: 24px;
  color: #8c8c8c;
  font-size: 16px;
  text-align: center;
  line-height: 1.6;
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

.type-count-item {
  align-items: center;
  justify-content: space-between;
  margin-bottom: 16px;
}

.total-count-tip {
  font-weight: 500;
  color: #1890ff;
}

/* 数据集统计卡片样式 */
.dataset-stats {
  background-color: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  height: 100%;
}

.dataset-wrapper {
  background-color: #ffffff;
  border-radius: 8px;
  padding: 16px;
}

.dataset-item {
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 16px;
  background: #f9fafb;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
  box-shadow: 0 3px 8px rgba(0, 0, 0, 0.08);
}

.dataset-item:hover {
  transform: translateY(-7px);

}

.dataset-icon {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  margin-right: 12px;
  transition: transform 0.3s ease;
  background-color: rgba(255, 255, 255, 0.6);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.dataset-item:hover .dataset-icon {
  transform: scale(1.1);
}

.dataset-info {
  flex: 1;
}

.dataset-name {
  font-weight: 500;
  margin-bottom: 4px;
  font-size: 15px;
  color: #262626;
  line-height: 1.4;
  letter-spacing: 0.2px;
}

.dataset-tag {
  margin-top: 4px;
}

.dataset-tag .ant-tag {
  border-radius: 4px;
  font-size: 12px;
  padding: 0 6px;
  height: 22px;
  line-height: 22px;
  margin-right: 0;
}

.dataset-item-blue {
  background-color: #f0f5ff;
  border-color: #d6e4ff;
}

.dataset-item-orange {
  background-color: #fff7e8;
  border-color: #ffd8bf;
}

.dataset-item-purple {
  background-color: #f9f0ff;
  border-color: #efdbff;
}

.dataset-item-green {
  background-color: #f6ffed;
  border-color: #d9f7be;
}

.dataset-item-cyan {
  background-color: #e6fffb;
  border-color: #b5f5ec;
}

.dataset-item-red {
  background-color: #fff2f0;
  border-color: #ffccc7;
}

.mt-15 {
  margin-top: 15px !important;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .pagination-right {
    position: static;
    margin-top: 10px;
  }
  
  .pagination-wrapper {
    flex-direction: column;
  }
}

/* 题目类型卡片样式 */
.type-count-card {
  background: #fff;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border-left: 3px solid transparent;
  height: 100%;
}

.type-count-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.type-card-header {
  display: flex;
  align-items: center;
  margin-bottom: 12px;
  justify-content: center;
}

.type-icon {
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 6px;
  margin-right: 12px;
  transition: all 0.3s ease;
}

.type-icon-blue {
  background-color: rgba(24, 144, 255, 0.1);
  color: #1890ff;
}

.type-icon-orange {
  background-color: rgba(250, 140, 22, 0.1);
  color: #fa8c16;
}

.type-icon-purple {
  background-color: rgba(114, 46, 209, 0.1);
  color: #722ed1;
}

.type-checkbox {
  font-size: 16px;
  font-weight: 500;
  text-align: center; 
}

.type-card-content {
  padding-top: 12px;
  margin-top: 12px;
  border-top: 1px dashed rgba(0, 0, 0, 0.06);
}

.count-input-group {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.count-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
  margin-right: 8px;
}

.count-input {
  flex: 1;
  width: 100% !important;
}

.count-suffix {
  margin-left: 8px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.count-tips {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  margin-top: 8px;
  line-height: 1.5;
}

.count-summary {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  margin-top: 16px;
  padding: 12px 16px;
  background-color: rgba(24, 144, 255, 0.05);
  border-radius: 8px;
  border: 1px dashed rgba(24, 144, 255, 0.3);
}

.count-summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.total-count-tip {
  font-weight: 600;
  color: #1890ff;
  font-size: 16px;
}

.total-time-tip {
  font-weight: 500;
  color: #52c41a;
  font-size: 14px;
}

@media (max-width: 768px) {
  .count-summary {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
  
  .count-input-group {
    flex-wrap: wrap;
  }
  
  .count-label {
    width: 100%;
    margin-bottom: 4px;
  }
}

</style>