<template>
    <div class="question-expansion-container">
      <!-- 页面标题部分 -->
      <a-row :gutter="24" class="mb-24">
        <a-col :span="24">
          <a-card :bordered="false" class="header-card">
            <div class="card-header mb-15">
              <h2 class="font-bold">观测题库扩展模块</h2>
            </div>
            <p class="problem-text">
              自动化拓展测试题库，支持多种变形方式，有效性不低于90%。
            </p>
          </a-card>
        </a-col>
      </a-row>
  
      <a-row :gutter="24" class="mb-24">
        <!-- 左侧控制面板 -->
        <a-col :span="24" :lg="12" class="mb-24">
          <a-card :bordered="false" class="control-panel" style="height: 350px;">
            <div class="card-header mb-15">
              <h3 class="font-bold">题库扩展设置</h3>
            </div>
            
            <!-- 导入题目按钮 -->
            <a-button 
              type="dashed" 
              block 
              @click="openImportDialog" 
              class="import-btn mb-15"
              :disabled="isTransforming"
            >
              <span class="btn-content">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M7 10L12 15M12 15L17 10M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                导入题库 
                <span v-if="originalQuestions.length > 0" class="count-indicator">
                  {{originalQuestions.length}} 题
                </span>
              </span>
            </a-button>
            
            <!-- 变形方式选择 -->
            <div class="form-item">
              <div class="form-label">
                <span class="icon-wrapper">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M8 3V5M16 3V5M7 21H17C19.2091 21 21 19.2091 21 17V9C21 6.79086 19.2091 5 17 5H7C4.79086 5 3 6.79086 3 9V17C3 19.2091 4.79086 21 7 21Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </span>
                变形方式选择（可任意多选方式）
              </div>
              <a-checkbox-group v-model="selectedTransformations" class="transform-checkbox-group">
                <div class="transform-checkbox">
                  <a-checkbox value="语序变换">语序变换</a-checkbox>
                </div>
                <div class="transform-checkbox">
                  <a-checkbox value="同义词替换">同义词替换</a-checkbox>
                </div>
                <div class="transform-checkbox">
                  <a-checkbox value="选项扰动">选项扰动</a-checkbox>
                </div>
                <div class="transform-checkbox">
                  <a-checkbox value="上下文调整">上下文调整</a-checkbox>
                </div>
                <div class="transform-checkbox">
                  <a-checkbox value="情感立场转换">情感立场转换</a-checkbox>
                </div>
                <div class="transform-checkbox">
                  <a-checkbox value="噪声注入">噪声注入</a-checkbox>
                </div>
              </a-checkbox-group>
            </div>
            
            <!-- 生成按钮 -->
            <a-button 
              type="primary" 
              size="large" 
              block 
              @click="transformQuestions" 
              :loading="isTransforming"
              class="generate-btn"
            >
              <span class="btn-content">
                <svg v-if="!isTransforming" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M17 1L21 5M21 5L17 9M21 5H7C4.79086 5 3 6.79086 3 9V9M7 23L3 19M3 19L7 15M3 19H17C19.2091 19 21 17.2091 21 15V15" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                {{ isTransforming ? '正在变换中...' : '开始变换' }}
              </span>
            </a-button>
          
            
          </a-card>
        </a-col>
  
        <!-- 右侧变形方式卡片 -->
        <a-col :span="24" :lg="12" class="mb-24">
          <a-card :bordered="false" class="transform-methods" style="height:350px;">
            <div class="card-header mb-15">
              <h3 class="font-bold">变形方式说明</h3>
            </div>
  
            <a-row :gutter="16">
              <a-col :span="12" :xs="12">
                <div class="transform-item transform-item-blue">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#1890ff" aria-hidden="true">
                      <path d="M19 20H5V4h7V2H5c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 2l5 5h-5V2zm3 12v-2h-4v-2h4V8l4 4-4 4z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">语序变换</div>
                    <div class="transform-desc">保持含义不变，重新调整语句结构</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="12">
                <div class="transform-item transform-item-orange">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#fa8c16" aria-hidden="true">
                      <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 13h2v4H7zm4-6h2v10h-2zm4 3h2v7h-2z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">同义词替换</div>
                    <div class="transform-desc">用同义词替换关键词，保持含义</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="12">
                <div class="transform-item transform-item-purple">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#722ed1" aria-hidden="true">
                      <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">选项扰动</div>
                    <div class="transform-desc">调整选项表述，增强干扰性</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="12">
                <div class="transform-item transform-item-green">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#52c41a" aria-hidden="true">
                      <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">上下文调整</div>
                    <div class="transform-desc">添加相关背景信息和上下文</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="12">
                <div class="transform-item transform-item-cyan">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#13c2c2" aria-hidden="true">
                      <path d="M4 11h6v2H4zm0 4h6v2H4zm0-8h6v2H4zm9 0h7v10h-7zm2 2v6h3v-6z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">情感立场转换</div>
                    <div class="transform-desc">调整题目情感色彩和立场</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="12">
                <div class="transform-item transform-item-red">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#f5222d" aria-hidden="true">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4.59-12.42L10 14.17l-2.59-2.58L6 13l4 4 8-8z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">噪声注入</div>
                    <div class="transform-desc">增加适当噪声，保持核心语义</div>
                  </div>
                </div>
              </a-col>
            </a-row>
          </a-card>
        </a-col>
  
        <!-- 变形进度展示 -->
        <a-col :span="24" v-if="isTransforming">
            <a-card :bordered="false" class="progress-card mb-24">
                <div class="progress-header">
                <h3>正在变形题目 {{transformationProgress}}/{{originalQuestions.length}}</h3>
                </div>
                <a-progress :percent="transformProgressPercentage" status="active" />
                <div class="progress-info" v-if="transformingQuestionIndex >= 0">
                <p class="current-question">
                    <span class="question-label">当前题目：</span>
                    <span class="question-content">{{transformingQuestionIndex >= 0 && originalQuestions[transformingQuestionIndex] && originalQuestions[transformingQuestionIndex].prompt || ''}}</span>
                </p>
                <p class="current-method">
                    <span class="method-label">变形方法：</span>
                    <span class="method-content">{{currentTransformMethod}}</span>
                </p>
                </div>
            </a-card>
        </a-col>
  
        <!-- 变形统计卡片 -->
        <a-col :span="24" :lg="24" v-if="transformedQuestions.length > 0 && !isTransforming" class="mb-24">
          <a-row :gutter="24">
            <a-col :span="24" :lg="8" class="mb-24">
              <WidgetCounter
                title="题目数量"
                :value="stats.totalQuestions"
                :precision="0"
                suffix="+"
                icon="<svg width='22' height='22' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M17 1L21 5M21 5L17 9M21 5H7C4.79086 5 3 6.79086 3 9V9M7 23L3 19M3 19L7 15M3 19H17C19.2091 19 21 17.2091 21 15V15' stroke='#ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>"
                status="success"
              ></WidgetCounter>
            </a-col>
            <a-col :span="24" :lg="8" class="mb-24">
              <WidgetCounter
                title="有效变形题目"
                :value="stats.validCount"
                :precision="0"
                icon="<svg width='22' height='22' viewBox='0 0 24 24' fill='none' xmlns='http://www.w3.org/2000/svg'><path d='M9 6C9 7.65685 7.65685 9 6 9C4.34315 9 3 7.65685 3 6C3 4.34315 4.34315 3 6 3C7.65685 3 9 4.34315 9 6Z' stroke='#ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/><path d='M17 6C17 7.65685 15.6569 9 14 9C12.3431 9 11 7.65685 11 6C11 4.34315 12.3431 3 14 3C15.6569 3 17 4.34315 17 6Z' stroke='#ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/><path d='M12.9291 17C12.9758 16.6734 13 16.3395 13 16C13 14.3648 12.4393 12.8606 11.4998 11.6691C12.2352 11.2435 13.0892 11 14 11C16.7614 11 19 13.2386 19 16V17H12.9291Z' stroke='#ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/><path d='M6 11C8.76142 11 11 13.2386 11 16V17H1V16C1 13.2386 3.23858 11 6 11Z' stroke='#ffffff' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'/></svg>"
                status="purple"
              ></WidgetCounter>
            </a-col>
            <a-col :span="24" :lg="8" class="mb-24">
              <WidgetCounter
                title="有效性评分"
                :value="effectivenessPercentage"
                :precision="1"
                suffix="%"
                icon="<svg width='22' height='22' viewBox='0 0 20 20' fill='none' xmlns='http://www.w3.org/2000/svg'><path fill-rule='evenodd' clip-rule='evenodd' d='M10 18C14.4183 18 18 14.4183 18 10C18 5.58172 14.4183 2 10 2C5.58172 2 2 5.58172 2 10C2 14.4183 5.58172 18 10 18ZM13.7071 8.70711C14.0976 8.31658 14.0976 7.68342 13.7071 7.29289C13.3166 6.90237 12.6834 6.90237 12.2929 7.29289L9 10.5858L7.70711 9.29289C7.31658 8.90237 6.68342 8.90237 6.29289 9.29289C5.90237 9.68342 5.90237 10.3166 6.29289 10.7071L8.29289 12.7071C8.68342 13.0976 9.31658 13.0976 9.70711 12.7071L13.7071 8.70711Z' fill='#52C41A'/></svg>"
                :status="effectivenessPercentage >= 90 ? 'success' : 'warning'"
              ></WidgetCounter>
            </a-col>
          </a-row>
        </a-col>
        
  
        <!-- 题目变形展示区 -->
        <a-col :span="24" :lg="24">
          <a-card :bordered="false" class="questions-display">
            <div class="card-header mb-15">
              <h3 class="font-bold">题目变形预览</h3>
            </div>
            

            
            <!-- 有变形结果时显示 -->
            <div v-if="transformedQuestions.length > 0 && !isTransforming">
              <!-- 筛选工具栏 -->
              <div class="filter-toolbar mb-15">
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
              <div class="questions-list">
                <a-collapse accordion :bordered="false">
                  <a-collapse-panel 
                    v-for="(item, index) in paginatedTransformedQuestions" 
                    :key="index" 
                    :header="`题目 ${(currentPage - 1) * pageSize + index + 1}: ${item.prompt ? (item.prompt.length > 50 ? item.prompt.substring(0, 50) + '...' : item.prompt) : '无标题'}`"
                    class="question-panel"
                  >
                    <!-- 标题栏 -->
                    <div class="question-header">
                      <div class="question-tags">
                        <a-tag :color="getTypeColor(item.type)">{{getTypeName(item.type)}}</a-tag>
                        <a-tag color="blue">{{item.domain || '未分类'}}</a-tag>
                        <a-tag color="purple">{{getSourceName(item.source)}}</a-tag>
                        <a-tag color="green">ID: {{item.id}}</a-tag>
                      </div>
                    </div>
                    
                    <!-- 原始题目和变形题目对比 -->
                    <a-row :gutter="24">
                      <a-col :span="12">
                        <div class="original-question-section">
                          <div class="section-title">原始题目
                            <a-tag :color="getTransformationColor(item.transformationType)">
                              {{item.transformationType}}
                            </a-tag>
                            <a-tag :color="item.is_valid ? 'green' : 'red'">
                              {{item.is_valid ? '有效' : '无效'}} ({{Math.round((item.similarity_score || 0) * 100)}}%)
                            </a-tag>
                          </div>
                          <div class="question-content">
                            <div class="question-prompt">
                              <div class="label">题目描述:</div>
                              <div class="content">{{item.original.prompt}}</div>
                            </div>
                            
                            <!-- 选择题选项 -->
                            <div v-if="(item.original.type === 'single' || item.original.type === 'judge') && item.original.options" class="question-options">
                              <div class="label">选项:</div>
                              <div class="options-list">
                                <div 
                                  v-for="(option, optIndex) in item.original.options" 
                                  :key="optIndex" 
                                  class="option-item"
                                  :class="{'option-selected': item.original.answer === optionLetters[optIndex]}"
                                >
                                  <span class="option-letter">{{optionLetters[optIndex]}}</span>
                                  <span class="option-text">{{option}}</span>
                                </div>
                              </div>
                            </div>
                            
                            <!-- 答案 -->
                            <div class="question-answer">
                              <div class="label">答案:</div>
                              <div class="answer-content">{{item.original.answer}}</div>
                            </div>
                          </div>
                        </div>
                      </a-col>
                      
                      <a-col :span="12">
                        <div class="transformed-question-section">
                          <div class="section-title">变形后题目</div>
                          <div class="question-content">
                            <div class="question-prompt">
                              <div class="label">题目描述:</div>
                              <div class="content">{{item.prompt}}</div>
                            </div>
                            
                            <!-- 选择题选项 -->
                            <div v-if="(item.type === 'single' || item.type === 'judge') && item.options" class="question-options">
                              <div class="label">选项:</div>
                              <div class="options-list">
                                <div 
                                  v-for="(option, optIndex) in item.options" 
                                  :key="optIndex" 
                                  class="option-item"
                                  :class="{'option-selected': item.answer === optionLetters[optIndex]}"
                                >
                                  <span class="option-letter">{{optionLetters[optIndex]}}</span>
                                  <span class="option-text">{{option}}</span>
                                </div>
                              </div>
                            </div>
                            
                            <!-- 答案 -->
                            <div class="question-answer">
                              <div class="label">答案:</div>
                              <div class="answer-content">{{item.answer}}</div>
                            </div>
                          </div>
                        </div>
                      </a-col>
                    </a-row>
                  </a-collapse-panel>
                </a-collapse>
              </div>
              
              <!-- 分页组件 -->
              <div class="pagination-container">
                <div class="pagination-wrapper">
                  <div class="pagination-left">
                    <a-pagination 
                      v-model="currentPage" 
                      :total="filteredTransformedQuestions.length" 
                      :pageSize="pageSize"
                      @change="handlePageChange"
                      show-quick-jumper
                      show-size-changer
                      :pageSizeOptions="['5', '10', '20', '50']"
                      @showSizeChange="onShowSizeChange"
                    />
                    <div class="pagination-info">
                      共 {{filteredTransformedQuestions.length}} 题，当前显示第 {{(currentPage-1)*pageSize+1}} - {{Math.min(currentPage*pageSize, filteredTransformedQuestions.length)}} 题
                    </div>
                  </div>
                  
                  <!-- 清空题库按钮 -->
                  <div class="pagination-right">
                    <a-button 
                      type="danger" 
                      @click="clearTransformedQuestions" 
                      class="reset-btn" 
                      size="small"
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
              <div class="export-options" v-if="transformedQuestions.length > 0">
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
                      :disabled="isTransforming"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="export-icon">
                        <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      导出拓展题库为JSON
                    </a-button>
                  </a-col>
                  <a-col :span="12">
                    <a-button 
                      type="default" 
                      block 
                      @click="exportToExcel" 
                      class="export-btn"
                      :disabled="isTransforming"
                    >
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="export-icon">
                        <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M7 10L12 15L17 10" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      </svg>
                      导出拓展题库为Excel
                    </a-button>
                  </a-col>
                </a-row>
              </div>
            </div>  
            <!-- 空状态 -->
            <div v-else-if="!isTransforming" class="empty-state">
              <div class="empty-content">
                <svg viewBox="0 0 24 24" width="64" height="64" fill="#bfbfbf" aria-hidden="true">
                  <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 2h4v2h-4V5zm-6 6h4v2H6v-2zm10 8H8v-2h8v2zm0-4H8v-2h8v2zm-4-6H6V7h6v2z"/>
                </svg>
                <p class="empty-text">
                  暂无变形后的题目<br/>
                  请先<a href="#" @click.prevent="openImportDialog">导入题库</a>，然后选择变形方式并点击「开始变换」按钮
                </p>
              </div>
            </div>
          </a-card>
        </a-col>
      </a-row>
      
      <!-- 导入题库对话框 -->
      <a-modal
        title="导入题库"
        :visible="importDialogVisible"
        :confirmLoading="isImporting"
        @ok="importQuestionsFromGenerate"
        @cancel="importDialogVisible = false"
        okText="开始导入"
        cancelText="取消"
      >
        <p>点击<span class="highlight-text">开始导入</span>从题库生成模块导入题目，将用于变形操作。</p>
        <p>您也可以返回<router-link to="/question-generate">题库生成模块</router-link>创建新的题库。</p>
      </a-modal>
    </div>
</template>
  
<script>
  import axios from 'axios';
  import WidgetCounter from '../components/Widgets/WidgetCounter';
  
  export default {
    name: 'QuestionExpansion',
    
    components: {
      WidgetCounter
    },
    
    data() {
      return {
        // 题目导入相关状态
        importDialogVisible: false,
        isImporting: false,
        
        // 变形相关状态
        isTransforming: false,
        selectedTransformations: ['语序变换', '同义词替换','选项扰动','上下文调整','情感立场转换','噪声注入'],
        transformationProgress: 0,
        transformingQuestionIndex: -1,
        currentTransformMethod: '',
        
        // 题目数据
        originalQuestions: [],
        transformedQuestions: [],
        
        // 分页相关
        currentPage: 1,
        pageSize: 10,
        
        // 新增的filterMethod和optionLetters
        filterMethod: '',
        optionLetters: ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'],
        
        // 筛选相关
        searchKeyword: '',
        filterType: '',
        filterDomain: '',
        filterSource: '',
      };
    },
    
    computed: {
      transformProgressPercentage() {
        if (this.originalQuestions.length === 0) return 0;
        return Math.round((this.transformationProgress / this.originalQuestions.length) * 100);
      },
      
      effectivenessPercentage() {
        if (this.transformedQuestions.length === 0) return 0;
        const validCount = this.transformedQuestions.filter(q => q.is_valid === true).length;
        return ((validCount / this.transformedQuestions.length) * 100).toFixed(1);
      },
      
      paginatedTransformedQuestions() {
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        return this.filteredTransformedQuestions.slice(startIndex, endIndex);
      },
      
      stats() {
        return {
          totalQuestions: this.originalQuestions.length,
          transformedCount: this.transformedQuestions.length,
          validCount: this.transformedQuestions.filter(q => q.is_valid === true).length
        };
      },
      
      filteredTransformedQuestions() {
        let result = [...this.transformedQuestions];
        
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
        
        // 按变形方式筛选
        if (this.filterMethod) {
          result = result.filter(q => q.transformationType === this.filterMethod);
        }
        
        return result;
      },
      
      domainStats() {
        const domains = {};
        this.transformedQuestions.forEach(q => {
          const domain = q.domain || '未分类';
          domains[domain] = (domains[domain] || 0) + 1;
        });
        
        return Object.keys(domains).map(name => ({
          name,
          count: domains[name]
        })).sort((a, b) => b.count - a.count);
      },
      
      sourceStats() {
        const sources = {};
        this.transformedQuestions.forEach(q => {
          const source = q.source;
          if (source) {
            sources[source] = (sources[source] || 0) + 1;
          }
        });
        
        return Object.keys(sources).map(name => ({
          name,
          count: sources[name]
        })).sort((a, b) => b.count - a.count);
      },
    },
    
    mounted() {
      // 页面加载时尝试获取已生成的题库
      this.checkExistingQuestions();
      
      // 获取已保存的变形题目
      this.fetchTransformedQuestions();
    },

    methods: {
      openImportDialog() {
        this.importDialogVisible = true;
      },
      
      async checkExistingQuestions() {
        try {
          const response = await axios.get('http://localhost:5000/api/questions/current-bank');
          if (response.data.success && response.data.data.length > 0) {
            this.originalQuestions = response.data.data;
            this.$message.info(`发现${this.originalQuestions.length}道已生成的题目`);
          }
        } catch (error) {
          console.error('检查已存在题目失败:', error);
        }
      },
      
      // 获取已保存的变形题目
      async fetchTransformedQuestions() {
        try {
          const response = await axios.get('http://localhost:5000/api/questions/get-transformed');
          if (response.data.success && response.data.data.length > 0) {
            this.transformedQuestions = response.data.data;
            console.log(`成功加载${this.transformedQuestions.length}道已保存的变形题目`);
          }
        } catch (error) {
          console.error('获取已保存变形题目失败:', error);
        }
      },
      
      // 保存变形题目到后端
      async saveTransformedQuestions() {
        if (this.transformedQuestions.length === 0) return;
        
        try {
          const response = await axios.post('http://localhost:5000/api/questions/save-transformed', {
            questions: this.transformedQuestions
          });
          
          if (response.data.success) {
            console.log(`成功保存${this.transformedQuestions.length}道变形题目`);
          }
        } catch (error) {
          console.error('保存变形题目失败:', error);
        }
      },
      
      // 清空变形题库
      async clearTransformedQuestions() {
        this.$confirm({
          title: '确定要清空变形题库吗?',
          content: '清空后将无法恢复，需要重新变形生成题目',
          okText: '确定',
          okType: 'danger',
          cancelText: '取消',
          onOk: async () => {
            try {
              const response = await axios.post('http://localhost:5000/api/questions/clear-transformed');
              if (response.data.success) {
                this.transformedQuestions = [];
                this.currentPage = 1;
                this.$message.success('已清空变形题库');
              }
            } catch (error) {
              console.error('清空变形题库失败:', error);
              this.$message.error('清空变形题库失败，请重试');
            }
          }
        });
      },
    
      
      async importQuestionsFromGenerate() {
        this.isImporting = true;
        try {
          // 通过API直接从后端获取已生成的题库
          const response = await axios.get('http://localhost:5000/api/questions/current-bank');
          
          if (response.data.success && response.data.data.length > 0) {
            this.originalQuestions = response.data.data;
            this.transformedQuestions = [];
            this.currentPage = 1;
            this.$message.success(`成功导入${this.originalQuestions.length}道题目`);
            this.importDialogVisible = false;
          } else {
            this.$message.warning('题库为空，请先在"题库生成"页面生成题目');
          }
        } catch (error) {
          console.error('导入题目失败:', error);
          this.$message.error('导入题目失败，请确保已生成题库');
        } finally {
          this.isImporting = false;
        }
      },
      
      async transformQuestions() {
        if (this.originalQuestions.length === 0) {
          // 如果没有题目，提示用户先导入题目
          this.openImportDialog();
          return;
        }
        
        if (this.selectedTransformations.length === 0) {
          // 如果没有选择变形方式，提示用户先选择变形方式
          this.$message.warning('请至少选择一种变形方式');
          return;
        }
        
        // 开始变形
        this.isTransforming = true;
        this.transformationProgress = 0;
        this.transformedQuestions = [];
        
        try {
          // 对每道题目，随机选择一种所选的变形方式
          const questionGroups = {}; // 按变形方式分组的题目
          
          // 初始化分组
          for (const method of this.selectedTransformations) {
            questionGroups[method] = [];
          }
          
          // 为每道题随机分配变形方式
          for (let i = 0; i < this.originalQuestions.length; i++) {
            this.transformingQuestionIndex = i;
            const question = this.originalQuestions[i];
            
            // 获取适合该题型的变形方式
            let availableMethods = [...this.selectedTransformations];
            
            // 如果不是单选题，不能使用选项扰动
            if (question.type !== 'single' && availableMethods.includes('选项扰动')) {
              availableMethods = availableMethods.filter(method => method !== '选项扰动');
            }
            
            // 如果没有适合的变形方式，跳过此题
            if (availableMethods.length === 0) continue;
            
            // 随机选择一种变形方式
            const randomMethod = availableMethods[Math.floor(Math.random() * availableMethods.length)];
            this.currentTransformMethod = randomMethod;
            
            // 将题目添加到对应的分组
            questionGroups[randomMethod].push(question);
          }
          
          // 对每种变形方式分组进行批量处理
          for (const method of this.selectedTransformations) {
            const questionsToTransform = questionGroups[method];
            
            // 如果该方法没有适用的题目，跳过
            if (questionsToTransform.length === 0) {
              continue;
            }
            
            this.currentTransformMethod = method;
            
            // 调用后端API进行变形
            const response = await axios.post('http://localhost:5000/api/questions/transform', {
              questions: questionsToTransform,
              method: method,
              evaluate_similarity: true,
              similarity_threshold: 0.8
            });
            
            // 打印响应数据，查看结构
            console.log(`${method}变形响应:`, JSON.stringify(response.data));
            
            if (response.data.success) {
              // 将变形后的题目添加到结果中
              const transformedData = response.data.data || [];
              
              console.log(`${method}变形数据:`, transformedData);
              
              if (!transformedData || transformedData.length === 0) {
                console.warn(`${method}变形返回空数据`);
                continue;
              }
              
              // 记录所有变形后的题目ID，方便调试
              console.log(`${method}变形题目IDs:`, transformedData.map(t => ({
                id: t.id || 'unknown',
                original_id: t.original_id || 'unknown',
                similarity: t.similarity_score
              })));
              
              // 为每个变形后的题目添加原始题目和变形方式信息
              for (const transformed of transformedData) {
                try {
                  // 确保transformed是对象
                  if (!transformed || typeof transformed !== 'object') {
                    console.warn('变形结果不是对象:', transformed);
                    continue;
                  }
                  
                  // 尝试找到对应的原题
                  let originalQuestion = null;
                  
                  if (transformed.original_id) {
                    // 如果有original_id，尝试通过ID匹配
                    const originalId = String(transformed.original_id).replace('q', '');
                    console.log('尝试匹配题目:', {
                      original_id: transformed.original_id,
                      formatted_id: originalId,
                      matching_ids: this.originalQuestions.map(q => q.id)
                    });
                    originalQuestion = this.originalQuestions.find(q => q.id === `q${originalId}` || q.id === originalId);
                    
                    // 如果找不到，尝试直接使用数字ID
                    if (!originalQuestion && !isNaN(Number(transformed.original_id))) {
                      const numericId = Number(transformed.original_id);
                      originalQuestion = this.originalQuestions.find(q => 
                        q.id === numericId.toString() || 
                        q.id === `q${numericId}`
                      );
                    }
                  } else if (transformed.original) {
                    // 如果已经包含original对象，直接使用
                    originalQuestion = transformed.original;
                  } else {
                    // 尝试通过其他方式匹配（如答案或内容相似）
                    const index = transformedData.indexOf(transformed);
                    if (index < questionsToTransform.length) {
                      originalQuestion = questionsToTransform[index];
                    }
                  }
                  
                  if (originalQuestion) {
                    // 确保transformed包含所有必要字段
                    const processedTransformed = {
                      ...transformed,
                      id: transformed.id || `${originalQuestion.id}_transformed`,
                      type: transformed.type || originalQuestion.type,
                      prompt: transformed.prompt || transformed.content || transformed.question || originalQuestion.prompt,
                      options: transformed.options || originalQuestion.options,
                      answer: transformed.answer || originalQuestion.answer,
                      original: originalQuestion,
                      transformationType: method,
                      similarity_score: parseFloat(transformed.similarity_score || 0.8)
                    };
                    
                    // 严格使用后端返回的is_valid字段，不在前端重新计算
                    if (transformed.is_valid !== undefined) {
                      // 确保boolean类型
                      processedTransformed.is_valid = transformed.is_valid === true || transformed.is_valid === 'true';
                    } else {
                      // 如果后端没有返回is_valid字段，按相似度>0.8判断
                      processedTransformed.is_valid = processedTransformed.similarity_score >= 0.8;
                    }
                    
                    console.log('成功匹配并处理题目:', {
                      id: processedTransformed.id,
                      original_id: transformed.original_id,
                      is_valid: processedTransformed.is_valid,
                      similarity: processedTransformed.similarity_score
                    });
                    
                    // 添加到结果数组
                    this.transformedQuestions.push(processedTransformed);
                  } else {
                    console.warn('找不到对应的原始题目，尝试使用位置索引匹配:', transformed);
                    // 如果ID匹配失败，尝试使用位置索引匹配
                    const index = transformedData.indexOf(transformed);
                    if (index < questionsToTransform.length) {
                      const backupOriginal = questionsToTransform[index];
                      console.log('使用位置索引匹配找到原题:', backupOriginal.id);
                      
                      // 创建处理后的转换题目
                      const processedTransformed = {
                        ...transformed,
                        id: transformed.id || `${backupOriginal.id}_transformed`,
                        type: transformed.type || backupOriginal.type,
                        prompt: transformed.prompt || transformed.content || transformed.question || backupOriginal.prompt,
                        options: transformed.options || backupOriginal.options,
                        answer: transformed.answer || backupOriginal.answer,
                        original: backupOriginal,
                        transformationType: method,
                        similarity_score: parseFloat(transformed.similarity_score || 0.8),
                        is_valid: transformed.is_valid === true || transformed.is_valid === 'true' || 
                                 (transformed.similarity_score ? parseFloat(transformed.similarity_score) >= 0.8 : true)
                      };
                      
                      // 添加到结果数组
                      this.transformedQuestions.push(processedTransformed);
                    } else {
                      console.error('无法匹配题目，跳过此题:', transformed);
                    }
                  }
                } catch (err) {
                  console.error('处理变形题目时出错:', err, transformed);
                }
              }
              
              // 更新进度
              this.transformationProgress += questionsToTransform.length;
            } else {
              this.$message.error(`${method}变形失败: ${response.data.message}`);
            }
          }
          
          // 变形完成后，显示结果
          if (this.transformedQuestions.length === 0) {
            this.$message.warning('没有成功变形的题目');
          } else {
            // 计算有效题目数量
            const validCount = this.transformedQuestions.filter(q => q.is_valid === true).length;
            console.log(`变形总结: 总题数=${this.transformedQuestions.length}, 有效题数=${validCount}`);
            console.log('所有变形题目有效性:', this.transformedQuestions.map(q => ({
              id: q.id,
              similarity: q.similarity_score,
              is_valid: q.is_valid
            })));
            
            // 计算有效率
            const validityRatio = validCount / this.transformedQuestions.length;
            this.$message.success(`成功变形${this.transformedQuestions.length}道题目，有效题数${validCount}，有效率${(validityRatio * 100).toFixed(1)}%`);
            
            // 保存变形题目到后端
            this.saveTransformedQuestions();
          }
        } catch (error) {
          console.error('变形题目失败:', error);
          let errorMessage = '变形题目失败';
          
          // 尝试提取详细错误信息
          if (error.response && error.response.data) {
            errorMessage += `：${error.response.data.message || JSON.stringify(error.response.data)}`;
          } else if (error.message) {
            errorMessage += `：${error.message}`;
          } else {
            errorMessage += '，请检查网络连接或服务器状态';
          }
          
          this.$message.error(errorMessage);
        } finally {
          this.isTransforming = false;
          this.transformingQuestionIndex = -1;
          this.currentTransformMethod = '';
        }
      },
      
      handlePageChange(page) {
        this.currentPage = page;
      },
      
      onShowSizeChange(current, size) {
        this.pageSize = size;
        this.currentPage = 1;
      },
      
      getTransformationColor(type) {
        const colorMap = {
          '语序变换': '#1890ff',
          '同义词替换': '#fa8c16',
          '选项扰动': '#722ed1',
          '上下文调整': '#52c41a',
          '情感立场转换': '#13c2c2',
          '噪声注入': '#f5222d'
        };
        return colorMap[type] || '#1890ff';
      },
      
      getTypeName(type) {
        const typeMap = {
          'single': '单选题',
          'judge': '判断题',
          'essay': '简答题'
        };
        return typeMap[type] || type;
      },
      
      getTypeColor(type) {
        const colorMap = {
          'single': 'blue',
          'judge': 'orange',
          'essay': 'purple'
        };
        return colorMap[type] || 'blue';
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
        
        return sourceNames[source] || source;
      },
      
      // 搜索功能
      handleSearch() {
        this.currentPage = 1;
      },
      
      // 导出功能
      async exportQuestions(format) {
        this.isTransforming = true;
        try {
          // 获取原始题目
          const originalQuestions = this.originalQuestions || [];
          
          // 获取变形题目
          const transformedQuestions = this.transformedQuestions || [];
          
          if (originalQuestions.length === 0 && transformedQuestions.length === 0) {
            this.$message.warning('没有可导出的题目');
            return;
          }
          
          console.log(`准备导出拓展题库为${format}格式（原始题目: ${originalQuestions.length}, 变形题目: ${transformedQuestions.length}）`);
          
          const response = await fetch(`http://localhost:5000/api/questions/export-transformed-${format}`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({
              originalQuestions: originalQuestions,
              transformedQuestions: transformedQuestions
            })
          });

          if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || '导出失败');
          }

          const blob = await response.blob();
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;

          // 使用与后端一致的命名格式：拓展题库_年月日_时分秒
          const now = new Date();
          const formatter = (num) => num.toString().padStart(2, '0');
          const timestamp = `${now.getFullYear()}${formatter(now.getMonth() + 1)}${formatter(now.getDate())}_${formatter(now.getHours())}${formatter(now.getMinutes())}${formatter(now.getSeconds())}`;
          a.download = `拓展题库_${timestamp}.${format}`;
          document.body.appendChild(a);
          a.click();

          // 清理
          setTimeout(() => {
            document.body.removeChild(a);
            window.URL.revokeObjectURL(url);
          }, 0);

          this.$message.success(`成功导出拓展题库为${format.toUpperCase()}文件`);
        } catch (error) {
          console.error(`导出${format.toUpperCase()}失败:`, error);
          this.$message.error(`导出${format.toUpperCase()}失败: ${error.message || '请重试'}`);
        } finally {
          this.isTransforming = false;
        }
      },
      exportToJson() {
        this.exportQuestions('json');
      },
      exportToExcel() {
        this.exportQuestions('xlsx');
      },
    }
  };
</script>
  
<style lang="scss" scoped>
.question-expansion-container {
  padding-top: 40px;
}

.mb-15 {
  margin-bottom: 15px;
}

.mb-24 {
  margin-bottom: 24px;
}

.font-bold {
  font-weight: 600;
}


.control-panel,
.transform-methods {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
}

.control-panel:hover,
.transform-methods:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.form-item {
  margin-bottom: 16px;
}

.form-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
  margin-bottom: 8px;
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

.transform-checkbox-group {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}

.import-btn {
  border: 1px dashed #d9d9d9;
  font-size: 14px;
  height: 52px;
  transition: all 0.3s;
}

.import-btn:hover {
  border-color: #40a9ff;
  color: #40a9ff;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-content svg {
  margin-right: 8px;
}

.generate-btn {
  margin-top: 24px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.transform-item {
  height: 78px;
  display: flex;
  align-items: center;
  padding: 12px;
  border-radius: 16px;
  margin-bottom: 12px;
  transition: all 0.3s;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.transform-item:hover {
  transform: translateY(-7px);
  cursor: pointer;
}

.transform-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 42px;
  height: 42px;
  border-radius: 8px;
  background-color: rgba(255, 255, 255, 0.6);
  margin-right: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}
.transform-icon:hover {
  transform: scale(1.1);
}
.transform-info {
  flex: 1;
}
.transform-name {
  font-weight: 600;
  font-size: 14px;
  margin-bottom: 4px;
}

.transform-desc {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.65);
}

.transform-item-blue {
  background-color: rgba(24, 144, 255, 0.06);
  border: 1px solid rgba(24, 144, 255, 0.15);
}

.transform-item-orange {
  background-color: rgba(250, 140, 22, 0.06);
  border: 1px solid rgba(250, 140, 22, 0.15);
}

.transform-item-purple {
  background-color: rgba(114, 46, 209, 0.06);
  border: 1px solid rgba(114, 46, 209, 0.15);
}

.transform-item-green {
  background-color: rgba(82, 196, 26, 0.06);
  border: 1px solid rgba(82, 196, 26, 0.15);
}

.transform-item-cyan {
  background-color: rgba(19, 194, 194, 0.06);
  border: 1px solid rgba(19, 194, 194, 0.15);
}

.transform-item-red {
  background-color: rgba(245, 34, 45, 0.06);
  border: 1px solid rgba(245, 34, 45, 0.15);
}

.progress-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.progress-header {
  margin-bottom: 16px;
}

.progress-info {
  margin-top: 16px;
}

.current-question,
.current-method {
  font-size: 14px;
  margin-bottom: 8px;
}

.question-label,
.method-label {
  color: rgba(0, 0, 0, 0.65);
  display: inline-block;
  width: 80px;
}

.question-content,
.method-content {
  color: rgba(0, 0, 0, 0.85);
  font-weight: 500;
}

.questions-display {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-toolbar {
  margin-bottom: 16px;
}

.statistics-bar,
.transform-stats,
.transform-filter {
  display: none;
}

.questions-list {
  margin-bottom: 16px;
}

.question-panel {
  margin-bottom: 16px;
}

.question-header {
  margin-bottom: 12px;
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
}

.question-tags .ant-tag {
  margin-right: 8px;
  margin-bottom: 8px;
}

.original-question-section,
.transformed-question-section {
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
}

.section-title {
  font-weight: 600;
  color: #1f2937;
  font-size: 16px;
  margin-bottom: 12px;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.original-question-section {
  background-color: #f9fafb;
  border: 1px solid #f0f0f0;
}

.transformed-question-section {
  background-color: rgba(24, 144, 255, 0.05);
  border: 1px solid rgba(24, 144, 255, 0.15);
}

.question-prompt,
.question-options,
.question-answer {
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
  margin-bottom: 8px;
  transition: all 0.3s;
}

.option-item.option-selected {
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
  flex: 1;
  line-height: 1.5;
}

.answer-content {
  font-weight: 500;
  color: #1890ff;
}

.empty-state {
  padding: 48px 0;
  text-align: center;
}

.empty-content {
  display: inline-block;
}

.empty-content svg {
  margin-bottom: 16px;
}

.empty-text {
  color: rgba(0, 0, 0, 0.45);
  font-size: 14px;
  line-height: 1.6;
}

.empty-text a {
  color: #1890ff;
  text-decoration: none;
}

.empty-text a:hover {
  text-decoration: underline;
}

.highlight-text {
  color: #1890ff;
  cursor: pointer;
}

.count-indicator {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 20px;
  height: 20px;
  line-height: 20px;
  padding: 0 6px;
  margin-left: 10px;
  font-size: 12px;
  font-weight: 500;
  color: #fff;
  background-color: #1890ff;
  border-radius: 10px;
  text-align: center;
}

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
.pagination-info{
  padding-top: 15px;
}

.card-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  position: relative;
}

.card-header h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #1f2937;
  text-align: center;
}

.card-actions {
  position: absolute;
  right: 0;
  top: 0;
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
</style>