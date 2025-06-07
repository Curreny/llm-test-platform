<template>
  <div class="data-audit-container">
    <!-- 页面标题部分 -->
    <a-row :gutter="24" class="mb-24"id="header-data-audit">
      <a-col :span="24">
        <a-card :bordered="false" class="header-card">
          <div class="card-header mb-15">
            <h2 class="font-bold">📶模型响应检测</h2>
          </div>
          <p class="problem-text">
            针对大模型测试结果，平台能够自动审核测试结果，并将大模型输入、输出与判定结果进行页面展示，支持规则匹配和模型辅助2种审核模式，且自动化判定审核成功率大于90%。
          </p>
        </a-card>
      </a-col>
    </a-row>

    <a-row :gutter="24" class="mb-24">
      <!-- 左侧控制面板 -->
      <a-col :span="24" :lg="12" class="mb-24">
        <a-card :bordered="false" class="control-panel"style="height:410px;" >
          <div class="card-header mb-5">
            <h3 class="font-bold">模型响应检测设置</h3>
          </div>
          
          <!-- 导入题目按钮 -->
          <a-button              
            type="dashed" 
            block 
            class="import-btn mb-15"
            @click="showImportDialog"
          >
            <span class="btn-content">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M21 15V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V15" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M7 10L12 15M12 15L17 10M12 15V3" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              导入题库 
              <span v-if="questions.length > 0" class="count-indicator">
                {{questions.length}} 题
              </span>
            </span>
          </a-button>
          
          <!-- 选择测试模型 -->
          <div class="section-container mb-5" style="width: 100%;">
            <div class="aaa">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="section-icon">
                <path d="M12 6.25278V19.2528M12 6.25278C10.8321 5.47686 9.24649 5 7.5 5C5.75351 5 4.16789 5.47686 3 6.25278V19.2528C4.16789 18.4769 5.75351 18 7.5 18C9.24649 18 10.8321 18.4769 12 19.2528M12 6.25278C13.1679 5.47686 14.7535 5 16.5 5C18.2465 5 19.8321 5.47686 21 6.25278V19.2528C19.8321 18.4769 18.2465 18 16.5 18C14.7535 18 13.1679 18.4769 12 19.2528" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
              选择测试模型
                </div>
            <a-select
              v-model="selectedModels"
              placeholder="请选择要测试的模型"
              class="model-select mb-10"
              :options="modelOptions"
            ></a-select>
              </div>

          <!-- 检测模式选择 -->
          <div class="section-container mb-5">
            <div class="aaa">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" class="section-icon">
                <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
              响应检测模式
              </div>
            <div class="audit-mode-cards">
              <div 
                v-for="mode in auditModes" 
                :key="mode.value"
                class="audit-mode-card" 
                :class="{ active: selectedAuditModes.includes(mode.value) }"
                @click="toggleAuditMode(mode.value)"
              >
                <div class="mode-icon" :class="`mode-${mode.value}`">
                  <div v-html="mode.icon"></div>
            </div>
                <div class="mode-content">
                  <div class="mode-title">{{ mode.label }}</div>
                  <div class="mode-desc">{{ mode.description }}</div>
                </div>
                <div class="mode-checkbox">
                  <a-checkbox :checked="selectedAuditModes.includes(mode.value)"></a-checkbox>
                </div>
              </div>
            </div>
          </div>
          
          <!-- 开始检测按钮 -->
          <a-button 
            type="primary" 
            size="large" 
            block 
            @click="startAudit" 
            :loading="isAuditing"
            class="audit-btn"
          >
            <span class="btn-content">
              <svg v-if="!isAuditing" width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M5 3L19 12L5 21V3Z" fill="white"/>
              </svg>
              {{ isAuditing ? '正在检测中...' : '开始模型检测' }}
            </span>
          </a-button>
        
        </a-card>
      </a-col>

      <!-- 右侧变形方式卡片 -->
      <a-col :span="24" :lg="12" class="mb-24">
        <a-card :bordered="false" class="control-panel" style="height:410px;">
          <div class="card-header mb-15">
            <h3 class="font-bold">平台功能说明</h3>
          </div>
          
          <a-row :gutter="16">
            <a-col :span="12" :xs="12">
              <div class="transform-item transform-item-blue">
                <div class="transform-icon">
                  <svg viewBox="0 0 24 24" width="28" height="28" fill="#1890ff" aria-hidden="true">
                    <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm4.59-12.42L10 14.17l-2.59-2.58L6 13l4 4 8-8z"/>
                  </svg>
                </div>
                <div class="transform-info">
                  <div class="transform-name">模型响应检测能力</div>
                  <div class="transform-desc">自动检测大模型响应结果，支持规则匹配和模型辅助的检测模式</div>
                </div>
              </div>
            </a-col>
            <a-col :span="12" :xs="12">
              <div class="transform-item transform-item-orange">
                <div class="transform-icon">
                  <svg viewBox="0 0 24 24" width="28" height="28" fill="#fa8c16" aria-hidden="true">
                    <path d="M16 6l2.29 2.29-4.88 4.88-4-4L2 16.59 3.41 18l6-6 4 4 6.3-6.29L22 12V6h-6z"/>
                  </svg>
                </div>
                <div class="transform-info">
                  <div class="transform-name">判定成功率</div>
                  <div class="transform-desc">自动化判定检测成功率大于90%</div>
                </div>
              </div>
            </a-col>
            <a-col :span="12" :xs="12">
              <div class="transform-item transform-item-purple">
                <div class="transform-icon">
                  <svg viewBox="0 0 24 24" width="28" height="28" fill="#722ed1" aria-hidden="true">
                    <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 13h2v4H7zm4-6h2v10h-2zm4 3h2v7h-2z"/>
                  </svg>
                </div>
                <div class="transform-info">
                  <div class="transform-name">性能评估</div>
                  <div class="transform-desc">分析模型性能、安全性和准确性指标</div>
                </div>
              </div>
            </a-col>
            <a-col :span="12" :xs="12">
              <div class="transform-item transform-item-green">
                <div class="transform-icon">
                  <svg viewBox="0 0 24 24" width="28" height="28" fill="#52c41a" aria-hidden="true">
                    <path d="M15.5 1h-8C6.12 1 5 2.12 5 3.5v17C5 21.88 6.12 23 7.5 23h8c1.38 0 2.5-1.12 2.5-2.5v-17C18 2.12 16.88 1 15.5 1zm-4 21c-.83 0-1.5-.67-1.5-1.5s.67-1.5 1.5-1.5 1.5.67 1.5 1.5-.67 1.5-1.5 1.5zm4.5-4H7V4h9v14z"/>
                  </svg>
                </div>
                <div class="transform-info">
                  <div class="transform-name">资源监控</div>
                  <div class="transform-desc">监测推理速度、内存和计算资源消耗</div>
                </div>
              </div>
            </a-col>
            <a-col :span="12" :xs="12">
              <div class="transform-item transform-item-cyan">
                <div class="transform-icon">
                  <svg viewBox="0 0 24 24" width="28" height="28" fill="#13c2c2" aria-hidden="true">
                    <path d="M3 13h8V3H3v10zm0 8h8v-6H3v6zm10 0h8V11h-8v10zm0-18v6h8V3h-8z"/>
                  </svg>
              </div>
                <div class="transform-info">
                  <div class="transform-name">多样化展示</div>
                  <div class="transform-desc">图表、数据表格等多种结果呈现方式</div>
              </div>
              </div>
            </a-col>
            <a-col :span="12" :xs="12">
              <div class="transform-item transform-item-red">
                <div class="transform-icon">
                  <svg viewBox="0 0 24 24" width="28" height="28" fill="#f5222d" aria-hidden="true">
                    <path d="M14 2H6c-1.1 0-1.99.9-1.99 2L4 20c0 1.1.89 2 1.99 2H18c1.1 0 2-.9 2-2V8l-6-6zm2 16H8v-2h8v2zm0-4H8v-2h8v2zm-3-5V3.5L18.5 9H13z"/>
                  </svg>
              </div>
                <div class="transform-info">
                  <div class="transform-name">自动化报告</div>
                  <div class="transform-desc">支持一键生成性能与安全性观测报告</div>
                </div>
              </div>
      </a-col>
    </a-row>
        </a-card>
      </a-col>
    
      <!-- 下侧主区域 -->
      <a-col :span="24" :lg="24">
    <!-- 空状态 -->
        <a-card v-if="auditResults.length === 0 && !isAuditing" :bordered="false" class="empty-state-card">
          <div class="card-header mb-15">
            <h3 class="font-bold" style="font-size: 28px;">📊检测结果预览</h3>
          </div>
          <div class="empty-state">
            <div class="empty-content">
              <svg viewBox="0 0 24 24" width="80" height="80" fill="#bfbfbf" aria-hidden="true">
                <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 10h2v7H7zm4-3h2v10h-2zm4 6h2v4h-2z"/>
              </svg>
              <p class="empty-text">
                暂无模型测试与检测结果<br/>
                请导入题库、选择测试模型和检测模式，然后点击「开始模型检测」按钮
              </p>
            </div>
          </div>
        </a-card>


        <!-- 结果展示区 -->
        <a-card v-else :bordered="false" class="questions-display"id="results-preview">
          <div class="card-header mb-15">
            <h2 class="font-bold"style="font-size: 28px;">📊检测结果预览</h2>
          </div>
          
          <!-- 检测进度展示 -->
          <a-col :span="24" v-if="isAuditing">
            <a-card :bordered="false" class="progress-card mb-24">
              <div class="progress-header">
                <h3>正在检测题目 {{auditProgress}}/{{questions.length}}</h3>
              </div>
              <a-progress :percent="auditProgressPercentage" status="active" />
              <div class="progress-info" v-if="auditingQuestionIndex >= 0">
                <p class="current-question">
                  <span class="question-label">当前题目：</span>
                  <span class="question-content">{{auditingQuestionIndex >= 0 && questions[auditingQuestionIndex] && questions[auditingQuestionIndex].问题 || ''}}</span>
                </p>
                <p class="current-model">
                  <span class="model-label">测试模型：</span>
                  <span class="model-content">{{selectedModels}}</span>
                </p>
              </div>
            </a-card>
          </a-col>
          
          <!-- 有检测结果时显示 -->
          <div v-if="auditResults.length > 0">
            <!-- 筛选工具栏 -->
            <div class="filter-toolbar mb-15">
              <a-row :gutter="16" type="flex" align="middle">
                <a-col :span="6">
                  <a-input-search 
                    placeholder="搜索题目关键词"
                    v-model="filterKeyword" 
                    @search="onSearch"
                    class="search-input"
                  />
                </a-col>

                <a-col :span="6">
                  <a-select 
                    v-model="filterQuestionType" 
                    placeholder="按题型筛选" 
                    style="width: 100%"
                    allow-clear
                  >
                    <a-select-option value="">全部题型</a-select-option>
                    <a-select-option value="single">选择题</a-select-option>
                    <a-select-option value="judge">判断题</a-select-option>
                    <a-select-option value="essay">问答题</a-select-option>
                  </a-select>
                </a-col>

                <a-col :span="6">
                  <a-select 
                    v-model="filterDomain" 
                    placeholder="按领域筛选" 
                    style="width: 100%"
                    allow-clear
                  >
                    <a-select-option value="">全部领域</a-select-option>
                    <a-select-option v-for="domain in domainStats" :key="domain.name" :value="domain.name">
                      {{domain.name}} ({{domain.count}})
                    </a-select-option>
                  </a-select>
                </a-col>

                <a-col :span="6">
                  <a-select 
                    v-model="filterSource" 
                    placeholder="按数据集来源筛选" 
                    style="width: 100%"
                    allow-clear
                  >
                    <a-select-option value="">全部来源</a-select-option>
                    <a-select-option v-for="source in sourceList" :key="source.name" :value="source.name">
                      {{source.name}} ({{source.count}})
                    </a-select-option>
                  </a-select>
                </a-col>
              </a-row>
            </div>
            
            <!-- 结果列表 -->
            <div class="questions-list">
              <!-- 表格视图替代折叠面板 -->
              <a-table 
                :dataSource="paginatedResults" 
                :rowKey="record => record.id || Math.random().toString()"
                :pagination="false"
                :expandedRowKeys="expandedRows"
                @expand="handleExpandRow"
                :expandIconColumnIndex="-1"
                class="audit-table"
              >
                <!-- 问题列 -->
                <a-table-column title="问题" data-index="question" :width="350">
                  <template slot-scope="text, record, index">
                    <div class="question-cell">
                      <div class="question-index">{{ (currentPage - 1) * pageSize + index + 1 }}</div>
                      <div class="question-text">{{ text.length > 50 ? text.substring(0, 50) + '...' : text }}</div>
                    </div>
                  </template>
                </a-table-column>

                <!-- 模型列 -->
                <a-table-column title="模型" data-index="modelName" :width="100">
                  <template slot-scope="text">
                    <a-tag color="blue">{{ text }}</a-tag>
                  </template>
                </a-table-column>

                <!-- 题型列 -->
                <a-table-column title="题型" data-index="questionTypeZh" :width="120">
                  <template slot-scope="text, record">
                    <a-tag :color="record.questionType === 'single' ? '#1890ff' : (record.questionType === 'judge' ? '#fa8c16' : '#722ed1')">
                      {{ record.questionTypeZh }}
                    </a-tag>
                  </template>
                </a-table-column>

                <!-- 结果列 -->
                <a-table-column title="检测结果" data-index="isPassed" :width="100">
                  <template v-if="record.questionType !== 'essay' && record.qualityScore === null" slot-scope="text, record">
                    <a-tag :color="record.isPassed ? '#52c41a' : '#f5222d'">
                      {{ record.isPassed ? '通过' : '不通过' }}
                    </a-tag>
                  </template>
                </a-table-column>

                <!-- 评分列 - 仅对问答题显示 -->
                <a-table-column title="质量评分" data-index="qualityScore" :width="120">
                  <template slot-scope="text, record">
                    <template v-if="record.questionType === 'essay' && record.qualityScore !== null">
                      <a-progress 
                        :percent="record.qualityScore" 
                        :stroke-color="getScoreColor(record.qualityScore)" 
                        :format="percent => `${percent}分`"
                        size="small"
                        style="width: 80px;"
                      />
                    </template>
                    <span v-else>-</span>
                  </template>
                </a-table-column>

                <!-- 安全评分列 -->
                <a-table-column title="安全指数" :width="120">
                  <template slot-scope="text, record">
                    <template v-if="record.evaluationMetrics && record.evaluationMetrics['内容安全性']">
                      <a-progress 
                        :percent="record.evaluationMetrics['内容安全性']" 
                        :stroke-color="getSafetyColor(record.evaluationMetrics['内容安全性'])" 
                        :format="percent => `${percent}分`"
                        size="small"
                        style="width: 80px;"
                      />
                    </template>
                    <span v-else>-</span>
                  </template>
                </a-table-column>

                <!-- 响应时间列 -->
                <a-table-column title="响应时间" data-index="responseTime" :width="90">
                  <template slot-scope="text">
                    {{ text }}s
                  </template>
                </a-table-column>

                <!-- 操作列 -->
                <a-table-column title="操作" :width="100">
                  <template slot-scope="text, record">
                    <a-button 
                      type="link" 
                      class="detail-button"
                      @click="() => {
                        const key = record.id || Math.random().toString();
                        expandedRows = expandedRows.includes(key) ? 
                          [] : // 如果当前行已展开，则收起
                          [key]; // 只保留当前行为展开状态，其他行收起
                        handleExpandRow(expandedRows.includes(key), record);
                      }"
                    >
                      详情
                    </a-button>
                  </template>
                </a-table-column>

                <!-- 展开行的内容 -->
                <template slot="expandedRowRender" slot-scope="record">
                  <div class="expanded-row-detail">
                    <a-row :gutter="16">
                      <a-col :span="record.evaluationMetrics ? 12 : 24">
                        <a-card title="详细信息" class="detail-card" :bordered="false">
                          <!-- 问题和答案对比 -->
                          <a-descriptions title="问题详情" :column="1" bordered size="small">
                            <a-descriptions-item label="问题">
                              {{ record.question }}
                            </a-descriptions-item>
                            
                            <!-- 显示选项（如果有） -->
                            <a-descriptions-item v-if="record.options && record.options.length > 0" label="选项">
                              <div class="options-list">
                                <div v-for="(option, idx) in record.options" :key="idx" class="option-item" :class="{'correct-option': record.standardAnswer === String.fromCharCode(65 + idx)}">
                                  <span class="option-letter">{{ String.fromCharCode(65 + idx) }}.</span>
                                  <span class="option-text">{{ option }}</span>
                                </div>
                              </div>
                            </a-descriptions-item>
                            
                            <a-descriptions-item label="标准答案">
                              <template v-if="record.questionType === 'single' || record.questionType === 'judge'">
                                <a-tag color="gold">选项 {{ record.standardAnswer }}</a-tag>
                                <span v-if="record.options && record.standardAnswer && record.standardAnswer.charCodeAt(0) - 65 < record.options.length">
                                  - {{ record.options[record.standardAnswer.charCodeAt(0) - 65] }}
                                </span>
                              </template>
                              <template v-else>
                                {{ record.standardAnswer }}
                              </template>
                            </a-descriptions-item>

                            <a-descriptions-item label="模型回答">
                              <template v-if="record.questionType === 'single' || record.questionType === 'judge'">
                                <div class="model-answer">
                                  <a-tag :color="record.isPassed ? '#52c41a' : '#f5222d'">{{ record.answer }}</a-tag>
                                </div>
                              </template>
                              <template v-else-if="record.answer && record.answer.includes('[内容已过滤]')">
                                <div class="essay-answer filtered-content">
                                  <a-alert type="warning" message="内容已过滤" description="该问题可能包含敏感内容，模型拒绝回答" banner />
                                </div>
                              </template>
                              <template v-else>
                                <div class="essay-answer">{{ record.answer }}</div>
                              </template>
                            </a-descriptions-item>
                            
                            <a-descriptions-item v-if="record.fullResponse && record.fullResponse !== record.answer" label="完整回答">
                              <div class="full-response">{{ record.fullResponse }}</div>
                            </a-descriptions-item>
                          </a-descriptions>
                        </a-card>
                      </a-col>
                      
                      <a-col :span="12" v-if="record.evaluationMetrics">
                        <a-card title="多维度评估指标" class="metrics-card" :bordered="false">
                          <div class="metrics-radar-chart" ref="radarChart" :id="'radar-chart-' + record.id"></div>
                          <div class="metrics-table">
                            <a-table :dataSource="formatMetricsData(record.evaluationMetrics)" 
                                    :columns="metricsColumns" 
                                    :pagination="false"
                                    size="small">
                            </a-table>
                          </div>
                        </a-card>
                      </a-col>
                    </a-row>
                    
                  </div>
                </template>
              </a-table>
              
              <!-- 空结果提示 -->
              <div v-if="paginatedResults.length === 0" class="empty-state">
                <div class="empty-content">
                  <svg viewBox="0 0 24 24" width="48" height="48" fill="#d9d9d9">
                    <path d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/>
                  </svg>
                  <p class="empty-text">没有找到匹配的检测结果</p>
                </div>
              </div>
            </div>
            
        
            
            <!-- 分页组件 -->
            <div class="pagination-container" v-if="paginatedResults.length > 0">
              <div class="pagination-wrapper">
                <div class="pagination-left">
                  <a-pagination 
                    v-model="currentPage" 
                    :total="filteredResults.length" 
                    :pageSize="pageSize"
                    @change="onPageChange"
                    show-quick-jumper
                    show-size-changer
                    :pageSizeOptions="['5', '10', '20', '50']"
                    @showSizeChange="onShowSizeChange"
                  />
                  <div class="pagination-info">
                    共 {{filteredResults.length}} 项，当前显示第 {{(currentPage-1)*pageSize+1}} - {{Math.min(currentPage*pageSize, filteredResults.length)}} 项
                  </div>
                </div>             
              </div>
              <div class="pagination-right">
                <!-- 清除数据按钮 -->
                <a-popconfirm
                  title="确定要清除所有测试结果吗？此操作无法撤销。"
                  @confirm="clearResults"
                  okText="确定"
                  cancelText="取消"
                >
                  <a-button 
                    type="danger" 
                    size="large" 
                    block 
                    :disabled="isAuditing || auditResults.length === 0"
                  >
                    <span class="btn-content"style="font-size: 15px;">
                      <a-icon type="delete" />
                      清除测试结果
                    </span>
                  </a-button>
                </a-popconfirm>
              </div>
            </div>
            
            
            <!-- 当前为统计图表 -->
            <a-col :span="24" class="mb-24">
              <a-card :bordered="false" class="chart-panel">
                <div class="card-header mb-15">
                  <h2 class="font-bold"style="font-size: 28px;">测试总体结果预览</h2>
                </div>
                
                <!-- 无数据时显示的空状态 -->
                <div v-if="auditResults.length === 0" class="empty-state">
                  <a-empty description="暂无测试数据" />
                  <p class="empty-desc">请先在上方进行模型测试，生成结果后将在此处显示统计图表</p>
                </div>
                
                <!-- 图表区域 - 改为统一布局 -->
                <a-row :gutter="16" v-else>
  
                  <a-col :span="8" class="mb-24">
                  <div class="chart-container">
                      <div class="chart-title">选择题 & 判断题 & 问答题综合表现</div>
                      <div class="chart-wrapper" id="choice-performance-chart"></div>
                  </div>
                  </a-col>
                  
                  <!-- 问答题的多指标评分雷达图 -->
                  <a-col :span="8" class="mb-24">
                  <div class="chart-container">
                      <div class="chart-title">问答题质量多维评分</div>
                      <div class="chart-wrapper" id="essay-quality-radar-chart"></div>
                  </div>
                  </a-col>
                  
                  <!-- 题目来源分布 -->
                  <a-col :span="8" class="mb-24">
                  <div class="chart-container">
                      <div class="chart-title">题目来源分布</div>
                      <div class="chart-wrapper" id="question-source-chart"></div>
                  </div>
                  </a-col>
                  
                  <!-- 题目领域覆盖统计 -->
                  <a-col :span="12" class="mb-24">
                  <div class="chart-container">
                      <div class="chart-title">领域分布与正确率</div>
                      <div class="chart-wrapper" id="domain-distribution-chart"></div>
                  </div>
                  </a-col>
                  
                  <!-- 推理时间 & 资源使用趋势图 -->
                  <a-col :span="12" class="mb-24">
                    <div class="chart-container">
                      <div class="chart-title">大模型资源消耗分析</div>
                      <div class="chart-wrapper" id="inference-time-chart"></div>
                    </div>
                  </a-col>
                </a-row>

              </a-card>
            </a-col>
            
          </div>
        </a-card>
      </a-col>
    </a-row>
    
    <!-- 导入对话框 -->
    <a-modal
      v-model="importDialogVisible"
      title="导入题库"
      okText="确认导入"
      cancelText="取消"
      :confirmLoading="isImporting"
      @ok="handleImportConfirm"
    >
      <div class="import-options">
        <div class="file-upload-area mb-15">
          <a-upload-dragger
            name="file"
            :multiple="false"
            :beforeUpload="beforeUpload"
            :showUploadList="false"
            accept=".json"
          >
            <p class="ant-upload-drag-icon">
              <svg width="60" height="60" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <rect width="24" height="24" rx="4"/>
                <path d="M4 8C4 6.89543 4.89543 6 6 6H10L12 8H18C19.1046 8 20 8.89543 20 10V16C20 17.1046 19.1046 18 18 18H6C4.89543 18 4 17.1046 4 16V8Z" stroke="#1890ff" stroke-width="1.5" fill="#E6F7FF"/>
                <path d="M12 11V16" stroke="#1890ff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M9 13L12 10L15 13" stroke="#1890ff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </p>
            <p class="ant-upload-text">点击或拖拽JSON文件到此处</p>
            <p class="ant-upload-hint">
              支持导入题库JSON文件
            </p>
          </a-upload-dragger>
          <div v-if="fileInfo" class="file-info">
            <a-alert type="info" show-icon>
              <template slot="message">
                已选择文件: {{fileInfo.name}} ({{(fileInfo.size / 1024).toFixed(2)}} KB)
              </template>
            </a-alert>
            </div>
          </div>
      </div>
    </a-modal>
    
  
    <!-- 报告预览区域 - 有数据时显示 -->
    <a-row :gutter="16" v-if="auditResults.length > 0">
      <a-col :span="24">
        <a-card :bordered="false" class="report-card" id="report-generation">
          <div class="card-header mb-15">
            <h2 class="font-bold" style="text-align: center;font-size: 28px;">📝报告生成与预览</h2>
          </div>
          
          <a-row :gutter="24">
            <!-- 左侧报告配置区域 -->
            <a-col :span="8">
              <div class="report-config-panel">
                <h3 class="config-title">报告配置</h3>
                
                <a-form layout="vertical">
                  <a-form-item label="报告格式" class="format-form-item">
                    <div class="custom-radio-group">
                      <div 
                        class="custom-radio-button" 
                        :class="{ 'active': reportFormat === 'pdf' }" 
                        @click="reportFormat = 'pdf'"
                      >
                        <a-icon type="file-pdf" class="format-icon" />
                        <span class="format-text">PDF</span>
                      </div>
                      <div 
                        class="custom-radio-button" 
                        :class="{ 'active': reportFormat === 'html' }" 
                        @click="reportFormat = 'html'"
                      >
                        <a-icon type="html5" class="format-icon" />
                        <span class="format-text">HTML</span>
                      </div>
                    </div>
                  </a-form-item>
                  
                  <a-form-item label="报告内容" class="content-form-item">
                    <a-checkbox-group v-model="reportSections" class="content-checkbox-group">
                      <div class="checkbox-row">
                        <div class="checkbox-item">
                          <a-checkbox value="summary" class="content-checkbox">摘要概览</a-checkbox>
                        </div>
                        <div class="checkbox-item">
                          <a-checkbox value="performance" class="content-checkbox">性能分析</a-checkbox>
                        </div>
                      </div>
                      <div class="checkbox-row">
                        <div class="checkbox-item">
                          <a-checkbox value="charts" class="content-checkbox">图表数据</a-checkbox>
                        </div>
                        <div class="checkbox-item">
                          <a-checkbox value="recommendations" class="content-checkbox">优化建议</a-checkbox>
                        </div>
                      </div>
                    </a-checkbox-group>
                  </a-form-item>
                  
                  <div class="report-action-buttons">
                    <button 
                      class="custom-radio-button preview-button" 
                      @click="previewReport"
                    >
                      <a-icon type="eye" />
                      <span>预览报告</span>
                    </button>
                    <button 
                      class="custom-radio-button generate-button" 
                      @click="generateReport"
                      :disabled="isGeneratingReport"
                    >
                      <a-icon type="download" />
                      <span>生成报告</span>
                      <a-icon v-if="isGeneratingReport" type="loading" />
                    </button>
                  </div>
                </a-form>
              </div>
            </a-col>
            
            <!-- 右侧报告预览区域 -->
            <a-col :span="16">
              <div class="report-preview-container">
                <!-- 无报告时的状态 -->
                <div v-if="!reportPreviewVisible" class="empty-preview-state">
                  <a-icon type="file-text" class="empty-preview-icon" />
                  <div class="empty-preview-text">暂无报告预览</div>
                  <div class="empty-preview-subtext">请点击"预览报告"按钮生成预览</div>
                </div>
                
                <!-- 报告预览内容 -->
                <div v-else class="report-preview-panel">
                  <div class="report-preview-header">
                    <h3 class="preview-title">{{ currentModel || '大模型' }} 性能评估报告</h3>
                    <div class="preview-actions">
                      <button class="custom-button header-download-button" @click="generateReport">
                        <a-icon type="download" />
                        <span>下载报告</span>
                      </button>
                      <button class="custom-button header-close-button" @click="closeReportPreview">
                        <a-icon type="close" />
                        <span>关闭预览</span>
                      </button>
                    </div>
                  </div>
                  
                  <div class="report-document"></div>
                </div>
              </div>
            </a-col>
          </a-row>
        </a-card>
      </a-col>
    </a-row>

    <!-- 报告生成区域 - 无数据时显示空状态 -->
    <a-row :gutter="16" v-else>
      <a-col :span="24">
        <a-card :bordered="false" class="report-card" id="report-generation">
          <div class="card-header mb-15">
            <h2 class="font-bold" style="text-align: center;font-size: 28px;">📝报告生成与预览</h2>
          </div>
          
          <div class="empty-state">
            <a-empty description="暂无测试结果，无法生成报告" />
            <p class="empty-desc">请先完成模型测试，测试完成后可在此处生成评估报告</p>
          </div>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'DataAudit',
  
  data() {
    return {
      activeTab: 'data',
      questions: [],
      importDialogVisible: false,
      fileInfo: null,
      isImporting: false,
      selectedModels: "",
      selectedAuditModes: ["rule-based"],  // 使用数组存储多选值
      isAuditing: false,
      auditProgress: 0,
      auditingQuestionIndex: -1,
      auditResults: [],
      statsSummary: {
        totalCount: 0,
        passRate: 0,
        avgResponseTime: 0,
        choiceCount: 0,
        choicePassCount: 0,
        choicePassRate: 0,
        essayCount: 0,
        essayAvgScore: 0
      },
      filterKeyword: '',
      filterModel: '',
      filterQuestionType: '',
      filterDomain: '',
      filterSource: '',
      activeKeys: [],
      currentPage: 1,
      pageSize: 10,
      
      // 模型相关
      modelOptions: [
        { label: '请选择要检测的模型', value: '', disabled: true },
        { label: 'GLM-4-Plus', value: 'glm-4-plus' },
        { label: 'GLM-4-0520', value: 'glm-4-0520' },
        { label: 'GLM-4-AirX', value: 'glm-4-airx' },
        { label: 'GLM-Zero-Preview', value: 'glm-zero-preview' },
        { label: 'GLM-4-Air', value: 'glm-4-air' },
        { label: 'GLM-4-Long', value: 'glm-4-long' },
        { label: 'GLM-4-9B', value: 'glm-4-9b' }
      ],
      
      // 检测模式
      auditModes: [
        {
          label: '规则匹配',
          value: 'rule-based',
          description: '基于规则的自动检测',
          icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>'
        },
        {
          label: '模型辅助',
          value: 'model-assisted',
          description: '使用大模型辅助评估',
          icon: '<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2a4 4 0 0 0-4 4 4 4 0 0 0 4 4 4 4 0 0 0 4-4 4 4 0 0 0-4-4zM6 14a8 8 0 0 0-6 7h24a8 8 0 0 0-6-7 8.5 8.5 0 0 0-6 2.5 8.5 8.5 0 0 0-6-2.5z" fill="currentColor" stroke="none" /></svg>'
        }
      ],
      

      
      // 报告配置
      reportConfig: {
        title: '大模型检测报告',
        format: 'pdf',
        includes: ['summary', 'details', 'charts'],
        filter: 'all'
      },
      
      // 添加评估指标列定义
      metricsColumns: [
        { title: '评估维度', dataIndex: 'name', key: 'name' },
        { 
          title: '得分', 
          dataIndex: 'value', 
          key: 'value',
          customRender: (text, record) => {
            // 根据分数返回不同颜色的进度条
            const scoreColor = this.getScoreColor(record.value);
            return (
              <a-progress 
                percent={record.value} 
                format={percent => `${percent}分`} 
                status="normal" 
                strokeColor={scoreColor} />
            );
          }
        },
      ],
      
      // 跟踪展开的行
      expandedRows: [],
      
      // 摘要表格列
      summaryColumns: [
        { 
          title: '评估维度', 
          dataIndex: 'name', 
          key: 'name',
          scopedSlots: { customRender: 'name' },
          width: 150
        },
        { 
          title: '各模型评分', 
          dataIndex: 'modelScores', 
          key: 'modelScores',
          scopedSlots: { customRender: 'modelScores' }
        }
      ],
      
      // 报告生成相关变量
      reportFormat: 'pdf',
      reportSections: ['summary', 'performance', 'charts', 'recommendations'],
      isGeneratingReport: false,
      reportPreviewVisible: false,
      currentModel: '',
      averageInferenceTime: 0,
      averageMemoryUsage: 0,
      averageComputeLoad: 0,
      maxTypeResponseTime: 0,
      essayAverageScore: 0,
      correctRate: 0,
      averageResponseTime: 0,
    };
  },
  
  computed: {
    // 根据筛选条件过滤结果
    filteredResults() {
      let results = [...this.auditResults];
      
      // 按模型筛选
      if (this.filterModel) {
        results = results.filter(item => item.modelName === this.filterModel);
      }
      
      // 按数据集来源筛选
      if (this.filterSource) {
        results = results.filter(item => item.source === this.filterSource);
      }
      
      // 按题型筛选
      if (this.filterQuestionType) {
        results = results.filter(item => item.questionType === this.filterQuestionType);
      }
      
      // 按领域筛选
      if (this.filterDomain) {
        results = results.filter(item => item.domain === this.filterDomain);
      }
      
      // 按关键词搜索
      if (this.filterKeyword) {
        const keyword = this.filterKeyword.toLowerCase();
        results = results.filter(item => 
          (item.question && item.question.toLowerCase().includes(keyword)) || 
          (item.answer && item.answer.toLowerCase().includes(keyword))
        );
      }
      
      return results;
    },
    
    // 计算当前页的数据
    paginatedResults() {
      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      return this.filteredResults.slice(start, end);
    },
    
    // 领域统计
    domainStats() {
      const domains = {};
      this.auditResults.forEach(result => {
        const domain = result.domain;
        domains[domain] = (domains[domain] || 0) + 1;
      });
      
      return Object.keys(domains).map(name => ({
        name,
        count: domains[name]
      })).sort((a, b) => b.count - a.count);
    },
    
    // 数据来源列表
    sourceList() {
      const sources = {};
      this.auditResults.forEach(result => {
        if (result.source) {
          sources[result.source] = (sources[result.source] || 0) + 1;
        }
      });
      
      return Object.keys(sources).map(name => ({
        name,
        count: sources[name]
      })).sort((a, b) => b.count - a.count);
    },
    
    auditProgressPercentage() {
      if (this.questions.length === 0) return 0;
      return Math.floor((this.auditProgress / this.questions.length) * 100);
    },
  },
  
  created() {
    // 页面加载时尝试获取数据，模仿QuestionExpansion.vue的实现
    this.checkExistingQuestions();
    
    // 获取已保存的审计结果
    this.fetchAuditResults();
    
    // 添加窗口大小变化监听，实现图表自适应
    window.addEventListener('resize', this.handleResize);
  },
  
  mounted() {
    // 页面挂载后初始化所有图表
    if (this.auditResults.length > 0) {
      this.initializeAllCharts();
    }
  },
  
  updated() {
    // 组件更新后重新调整图表大小
    this.$nextTick(() => {
      this.handleResize();
    });
  },
  
  beforeDestroy() {
    // 组件销毁前移除监听
    window.removeEventListener('resize', this.handleResize);
  },
  
  methods: {
    // 检查是否有已存在的题目
    async checkExistingQuestions() {
      try {
        // 从会话存储中获取题库
        const sessionData = sessionStorage.getItem('questionBank');
        if (sessionData) {
          const parsedQuestions = JSON.parse(sessionData);
          // 更新题库选择列表
          this.availableQuestions = parsedQuestions.map(q => ({
            id: q.id,
            prompt: q.prompt,
            type: q.type,
            selected: true
          }));
          
          // 按题型分组
          this.updateQuestionGroups(this.availableQuestions);
          console.log(`已从会话中恢复${this.availableQuestions.length}道题目`);
        } 
      } catch (error) {
        console.error('检查已存在题目失败:', error);
      }
    },
    
    // 获取已保存的审计结果
    async fetchAuditResults() {
      try {
        // 从会话存储中获取审计结果
        const auditData = sessionStorage.getItem('auditResults');
        if (auditData) {
          this.auditResults = JSON.parse(auditData);
          console.log(`已从会话中恢复${this.auditResults.length}条审计结果`);
          
          // 如果有审计结果，也获取统计摘要
          const summaryData = sessionStorage.getItem('auditSummary');
          if (summaryData) {
            this.statsSummary = JSON.parse(summaryData);
          } else if (this.auditResults.length > 0) {
            // 如果没有保存的摘要但有结果，则重新计算
            this.statsSummary = this.calculateStatisticsFromResults(this.auditResults);
          }
        }
      } catch (error) {
        console.error('获取已保存审计结果失败:', error);
      }
    },
    
    // 保存审计结果到后端和会话存储
    async saveAuditResults() {
      if (this.auditResults.length === 0) return;
      
      try {
        // 保存到会话存储
        sessionStorage.setItem('auditResults', JSON.stringify(this.auditResults));
        
        // 如果有统计摘要，也保存它
        if (this.statsSummary) {
          sessionStorage.setItem('auditSummary', JSON.stringify(this.statsSummary));
        }
        
        console.log(`成功保存${this.auditResults.length}条审计结果`);
      } catch (error) {
        console.error('保存审计结果失败:', error);
      }
    },
    
    // 清空审计结果
    async clearAuditResults() {
      this.$confirm({
        title: '确认清空所有结果',
        content: '此操作将删除所有测试结果，无法恢复。确定要继续吗？',
        okText: '确定',
        okType: 'danger',
        cancelText: '取消',
        onOk: () => {
          this.auditResults = [];
          this.statsSummary = null;
          
          // 清除会话存储中的审计数据
          sessionStorage.removeItem('auditResults');
          sessionStorage.removeItem('auditSummary');
          
          // 保留题库数据，只清除结果
          this.updateQuestionSelection();
          
          // 清空图表
          this.destroyCharts();
          
          this.$message.success('已清空所有测试结果');
        },
      });
    },
    
    // 添加切换检测模式的方法
    toggleAuditMode(mode) {
      const index = this.selectedAuditModes.indexOf(mode);
      if (index === -1) {
        // 如果不存在，添加这个模式
        this.selectedAuditModes.push(mode);
      } else {
        // 如果已存在，且不是最后一个选中的模式，则移除
        if (this.selectedAuditModes.length > 1) {
          this.selectedAuditModes.splice(index, 1);
        } else {
          // 至少保留一个模式
          this.$message.info('至少需要选择一种检测模式');
        }
      }
    },
    
    // 开始模型响应检测
    async startAudit() {
      if (this.questions.length === 0) {
        this.$message.warning('请先导入题库');
        this.showImportDialog();
        return;
      }

      if (!this.selectedModels) {
        this.$message.warning('请选择一个测试模型');
        return;
      }
      
      this.isAuditing = true;
      this.auditProgress = 0;
      this.auditingQuestionIndex = 0;
      this.auditResults = [];
      
      try {
        console.log('调用模型API，开始测试...');
        console.log('发送数据:', {
          questions: this.questions.length,
          models: [this.selectedModels],
          auditMode: this.selectedAuditModes
        });
        
        // 为了实时显示进度，分批处理题目
        const totalQuestions = this.questions.length;
        const batchSize = 1; // 每次处理的题目数
        let processedCount = 0;
        let allResults = [];
        
        console.log('使用检测模式:', this.selectedAuditModes);
        
        // 批量处理题目
        for (let i = 0; i < totalQuestions; i += batchSize) {
          this.auditingQuestionIndex = i;
          this.auditProgress = i;
          
          const currentBatch = this.questions.slice(i, i + batchSize);
          
          // 调用后端API处理当前批次
          const response = await axios.post('/api/audit/test-models', {
            questions: currentBatch,
            models: [this.selectedModels],
            auditMode: this.selectedAuditModes
          });
          
          if (response.data && response.data.success) {
            // 合并结果
            allResults = allResults.concat(response.data.results);
            processedCount += currentBatch.length;
            
            // 更新进度
            this.auditProgress = processedCount;
        } else {
            throw new Error(response.data?.message || '测试批次失败');
          }
          
          // 短暂延迟，让UI有时间更新
          // await this.delay(100);
        }
        
        // 所有批次处理完成后，设置最终进度
        this.auditProgress = totalQuestions;
        
        // 处理结果
        const summary = this.calculateStatisticsFromResults(allResults);
        this.processResults(allResults, summary);
        
        this.$message.success(`成功完成${this.auditResults.length}条测试`);
      } catch (error) {
        console.error('测试失败:', error);
        this.$message.error(`测试失败: ${error.message || '请检查网络连接'}`);
      } finally {
        this.isAuditing = false;
        this.auditingQuestionIndex = -1;
      }
    },
    
    // 从结果中计算统计数据
    calculateStatisticsFromResults(results) {
      if (!results || results.length === 0) {
        return {
          totalCount: 0,
          avgResponseTime: 0,
          choiceCount: 0,
          choiceCorrectCount: 0,
          choiceCorrectRate: 0,
          essayCount: 0,
          essayAvgScore: 0
        };
      }

      const total = results.length;

      // 区分单选/判断题和问答题
      const choiceResults = results.filter(r => ['single', 'judge'].includes(r.questionType));
      const essayResults = results.filter(r => r.questionType === 'essay');

      // 单选/判断题统计 - 改为正确率而不是通过率
      const choiceCount = choiceResults.length;
      const choiceCorrectCount = choiceResults.filter(r => r.isCorrect || r.isPassed).length;
      const choiceCorrectRate = choiceCount > 0 ? Math.round((choiceCorrectCount / choiceCount) * 100) : 0;

      // 问答题统计
      const essayCount = essayResults.length;
      const essayTotalScore = essayResults.reduce((sum, r) => sum + (r.qualityScore || 0), 0);
      const essayAvgScore = essayCount > 0 ? parseFloat((essayTotalScore / essayCount).toFixed(1)) : 0;

      // 平均响应时间
      const avgResponse = parseFloat((results.reduce((sum, r) => sum + (r.responseTime || 0), 0) / total).toFixed(2));

      return {
        totalCount: total,
        avgResponseTime: avgResponse,
        choiceCount: choiceCount,
        choiceCorrectCount: choiceCorrectCount,
        choiceCorrectRate: choiceCorrectRate,
        essayCount: essayCount,
        essayAvgScore: essayAvgScore
      };
    },
    
    // 处理API返回的检测结果
    processResults(results, summary) {
      // 将API返回的结果转换为页面需要的格式
      this.auditResults = results.map(result => {
        // 确定题目类型的中文名称
        let questionTypeZh = '';
        if (result.questionType === 'single') {
          questionTypeZh = '选择题';
        } else if (result.questionType === 'judge') {
          questionTypeZh = '判断题';
        } else if (result.questionType === 'essay') {
          questionTypeZh = '问答题';
        }
        
        // 对前端进行适当处理
        if (result.questionType === 'essay') {
          // 问答题不再使用isPassed，使用qualityScore作为评估指标
          // 生成评分反馈
          if (!result.feedback) {
            if (result.qualityScore >= 8) {
              result.feedback = `评分 ${result.qualityScore}。解释全面，要点覆盖完整。`;
            } else if (result.qualityScore >= 6) {
              result.feedback = `评分 ${result.qualityScore}。回答基本正确，但可以更加详细。`;
            } else if (result.qualityScore >= 4) {
              result.feedback = `评分 ${result.qualityScore}。回答部分正确，但缺少关键要点。`;
            } else {
              result.feedback = `评分 ${result.qualityScore}。回答与题目关联性低，未能正确理解问题。`;
            }
          }
        } else {
          // 单选和判断题，将isPassed重命名为isCorrect，语义更准确
          result.isCorrect = result.isPassed;
          
          if (!result.feedback) {
            result.feedback = result.isCorrect ? 
              '答案正确。' : 
              `答案错误，正确答案是: ${result.standardAnswer}`;
          }
        }
        
        return {
          ...result,
          questionTypeZh: questionTypeZh || result.questionTypeZh
        };
      });
      
      // 如果有统计摘要信息，更新统计数据
      if (summary) {
        this.statsSummary = summary;
      } else {
        // 否则根据当前结果计算统计数据
        this.updateStatsSummary();
      }
      
      // 重置筛选和分页
      this.currentPage = 1;
      this.filterKeyword = '';
      this.filterQuestionType = '';
      this.filterDomain = '';
      this.filterSource = '';
      
      // 数据加载完成后初始化所有图表
      if (this.auditResults.length > 0) {
        this.$nextTick(() => {
          this.initializeAllCharts();
        });
      }
      
      // 保存数据到会话存储
      this.saveAuditResults();
    },
    
    // 标准化答案格式，便于比较（保留此方法，因为可能会在其他地方使用）
    normalizeAnswer(answer) {
      if (!answer) return '';
      // 移除空格、转为大写
      return String(answer).trim().toUpperCase();
    },
    
    // 清除所有测试结果
    clearResults() {
      this.clearAllResults();
    },
    
    showImportDialog() {
      this.importDialogVisible = true;
      this.fileInfo = null;
    },
    
    
    async handleImportConfirm() {
      if (this.questions.length > 0) {
        // 如果已有题目，询问是否覆盖
        this.$confirm({
          title: '已存在题目数据',
          content: `当前已有 ${this.questions.length} 道题目，确定要覆盖吗？`,
          okText: '确认',
          cancelText: '取消',
          onOk: () => {
            this.processImport();
          }
        });
      } else {
        this.processImport();
      }
    },
    
    async processImport() {
      this.isImporting = true;
      
      try {
          if (!this.fileInfo) {
            this.$message.warning('请先选择文件');
            this.isImporting = false;
            return;
          }
          
          await this.importFromFile();
        this.importDialogVisible = false;
      } catch (error) {
        console.error('导入题库失败:', error);
        this.$message.error(`导入题库失败: ${error.message || '请重试'}`);
      } finally {
        this.isImporting = false;
      }
    },
    
    beforeUpload(file) {
      // 检查文件类型
      if (file.type !== 'application/json' && !file.name.endsWith('.json')) {
        this.$message.error('只支持 JSON 格式文件');
        return false;
      }
      
      // 检查文件大小（限制为10MB）
      const isLt10M = file.size / 1024 / 1024 < 10;
      if (!isLt10M) {
        this.$message.error('文件大小不能超过 10MB');
        return false;
      }
      
      // 保存文件信息
      this.fileInfo = file;
      return false; // 阻止默认上传行为
    },
    
    async importFromFile() {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        
        reader.onload = e => {
          try {
            const data = JSON.parse(e.target.result);
            console.log('导入的JSON数据结构:', Object.keys(data));
            
            // 临时存储题目数组
            let questions = [];
            
            // 处理题库生成模块格式（data数组）
            if (data.data && Array.isArray(data.data)) {
              questions = [...data.data];
            }
            // 处理题库拓展模块格式（originalQuestions和transformedQuestions）
            else if (data.originalQuestions && data.transformedQuestions) {
              const originalQuestions = data.originalQuestions || [];
              const transformedQuestions = data.transformedQuestions || [];
              
              // 合并原始题目和变形题目
              questions = [...originalQuestions, ...transformedQuestions];
            }
            // 直接作为题目数组处理（如果是数组的话）
            else if (Array.isArray(data)) {
              questions = [...data];
            }
            // 尝试从对象中找到可能的题目数组
            else {
            const possibleArrays = Object.values(data).filter(value => Array.isArray(value) && value.length > 0);
            if (possibleArrays.length > 0) {
              // 使用最长的数组作为题目数据
                questions = possibleArrays.reduce((prev, current) => 
                (prev.length > current.length) ? prev : current
              );
              } else {
                // 如果没有找到有效的题目数据
                reject(new Error('文件格式不支持，请确保JSON文件包含题目数据。导入的数据结构: ' + JSON.stringify(Object.keys(data))));
              return;
              }
            }
            
            // 标准化题目格式，确保选项格式正确
            this.questions = questions.map(question => {
              const standardizedQuestion = { ...question };
              
              // 处理题目类型
              if (question.type === 'single' || question.type === 'judge' || question.题型 === '选择题' || question.题型 === '判断题') {
                // 确定题目类型
                standardizedQuestion.type = question.type || (question.题型 === '选择题' ? 'single' : 'judge');
                
                // 如果题目有options数组但没有"选项A"等格式，进行转换
                if (question.options && Array.isArray(question.options) && question.options.length > 0) {
                  // 保留原始的options数组
                  standardizedQuestion.options = [...question.options];
                  
                  // 同时添加"选项A"格式的选项，方便后端处理
                  question.options.forEach((option, index) => {
                    const letter = String.fromCharCode(65 + index); // A, B, C, D...
                    standardizedQuestion[`选项${letter}`] = option;
                  });
                }
                // 如果题目有"选项A"等格式但没有options数组，需要构建options数组
                else if (!question.options || !Array.isArray(question.options)) {
                  const options = [];
                  // 检查是否有"选项A"、"选项B"等格式
                  for (let i = 0; i < 8; i++) { // 最多支持8个选项
                    const letter = String.fromCharCode(65 + i); // A, B, C, D...
                    const key = `选项${letter}`;
                    if (question[key]) {
                      options.push(question[key]);
                    }
                  }
                  if (options.length > 0) {
                    standardizedQuestion.options = options;
                  }
                }
                
                // 标准化答案
                if (question.答案 && !question.answer) {
                  standardizedQuestion.answer = question.答案;
                } else if (question.answer && !question.答案) {
                  standardizedQuestion.答案 = question.answer;
                }
              }
              
              // 确保question/prompt字段存在
              if (question.prompt && !question.问题) {
                standardizedQuestion.问题 = question.prompt;
              } else if (question.问题 && !question.prompt) {
                standardizedQuestion.prompt = question.问题;
              }
              
              return standardizedQuestion;
            });
            
            this.$message.success(`成功导入 ${this.questions.length} 道题目`);
            console.log('标准化后的第一道题目样本:', this.questions[0]);
            resolve();
          } catch (error) {
            console.error('解析JSON文件失败:', error);
            reject(new Error('解析JSON文件失败: ' + error.message));
          }
        };
        
        reader.onerror = () => {
          reject(new Error('读取文件失败'));
        };
        
        reader.readAsText(this.fileInfo);
      });
    },
    
    async importFromGenerateModule() {
      try {
        const response = await axios.get('/api/questions/current-bank');
        
        if (response.data.success && response.data.data) {
          this.questions = response.data.data;
          this.$message.success(`成功从题库生成模块导入 ${this.questions.length} 道题目`);
        } else {
          throw new Error(response.data.message || '题库为空，请先在"题库生成"页面生成题目');
        }
      } catch (error) {
        throw new Error('导入题库生成模块数据失败: ' + (error.message || '请确保已生成题库'));
      }
    },
    
    async importFromExpansionModule() {
      try {
        const response = await axios.get('/api/questions/transformed-bank');
        
        if (response.data.success && response.data.data) {
          const { originalQuestions = [], transformedQuestions = [] } = response.data.data;
          
          // 合并原始题目和变形题目
          this.questions = [...originalQuestions, ...transformedQuestions];
          this.$message.success(`成功从题库拓展模块导入 ${this.questions.length} 道题目（原始题目: ${originalQuestions.length}, 变形题目: ${transformedQuestions.length}）`);
        } else {
          throw new Error(response.data.message || '拓展题库为空，请先在"题库拓展"页面生成变形题目');
        }
      } catch (error) {
        throw new Error('导入题库拓展模块数据失败: ' + (error.message || '请确保已生成拓展题库'));
      }
    },

    getResultHeader(result) {
      return result.question.slice(0, 50); // 截取前50个字符作为标题
    },

    getResultClass(result) {
      return {
        'pass': result.isPassed,
        'fail': !result.isPassed
      };
    },

    onSearch() {
      this.currentPage = 1; // 搜索后重置到第一页
    },

    onPageChange(page) {
      this.currentPage = page;
    },

    getPassRateColor() {
      return this.statsSummary.passRate > 80 ? 'success' : this.statsSummary.passRate > 50 ? 'warning' : 'error';
    },

    getAuditModeName(mode) {
      const modeNames = {
        'rule-based': '规则匹配',
        'model-assisted': '模型辅助',
      };
      
      if (Array.isArray(mode)) {
        return mode.map(m => modeNames[m] || m).join(' + ');
      }
      
      return modeNames[mode] || mode;
    },

    manualReview(result, index) {
      this.currentReviewItem = { ...result };
      this.currentReviewIndex = index;
      this.reviewModalVisible = true;
    },


    // 预览报告
    previewReport() {
      if (this.auditResults.length === 0) {
        this.$message.warning('无审计数据，无法生成报告');
        return;
      }
      
      // 设置预览可见
      this.reportPreviewVisible = true;
      
      // 预处理数据，确保可序列化
      const sanitizedResults = this.auditResults.map(result => {
        // 创建一个新对象，去除可能存在的不可序列化的字段
        const sanitized = { ...result };
        // 移除可能包含函数的字段
        delete sanitized.toJSON;
        delete sanitized.toString;
        
        // 确保所有字段都有值，防止NoneType和str比较错误
        for (const key in sanitized) {
          if (sanitized[key] === null || sanitized[key] === undefined) {
            sanitized[key] = ''; // 将null或undefined替换为空字符串
          } else if (typeof sanitized[key] === 'function') {
            delete sanitized[key]; // 移除函数
          }
        }
        return sanitized;
      });
      
      // 处理摘要数据，确保可序列化
      const sanitizedSummary = { ...this.statsSummary };
      for (const key in sanitizedSummary) {
        if (typeof sanitizedSummary[key] === 'function') {
          delete sanitizedSummary[key];
        } else if (sanitizedSummary[key] === null || sanitizedSummary[key] === undefined) {
          sanitizedSummary[key] = ''; // 将null或undefined替换为空字符串
        }
      }
      
      // 确保selectedAuditModes非空
      const auditModes = this.selectedAuditModes && this.selectedAuditModes.length 
        ? this.selectedAuditModes 
        : ['rule-based'];
      
      // 调用后端API预览报告
      axios.post('/api/audit/preview-report', {
        results: sanitizedResults,
        summary: sanitizedSummary,
        sections: this.reportSections,
        auditMode: auditModes // 添加检测模式信息
      }, {
        responseType: 'text' // 直接接收HTML文本响应
      })
      .then(response => {
        console.log('收到预览响应类型:', typeof response.data);
        
        // 找到预览容器
        const previewContainer = document.querySelector('.report-document');
        if (!previewContainer) {
          console.error('找不到预览容器 .report-document');
          return;
        }
        
        // 检查响应是否为HTML
        if (typeof response.data === 'string' && response.data.trim().startsWith('<!DOCTYPE html>')) {
          // 直接注入HTML内容
          previewContainer.innerHTML = response.data;
          // 尝试从HTML中提取模型名称
          const titleMatch = response.data.match(/<title>(.*?)<\/title>/);
          if (titleMatch && titleMatch[1]) {
            const modelName = titleMatch[1].replace(' 性能评估报告', '').trim();
            this.currentModel = modelName || this.selectedModels || '未知模型';
          }
        } 
        // 检查是否为JSON对象
        else if (typeof response.data === 'object' && response.data.success) {
          if (response.data.preview) {
            previewContainer.innerHTML = response.data.preview;
          }
          if (response.data.data && response.data.data.modelName) {
            this.currentModel = response.data.data.modelName || this.selectedModels || '未知模型';
          }
        } 
        // 如果响应是字符串但不是HTML
        else if (typeof response.data === 'string') {
          // 尝试解析为JSON
          try {
            const jsonData = JSON.parse(response.data);
            if (jsonData.success && jsonData.preview) {
              previewContainer.innerHTML = jsonData.preview;
            } else if (response.data.includes('<div')) {
              // 如果字符串包含div标签，可能是HTML片段
              previewContainer.innerHTML = response.data;
            } else {
              throw new Error('无法解析预览响应');
            }
          } catch (e) {
            // 可能是HTML片段或错误消息
            if (response.data.includes('<div')) {
              previewContainer.innerHTML = response.data;
            } else {
              console.error('预览报告解析错误:', e);
              this.$message.warning('预览报告格式异常，使用本地数据生成预览');
              this.calculateReportData();
            }
          }
        } else {
          // 无法处理的响应类型
          console.error('预览报告API返回未知格式:', response.data);
          this.$message.warning('使用本地数据生成预览，报告格式可能不完整');
          this.calculateReportData();
        }
      })
      .catch(error => {
        console.error('预览报告请求失败:', error);
        this.$message.warning('无法连接到服务器，使用本地数据生成预览');
        
        // 使用计算的数据生成简单预览
        this.calculateReportData();
      })
      .finally(() => {
        // 滚动到预览区域
        this.$nextTick(() => {
          const previewEl = document.querySelector('.report-preview-panel');
          if (previewEl) {
            previewEl.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
    },
    

    // 生成并导出报告
    generateReport() {
      if (this.auditResults.length === 0) {
        this.$message.warning('无审计数据，无法生成报告');
        return;
      }
      
      this.isGeneratingReport = true;
      
      // 构建下载URL
      const url = '/api/audit/generate-report';
      
      // 创建表单数据
      const formData = {
        results: this.auditResults,
        summary: this.statsSummary,
        format: this.reportFormat,
        sections: this.reportSections
      };
      
      // 使用axios发送请求并处理二进制响应
      axios({
        method: 'post',
        url: url,
        data: formData,
        responseType: 'blob', // 重要，表示期望收到二进制数据
      })
      .then(response => {
        // 创建Blob
        const blob = new Blob([response.data], {
          type: 'application/' + (this.reportFormat === 'pdf' ? 'pdf' : 'html')
        });
        
        // 根据报告格式决定操作
        if (this.reportFormat === 'html') {
          // HTML格式时，显示预览
          this.downloadReport(blob);
        } else {
          // PDF格式时，直接下载
          this.downloadReport(blob);
        }
        
        // 确保保存最新的审计结果
        this.saveAuditResults();
        
        this.$message.success(`报告生成成功`);
      })
      .catch(error => {
        console.error('生成报告失败:', error);
        this.$message.error('生成报告失败，请重试');
      })
      .finally(() => {
        this.isGeneratingReport = false;
      });
    },

    onShowSizeChange(current, pageSize) {
      this.pageSize = pageSize;
      this.currentPage = 1;
    },
    
    
    // 更新统计摘要
    updateStatsSummary() {
      const totalCount = this.auditResults.length;
      
      // 区分单选/判断题和问答题
      const choiceResults = this.auditResults.filter(item => 
        item.questionType === 'single' || item.questionType === 'judge'
      );
      const essayResults = this.auditResults.filter(item => 
        item.questionType === 'essay'
      );
      
      // 计算单选判断题的正确率
      const choiceCount = choiceResults.length;
      const choiceCorrectCount = choiceResults.filter(item => item.isCorrect || item.isPassed).length;
      const choiceCorrectRate = choiceCount > 0 ? Math.round((choiceCorrectCount / choiceCount) * 100) : 0;
      
      // 计算问答题的平均分
      const essayCount = essayResults.length;
      const essayTotalScore = essayResults.reduce((sum, item) => sum + (item.qualityScore || 0), 0);
      const essayAvgScore = essayCount > 0 ? +(essayTotalScore / essayCount).toFixed(1) : 0;
      
      // 计算总体通过率
      const passCount = this.auditResults.filter(item => item.isPassed).length;
      const passRate = totalCount > 0 ? Math.round((passCount / totalCount) * 100) : 0;
      
      // 使用问答题的平均分作为总体质量分数，而不是所有题型的平均
      const qualityScore = essayAvgScore;
      
      // 计算平均响应时间
      const totalResponseTime = this.auditResults.reduce((sum, item) => sum + item.responseTime, 0);
      const avgResponseTime = totalCount > 0 ? +(totalResponseTime / totalCount).toFixed(2) : 0;
      
      this.statsSummary = {
        totalCount,
        passCount,
        passRate,
        qualityScore,
        avgResponseTime,
        // 新增字段
        choiceCount,
        choicePassCount: choiceCorrectCount,
        choicePassRate: choiceCorrectRate,
        essayCount,
        essayAvgScore
      };
    },
    
    // 下载报告
    downloadReport(blob) {
      // 创建文件名（带有日期时间戳）
      const now = new Date();
      const timestamp = now.toISOString().replace(/[:.]/g, '-').slice(0, 19);
      const fileName = `大模型性能评估报告-${timestamp}.${this.reportFormat}`;
      
      // 创建下载链接
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', fileName);
      
      // 触发下载
      document.body.appendChild(link);
      link.click();
      
      // 清理
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    },
    
    // 辅助方法 - 延迟函数
    delay(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    },
    
    getModelLabel(modelValue) {
      const model = this.modelOptions.find(m => m.value === modelValue);
      return model ? model.label : '';
    },

    // 打开人工检测对话框
    openReview(result, index) {
      this.currentReviewItem = { ...result };
      this.currentReviewIndex = index;
      this.reviewModalVisible = true;
    },

    getScoreColor(score) {
      if (score >= 90) return '#52c41a'; // 绿色，高分
      if (score >= 75) return '#1890ff'; // 蓝色，良好分数
      if (score >= 60) return '#faad14'; // 黄色，中等分数
      return '#f5222d'; // 红色，低分
    },
    
    // 根据安全分数获取标签颜色
    getSafetyColor(score) {
      if (score >= 90) return '#52c41a'; // 安全 - 绿色
      if (score >= 70) return '#faad14'; // 警告 - 黄色
      return '#f5222d'; // 危险 - 红色
    },
    
    // 格式化评估指标数据以便于表格展示
    formatMetricsData(metrics) {
      if (!metrics) return [];
      
      // 按照重要性排序指标
      const orderedKeys = [
        "总分", "内容安全性", "隐私保护", 
        "相关性", "准确性", "完整性"
      ];
      
      return orderedKeys
        .filter(key => metrics[key] !== undefined)
        .map(key => ({
          name: key,
          value: metrics[key]
        }));
    },
    
    // 格式化反馈内容
    formatFeedback(feedback) {
      if (!feedback) return '';
      // 将换行符转换为HTML换行
      return feedback.replace(/\n/g, '<br>');
    },
    
    // 绘制雷达图的方法
    drawRadarChart(elementId, metricsData) {
      // 这里使用echarts或其他图表库绘制雷达图
      // 实际实现时需要引入相关库并完成绘制逻辑
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById(elementId);
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 准备雷达图数据，排除总分和模型评估字段
      const radarData = metricsData
        .filter(item => item.name !== "总分" && item.name !== "模型评估") // 不包括总分和模型评估
        .map(item => ({
          name: item.name,
          max: 100,
          value: item.value
        }));
      
      // 雷达图配置
      const option = {
        tooltip: {
          trigger: 'item'
        },
        radar: {
          indicator: radarData.map(item => ({
            name: item.name,
            max: 100
          })),
          radius: '65%'
        },
        series: [
          {
            type: 'radar',
            data: [
              {
                value: radarData.map(item => item.value),
                name: '模型表现',
                areaStyle: {
                  color: 'rgba(24, 144, 255, 0.3)'
                },
                lineStyle: {
                  color: '#1890ff'
                }
              }
            ]
          }
        ]
      };
      
      chart.setOption(option);
    },
    
    // 当展开行时绘制雷达图
    handleExpandRow(expanded, record) {
      if (expanded && record.evaluationMetrics) {
        // 使用setTimeout确保DOM已更新
        setTimeout(() => {
          const chartId = 'radar-chart-' + record.id;
          const metricsData = this.formatMetricsData(record.evaluationMetrics);
          this.drawRadarChart(chartId, metricsData);
        }, 100);
      }
    },
    
    // 获取所有模型的多维度评估数据
    getSummaryMetricsData() {
      if (!this.auditResults || this.auditResults.length === 0) return [];
      
      // 按评估维度组织数据
      const dimensionMap = {};
      const models = new Set();
      
      // 仅处理有评估数据的问答题记录
      this.auditResults
        .filter(result => result.evaluationMetrics && result.questionType === 'essay')
        .forEach(result => {
          const metrics = result.evaluationMetrics;
          const modelName = result.modelName;
          models.add(modelName);
          
          // 遍历每个维度的分数
          Object.keys(metrics).forEach(dimension => {
            // 跳过总分和模型评估标记
            if (dimension === '总分' || dimension === '模型评估' || dimension === '简要解释') return;
            
            if (!dimensionMap[dimension]) {
              dimensionMap[dimension] = { name: dimension, modelScores: {} };
            }
            
            // 为每个模型累计分数和计数
            if (!dimensionMap[dimension].modelScores[modelName]) {
              dimensionMap[dimension].modelScores[modelName] = {
                total: 0,
                count: 0
              };
            }
            
            dimensionMap[dimension].modelScores[modelName].total += metrics[dimension];
            dimensionMap[dimension].modelScores[modelName].count += 1;
          });
        });
      
      // 计算每个维度每个模型的平均分
      const result = Object.values(dimensionMap).map(item => {
        const avgScores = {};
        
        // 计算平均分
        Object.keys(item.modelScores).forEach(model => {
          const { total, count } = item.modelScores[model];
          avgScores[model] = count > 0 ? Math.round(total / count * 10) / 10 : 0;
        });
        
        return {
          name: item.name,
          modelScores: avgScores
        };
      });
      
      return result;
    },
    
    // 绘制多维度评估雷达图
    drawSummaryRadarChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('summary-radar-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 获取维度列表
      const metricsData = this.getSummaryMetricsData();
      if (metricsData.length === 0) return;
      
      const dimensions = metricsData.map(item => item.name);
      
      // 为每个模型准备数据
      const modelNames = Object.keys(metricsData[0].modelScores);
      const series = modelNames.map(modelName => {
        const data = metricsData.map(item => item.modelScores[modelName] || 0);
        
        return {
          name: modelName,
          type: 'radar',
          data: [{
            value: data,
            name: modelName
          }],
          areaStyle: {
            opacity: 0.3
          }
        };
      });
      
      // 配置雷达图
      const option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          data: modelNames,
          bottom: 0
        },
        radar: {
          indicator: dimensions.map(dim => ({
            name: dim,
            max: 100
          })),
          radius: '60%'
        },
        series
      };
      
      chart.setOption(option);
    },
    
    // 绘制安全性评估图表
    drawSafetyChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('safety-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 提取安全相关指标
      const safetyMetrics = ['内容安全性', '隐私保护', '相关性', '准确性'];
      const modelNames = new Set();
      const modelData = {};
      
      // 收集数据
      this.auditResults
        .filter(result => result.evaluationMetrics && result.questionType === 'essay')
        .forEach(result => {
          const metrics = result.evaluationMetrics;
          const modelName = result.modelName;
          modelNames.add(modelName);
          
          if (!modelData[modelName]) {
            modelData[modelName] = safetyMetrics.map(metric => ({
              metric,
              values: []
            }));
          }
          
          // 收集每个安全维度的分数
          safetyMetrics.forEach((metric, index) => {
            if (metrics[metric] !== undefined) {
              modelData[modelName][index].values.push(metrics[metric]);
            }
          });
        });
      
      // 计算平均分和分布
      const processedData = {};
      Object.keys(modelData).forEach(model => {
        processedData[model] = modelData[model].map(item => {
          // 计算平均分
          const avg = item.values.length > 0 
            ? item.values.reduce((sum, val) => sum + val, 0) / item.values.length
            : 0;
            
          // 分布统计
          const distribution = {
            excellent: 0, // 90-100
            good: 0,      // 75-89
            average: 0,   // 60-74
            poor: 0       // 0-59
          };
          
          item.values.forEach(val => {
            if (val >= 90) distribution.excellent++;
            else if (val >= 75) distribution.good++;
            else if (val >= 60) distribution.average++;
            else distribution.poor++;
          });
          
          return {
            metric: item.metric,
            average: Math.round(avg * 10) / 10,
            distribution,
            count: item.values.length
          };
        });
      });
      
      // 配置图表
      const series = [];
      const modelsList = Array.from(modelNames);
      
      // 为每个模型添加柱状图系列
      modelsList.forEach(model => {
        series.push({
          name: model,
          type: 'bar',
          barWidth: 20,
          data: processedData[model].map(item => item.average)
        });
      });
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            const modelName = params[0].seriesName;
            const metricName = safetyMetrics[params[0].dataIndex];
            const metricData = processedData[modelName].find(item => item.metric === metricName);
            
            let html = `<div><b>${modelName} - ${metricName}</b></div>`;
            html += `<div>平均分: ${metricData.average}</div>`;
            html += `<div>样本数: ${metricData.count}</div>`;
            html += `<div>分布:</div>`;
            html += `<div>优秀(90-100): ${metricData.distribution.excellent}</div>`;
            html += `<div>良好(75-89): ${metricData.distribution.good}</div>`;
            html += `<div>中等(60-74): ${metricData.distribution.average}</div>`;
            html += `<div>较差(0-59): ${metricData.distribution.poor}</div>`;
            
            return html;
          }
        },
        legend: {
          data: modelsList,
          bottom: 0
        },
        grid: {
          left: '0%',
          right: '0%',
          bottom: '0%',
          top: '0%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: safetyMetrics
        },
        yAxis: {
          type: 'value',
          max: 100,
          name: '安全评分'
        },
        series
      };
      
      chart.setOption(option);
    },
    
    // 在统计图表标签切换时初始化图表
    handleTabChange(key) {
      this.activeTab = key;
      
      // 如果切换到图表Tab，初始化图表
      if (key === '3') {
        // 延迟执行确保DOM已更新
        setTimeout(() => {
          this.drawChoicePerformanceChart();
          this.drawEssayQualityRadarChart();
          this.drawQuestionSourceChart();
          this.drawDomainDistributionChart();
          this.drawResourceUsageChart();
        }, 100);
      }
    },
    
    // 初始化所有图表
    initializeAllCharts() {
      // 延迟执行确保DOM已更新
      setTimeout(() => {
        this.drawChoicePerformanceChart();
        this.drawEssayQualityRadarChart();
        this.drawQuestionSourceChart();
        this.drawDomainDistributionChart();
        // 绘制资源使用趋势图
        this.drawResourceUsageChart();
        // 绘制其他图表...（如果有的话）
      }, 100);
    },
    
    // 绘制不同题型的模型表现图
    drawQuestionTypeChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('question-type-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 获取所有模型名称
      const modelNames = [...new Set(this.auditResults.map(item => item.modelName))];
      
      // 计算各模型在不同问题类型上的表现
      const questionTypeData = modelNames.map(model => {
        const modelResults = this.auditResults.filter(r => r.modelName === model);
        
        // 选择题通过率
        const singleResults = modelResults.filter(r => r.questionType === 'single');
        const singlePassRate = singleResults.length > 0
          ? singleResults.filter(r => r.isPassed).length / singleResults.length * 100
          : 0;
        
        // 判断题通过率
        const judgeResults = modelResults.filter(r => r.questionType === 'judge');
        const judgePassRate = judgeResults.length > 0
          ? judgeResults.filter(r => r.isPassed).length / judgeResults.length * 100
          : 0;
        
        // 问答题平均分
        const essayResults = modelResults.filter(r => r.questionType === 'essay');
        const essayAvgScore = essayResults.length > 0
          ? essayResults.reduce((sum, r) => sum + (r.qualityScore || 0), 0) / essayResults.length
          : 0;
          
        // 按领域分组的表现
        const domains = [...new Set(modelResults.filter(r => r.domain).map(r => r.domain))];
        const domainPerformance = domains.map(domain => {
          const domainResults = modelResults.filter(r => r.domain === domain);
          const domainPassRate = domainResults.length > 0
            ? domainResults.filter(r => r.isPassed).length / domainResults.length * 100
            : 0;
          return {
            domain,
            passRate: Math.round(domainPassRate * 10) / 10
          };
        });
        
        return {
          model,
          singlePassRate: Math.round(singlePassRate * 10) / 10,
          judgePassRate: Math.round(judgePassRate * 10) / 10,
          essayAvgScore: Math.round(essayAvgScore * 10) / 10,
          domainPerformance
        };
      });
      
      // 配置图表
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['选择题', '判断题', '问答题']
        },
        grid: {
          left: '0%',
          right: '0%',
          bottom: '0%',
          containLabel: true
        },
        xAxis: {
          type: 'value',
          name: '通过率/评分',
          max: 100
        },
        yAxis: {
          type: 'category',
          data: modelNames
        },
        series: [
          {
            name: '选择题',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: questionTypeData.map(item => item.singlePassRate)
          },
          {
            name: '判断题',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: questionTypeData.map(item => item.judgePassRate)
          },
          {
            name: '问答题',
            type: 'bar',
            stack: 'total',
            label: {
              show: true
            },
            emphasis: {
              focus: 'series'
            },
            data: questionTypeData.map(item => item.essayAvgScore)
          }
        ]
      };
      
      chart.setOption(option);
    },
    
    // 绘制资源消耗分析图
    drawResourceUsageChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('inference-time-chart');
      if (!chartDom) return;
      
      // 检查是否已有实例，如果有则直接使用
      let chart = this.$echarts.getInstanceByDom(chartDom);
      
      if (!chart) {
        // 创建新实例，并设置自适应大小
        chart = this.$echarts.init(chartDom, null, {
          renderer: 'canvas',
          useDirtyRect: false,
          width: 'auto',
          height: 'auto'
        });
      }
      
      // 如果没有数据，显示空图
      if (this.auditResults.length === 0) {
        chart.setOption({
          title: {
            text: '暂无资源消耗数据',
            left: 'center',
            top: 'center'
          }
        });
        return;
      }
      
      // 按题型分组计算平均推理时间
      const questionTypes = {
        'single': '选择题',
        'judge': '判断题', 
        'essay': '问答题'
      };
      
      const typeData = {};
      Object.keys(questionTypes).forEach(type => {
        const results = this.auditResults.filter(r => r.questionType === type);
        if (results.length > 0) {
          const avgTime = results.reduce((sum, r) => sum + (r.responseTime || 0), 0) / results.length;
          const avgTokens = type === 'essay' ? 2000 : type === 'judge' ? 1000 : 500; // 估计不同题型的平均token数量
          
          typeData[type] = {
            name: questionTypes[type],
            avgTime: avgTime,
            // 修改内存占用模拟公式：基础内存 + (prompt长度/1000) * 缩放因子 + 响应时间因素
            // 基础内存：6.5GB，缩放因子：0.5，时间影响：0.1GB/s
            avgMemory: parseFloat((6.5 + (avgTokens / 1000) * 0.5 + 0.1 * avgTime).toFixed(2)),
            // 修改计算资源消耗模拟公式：基础TFLOPS + 系数 * 响应时间
            // 基础TFLOPS：0.3，时间系数：0.2
            avgCompute: parseFloat((0.3 + 0.2 * avgTime).toFixed(2)),
          };
        }
      });
      
      // 按数据集来源分组计算平均推理时间
      const sourceData = {};
      this.auditResults.forEach(result => {
        if (result.source) {
          if (!sourceData[result.source]) {
            sourceData[result.source] = {
              count: 0,
              totalTime: 0,
              totalTokens: 0
            };
          }
          sourceData[result.source].count++;
          sourceData[result.source].totalTime += (result.responseTime || 0);
          // 根据题型估计token数量
          const estimatedTokens = result.questionType === 'essay' ? 2000 : 
                                result.questionType === 'judge' ? 1000 : 500;
          sourceData[result.source].totalTokens += estimatedTokens;
        }
      });
      
      // 处理数据来源数据为平均值
      Object.keys(sourceData).forEach(source => {
        const avgTime = sourceData[source].totalTime / sourceData[source].count;
        const avgTokens = sourceData[source].totalTokens / sourceData[source].count;
        sourceData[source].avgTime = avgTime;
        sourceData[source].avgMemory = parseFloat((6.5 + (avgTokens / 1000) * 0.5 + 0.1 * avgTime).toFixed(2));
        sourceData[source].avgCompute = parseFloat((0.3 + 0.2 * avgTime).toFixed(2));
      });
      
      // 按领域分组计算平均推理时间
      const domainData = {};
      this.auditResults.forEach(result => {
        if (result.domain) {
          if (!domainData[result.domain]) {
            domainData[result.domain] = {
              count: 0,
              totalTime: 0,
              totalTokens: 0
            };
          }
          domainData[result.domain].count++;
          domainData[result.domain].totalTime += (result.responseTime || 0);
          // 根据题型估计token数量
          const estimatedTokens = result.questionType === 'essay' ? 2000 : 
                                result.questionType === 'judge' ? 1000 : 500;
          domainData[result.domain].totalTokens += estimatedTokens;
        }
      });
      
      // 处理领域数据为平均值
      Object.keys(domainData).forEach(domain => {
        const avgTime = domainData[domain].totalTime / domainData[domain].count;
        const avgTokens = domainData[domain].totalTokens / domainData[domain].count;
        domainData[domain].avgTime = avgTime;
        domainData[domain].avgMemory = parseFloat((6.5 + (avgTokens / 1000) * 0.5 + 0.1 * avgTime).toFixed(2));
        domainData[domain].avgCompute = parseFloat((0.3 + 0.2 * avgTime).toFixed(2));
      });
      
      // 处理题型数据
      const typeNames = Object.keys(typeData).map(type => typeData[type].name);
      const typeTimes = Object.keys(typeData).map(type => parseFloat(typeData[type].avgTime.toFixed(2)));
      const typeMemories = Object.keys(typeData).map(type => typeData[type].avgMemory);
      const typeComputes = Object.keys(typeData).map(type => typeData[type].avgCompute);
      
      // 处理数据来源数据
      const sourceEntries = Object.entries(sourceData)
        .map(([source, data]) => ({
          name: source,
          count: data.count,
          avgTime: data.avgTime,
          avgMemory: data.avgMemory,
          avgCompute: data.avgCompute
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 100);
      
      const sourceNames = sourceEntries.map(entry => 
        entry.name.length > 8 ? entry.name.substring(0, 8) + '...' : entry.name
      );
      const sourceTimes = sourceEntries.map(entry => parseFloat(entry.avgTime.toFixed(2)));
      const sourceMemories = sourceEntries.map(entry => entry.avgMemory);
      const sourceComputes = sourceEntries.map(entry => entry.avgCompute);
      
      // 处理领域数据
      const domainEntries = Object.entries(domainData)
        .map(([domain, data]) => ({
          name: domain,
          count: data.count,
          avgTime: data.avgTime,
          avgMemory: data.avgMemory,
          avgCompute: data.avgCompute
        }))
        .sort((a, b) => b.count - a.count)
        .slice(0, 8);
      
      const domainNames = domainEntries.map(entry => 
        entry.name.length > 8 ? entry.name.substring(0, 8) + '...' : entry.name
      );
      const domainTimes = domainEntries.map(entry => parseFloat(entry.avgTime.toFixed(2)));
      const domainMemories = domainEntries.map(entry => entry.avgMemory);
      const domainComputes = domainEntries.map(entry => entry.avgCompute);
      
      // 创建选项卡式数据结构
      let currentTabIndex = 0; // 0: 题型, 1: 来源, 2: 领域
      
      const updateChart = (tabIndex) => {
        currentTabIndex = tabIndex;
        let xData, seriesData, memoryData, computeData, title;
        
        if (tabIndex === 0) {
          xData = typeNames;
          seriesData = typeTimes;
          memoryData = typeMemories;
          computeData = typeComputes;
        } else if (tabIndex === 1) {
          xData = sourceNames;
          seriesData = sourceTimes;
          memoryData = sourceMemories;
          computeData = sourceComputes;
        } else {
          xData = domainNames;
          seriesData = domainTimes;
          memoryData = domainMemories;
          computeData = domainComputes;
        }
        
        const colors = ['#1890ff', '#fa8c16', '#722ed1', '#52c41a', '#13c2c2', '#eb2f96', '#f5222d'];
        
        chart.setOption({
          title: {
            text: title,
            left: 'center',
            top: 0,
            textStyle: {
              fontSize: 14
            }
          },
          tooltip: {
            trigger: 'axis',
            formatter: function(params) {
              let originalName = '';
              if (tabIndex === 1 && params[0].name.includes('...')) {
                originalName = sourceEntries[params[0].dataIndex].name;
              } else if (tabIndex === 2 && params[0].name.includes('...')) {
                originalName = domainEntries[params[0].dataIndex].name;
              } else {
                originalName = params[0].name;
              }
              
              let result = `${originalName}<br/>`;
              params.forEach(param => {
                let unit = '';
                if (param.seriesName === '推理时间') unit = '秒';
                else if (param.seriesName === '内存占用') unit = 'GB';
                else if (param.seriesName === '计算量') unit = 'TFLOPS';
                
                result += `${param.seriesName}: ${param.value}${unit}<br/>`;
              });
              
              return result;
            }
          },
          legend: {
            data: ['推理时间', '内存占用', '计算量'],
            top: '8%'
          },
          grid: {
            left: '3%',
            right: '9%',
            bottom: '5%', 
            top: '25%',
            containLabel: true
          },
          xAxis: {
            type: 'category',
            data: xData,
            axisLabel: {
              interval: 0,
              rotate: xData.length > 3 ? 30 : 0,
              fontSize: 12
            }
          },
          yAxis: [
            {
            type: 'value',
              name: '时间(秒)',
              position: 'left',
              axisLine: {
                show: true,
                lineStyle: {
                  color: colors[0]
                }
              },
            axisLabel: {
              formatter: '{value}s'
            }
          },
            {
              type: 'value',
              name: '内存(GB)',
              position: 'right',
              offset: 0,
              min: 6,
              axisLine: {
                show: true,
                lineStyle: {
                  color: colors[1]
                }
              },
              axisLabel: {
                formatter: '{value}GB'
              }
            },
            {
              type: 'value',
              name: '计算量(TFLOPS)',
              position: 'right',
              offset: 80,
              min: 0.2,
              axisLine: {
                show: true,
                lineStyle: {
                  color: colors[2]
                }
              },
              axisLabel: {
                formatter: '{value}'
              }
            }
          ],
          series: [
            {
              name: '推理时间',
              type: 'bar',
              yAxisIndex: 0,
              barGap: '0%',
              data: seriesData,
                itemStyle: {
                color: colors[0]
              },
              label: {
                show: true,
                position: 'top',
                formatter: '{c}s'
              }
            },
            {
              name: '内存占用',
              type: 'bar',
              yAxisIndex: 1,
              barGap: '0%',
              data: memoryData,
              itemStyle: {
                color: colors[1]
              },
              label: {
                show: true,
                position: 'top',
                formatter: '{c}GB'
              }
            },
            {
              name: '计算量',
              type: 'line',
              yAxisIndex: 2,
              data: computeData,
              symbol: 'circle',
              symbolSize: 8,
              itemStyle: {
                color: colors[2]
              },
              lineStyle: {
                width: 2
              },
              label: {
                show: true,
                position: 'top',
                formatter: '{c}'
              }
            }
          ]
        });
      };
      
      // 添加自定义控件用于切换选项卡
      const tabOptions = ['按题型', '按来源', '按领域'];
      
      chart.setOption({
        toolbox: {
          feature: {
            myTool1: {
              show: true,
              title: tabOptions[0],
              icon: 'path://M932.4 156.9H91.6c-13.3 0-24.1-10.8-24.1-24.1s10.8-24.1 24.1-24.1h840.8c13.3 0 24.1 10.8 24.1 24.1s-10.8 24.1-24.1 24.1zM932.4 511.9H91.6c-13.3 0-24.1-10.8-24.1-24.1s10.8-24.1 24.1-24.1h840.8c13.3 0 24.1 10.8 24.1 24.1s-10.8 24.1-24.1 24.1zM932.4 866.8H91.6c-13.3 0-24.1-10.8-24.1-24.1s10.8-24.1 24.1-24.1h840.8c13.3 0 24.1 10.8 24.1 24.1s-10.8 24.1-24.1 24.1z',
              onclick: () => {
                updateChart(0);
              }
            },
            myTool2: {
              show: true,
              title: tabOptions[1],
              icon: 'path://M832 64H192c-17.7 0-32 14.3-32 32v832c0 17.7 14.3 32 32 32h640c17.7 0 32-14.3 32-32V96c0-17.7-14.3-32-32-32zm-260 72h96v209.9L621.5 312 572 347.4V136zm220 752H232V136h280v296.9c0 3.3 1 6.6 3 9.3a15.9 15.9 0 0 0 22.3 3.7l83.8-59.9 81.4 59.4c2.7 2 6 3.1 9.4 3.1 8.8 0 16-7.2 16-16V136h64v752z',
              onclick: () => {
                updateChart(1);
              }
            },
            myTool3: {
              show: true,
              title: tabOptions[2],
              icon: 'path://M512 140c-205.4 0-372 166.6-372 372s166.6 372 372 372 372-166.6 372-372-166.6-372-372-372zm128 320c0-4.4 3.6-8 8-8h48c4.4 0 8 3.6 8 8v48c0 4.4-3.6 8-8 8h-48c-4.4 0-8-3.6-8-8v-48zm176 0c0-4.4 3.6-8 8-8h48c4.4 0 8 3.6 8 8v48c0 4.4-3.6 8-8 8h-48c-4.4 0-8-3.6-8-8v-48zM464 512a48 48 0 1 0 96 0 48 48 0 1 0-96 0zm200-64c4.4 0 8 3.6 8 8v48c0 4.4-3.6 8-8 8h-48c-4.4 0-8-3.6-8-8v-48c0-4.4 3.6-8 8-8h48zm-256-64a48.01 48.01 0 0 1 0-96 48.01 48.01 0 0 1 0 96z',
              onclick: () => {
                updateChart(2);
              }
            }
          }
        }
      });
      
      // 默认显示领域面板
      updateChart(2);
    },
    
    
    
    // 加载保存的数据
    loadSavedResults() {
      try {
        // 从localStorage中获取数据
        const savedResults = localStorage.getItem('auditResults');
        const savedSummary = localStorage.getItem('auditSummary');
        const savedQuestions = localStorage.getItem('auditQuestions');
        
        if (savedResults && savedSummary) {
          this.auditResults = JSON.parse(savedResults);
          this.statsSummary = JSON.parse(savedSummary);
          
          if (savedQuestions) {
            this.questions = JSON.parse(savedQuestions);
          }
          
          // 加载后初始化图表
          if (this.auditResults.length > 0) {
            this.$nextTick(() => {
              this.initializeAllCharts();
            });
          }
          
          console.log('成功恢复检测数据:', this.auditResults.length);
        }
      } catch (error) {
        console.error('恢复保存的数据失败:', error);
      }
    },
    
    handleResize() {
      // 获取所有图表并调整大小
      const chartIds = [
        'choice-performance-chart',
        'correct-rate-pie-chart',
        'essay-quality-radar-chart',
        'question-source-chart',
        'domain-distribution-chart',
        'model-performance-chart',
        'inference-time-chart'
      ];
      
      chartIds.forEach(id => {
        const chartDom = document.getElementById(id);
        if (chartDom) {
          const chart = this.$echarts.getInstanceByDom(chartDom);
          if (chart) {
            chart.resize();
          }
        }
      });
    },
    
    // 绘制选择题和判断题表现柱状图
    drawChoicePerformanceChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('choice-performance-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 获取选择题、判断题和简答题数据
      const choiceResults = this.auditResults.filter(r => r.questionType === 'single');
      const judgeResults = this.auditResults.filter(r => r.questionType === 'judge');
      const essayResults = this.auditResults.filter(r => r.questionType === 'essay');
      
      // 计算选择题得分（正确率*100）
      const choiceScore = choiceResults.length > 0
        ? Math.round(choiceResults.filter(r => r.isPassed).length / choiceResults.length * 100)
        : 0;
        
      // 计算判断题得分（正确率*100）
      const judgeScore = judgeResults.length > 0
        ? Math.round(judgeResults.filter(r => r.isPassed).length / judgeResults.length * 100)
        : 0;
      
      // 计算简答题的平均分
      const essayAvgScore = essayResults.length > 0
        ? Math.round(essayResults.reduce((sum, r) => sum + (r.qualityScore || 0), 0) / essayResults.length * 10) / 10
        : 0;
      
      // 配置图表
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: '{b}: {c}分'
        },
        legend: {
          data: ['得分(百分制)']
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: ['选择题', '判断题', '问答题']
        },
        yAxis: {
          type: 'value',
          name: '得分',
          max: 100,
          axisLabel: {
            formatter: '{value}分'
          }
        },
        series: [
          {
            name: '得分(百分制)',
            type: 'bar',
            barWidth: '60%',
            data: [
              {
                value: choiceScore,
                itemStyle: {
                  color: '#1890ff'
                }
              },
              {
                value: judgeScore,
                itemStyle: {
                  color: '#52c41a'
                }
              },
              {
                value: essayAvgScore,
                itemStyle: {
                  color: '#722ed1'
                }
              }
            ],
            label: {
              show: true,
              position: 'top',
              formatter: '{c}分'
            }
          }
        ]
      };
      
      chart.setOption(option);
    },
    
    
    // 绘制问答题质量多维评分雷达图
    drawEssayQualityRadarChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('essay-quality-radar-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 获取所有问答题
      const essayResults = this.auditResults.filter(r => r.questionType === 'essay');
      
      // 如果没有问答题，显示空图
      if (essayResults.length === 0) {
        chart.setOption({
          title: {
            text: '暂无问答题数据',
            left: 'center',
            top: 'center',
            textStyle: {
              fontSize: 16,
              color: '#8c8c8c'
            }
          }
        });
        return;
      }
      
      // 汇总所有问答题的评估指标
      const dimensions = ['内容安全性', '隐私保护', '相关性', '准确性', '完整性'];
      let aggregatedMetrics = {};
      
      dimensions.forEach(dim => {
        aggregatedMetrics[dim] = 0;
      });
      
      let validResultsCount = 0;
      
      essayResults.forEach(result => {
        if (result.evaluationMetrics) {
          validResultsCount++;
          dimensions.forEach(dim => {
            aggregatedMetrics[dim] += result.evaluationMetrics[dim] || 0;
          });
        }
      });
      
      // 计算平均值
      if (validResultsCount > 0) {
        dimensions.forEach(dim => {
          aggregatedMetrics[dim] = Math.round(aggregatedMetrics[dim] / validResultsCount * 10) / 10;
        });
      }
      
      // 配置雷达图
      const option = {
        tooltip: {
          trigger: 'item'
        },
        radar: {
          indicator: dimensions.map(dim => ({
            name: dim,
            max: 100
          })),
          radius: '65%',
          shape: 'circle',
          splitNumber: 5,
          axisName: {
            color: '#555',
            fontSize: 12
          },
          splitArea: {
            areaStyle: {
              color: ['rgba(250, 250, 250, 0.3)', 'rgba(240, 240, 240, 0.3)']
            }
          }
        },
        series: [{
          type: 'radar',
          name: '问答题质量评分',
          data: [{
            value: dimensions.map(dim => aggregatedMetrics[dim]),
            name: '平均得分',
            symbol: 'circle',
            symbolSize: 6,
            areaStyle: {
              color: 'rgba(65, 105, 225, 0.3)'
            },
            lineStyle: {
              width: 2,
              color: 'rgba(65, 105, 225, 0.8)'
            },
            itemStyle: {
              color: 'rgba(65, 105, 225, 1)',
              borderColor: '#fff',
              borderWidth: 2
            }
          }]
        }]
      };
      
      chart.setOption(option);
    },
    
    // 绘制题目来源分布饼图
    drawQuestionSourceChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('question-source-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 统计题目来源分布
      const sourceMap = {};
      
      this.auditResults.forEach(result => {
        const source = result.source;
        
        if (!sourceMap[source]) {
          sourceMap[source] = 0;
        }
        
        sourceMap[source]++;
      });
      
      // 转换为图表数据格式
      let sourceEntries = Object.entries(sourceMap)
        .map(([name, value]) => ({ name, value }))
        .sort((a, b) => b.value - a.value);
      
      // 如果来源过多，只保留前7个，其余归为"其他"类别
      let sourceData = [];
      if (sourceEntries.length > 7) {
        const topSources = sourceEntries.slice(0, 7);
        const otherSources = sourceEntries.slice(7);
        
        const otherValue = otherSources.reduce((sum, item) => sum + item.value, 0);
        
        sourceData = [
          ...topSources,
          {
            name: '其他来源',
            value: otherValue
          }
        ];
      } else {
        sourceData = sourceEntries;
      }
      
      // 如果没有数据，显示空图
      if (sourceData.length === 0) {
        chart.setOption({
          title: {
            text: '暂无来源数据',
            left: 'center',
            top: 'center'
          }
        });
        return;
      }
      
      // 生成颜色列表
      const colors = [
        '#1890ff', '#52c41a', '#722ed1', '#fa8c16', 
        '#13c2c2', '#eb2f96', '#f5222d', '#faad14'
      ];
      
      // 计算总数用于百分比显示
      const total = sourceData.reduce((sum, item) => sum + item.value, 0);
      
      // 配置饼图
      const option = {
        color: colors,
        tooltip: {
          trigger: 'item',
          formatter: (params) => {
            const percentage = ((params.value / total) * 100).toFixed(2);
            return `${params.name}<br/>${params.value}题 (${percentage}%)`;
          }
        },
        legend: {
          type: 'scroll',
          orient: 'horizontal',
          bottom: 0,
          left: 'center',
          itemWidth: 12,
          itemHeight: 12,
          textStyle: {
            fontSize: 12
          },
          pageIconSize: 12,
          tooltip: {
            show: true,
            formatter: (params) => {
              const item = sourceData.find(item => item.name === params.name);
              if (!item) return params.name;
              const percentage = ((item.value / total) * 100).toFixed(2);
              return `${params.name}: ${item.value}题 (${percentage}%)`;
            }
          }
        },
        series: [
          {
            name: '题目来源',
            type: 'pie',
            radius: ['35%', '65%'],
            center: ['50%', '45%'],
            avoidLabelOverlap: true,
            itemStyle: {
              borderRadius: 4,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: true,
              position: 'outside',
              formatter: (params) => {
                const percentage = ((params.value / total) * 100).toFixed(1);
                if (percentage < 3) return ''; // 小于3%的不显示标签
                return `${params.name}: ${percentage}%`;
              },
              fontSize: 12
            },
            labelLine: {
              length: 10,
              length2: 10,
              smooth: true
            },
            emphasis: {
              label: {
                show: true,
                fontSize: 14,
                fontWeight: 'bold'
              },
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            data: sourceData
          }
        ]
      };
      
      chart.setOption(option);
    },
    
    // 绘制领域分布与得分图表
    drawDomainDistributionChart() {
      if (!this.$echarts) return;
      
      const chartDom = document.getElementById('domain-distribution-chart');
      if (!chartDom) return;
      
      const chart = this.$echarts.init(chartDom);
      
      // 统计各个领域的得分数据
      const domainData = {};
      
      // 首先收集所有领域
      this.auditResults.forEach(result => {
        const domain = result.domain || 'other domain';
        if (!domainData[domain]) {
          domainData[domain] = {
            // 总得分
            totalScore: 0,
            // 题目总数
            totalCount: 0,
            // 题目明细
            singleCount: 0,
            singleCorrect: 0,
            judgeCount: 0,
            judgeCorrect: 0,
            essayCount: 0,
            essayTotalScore: 0
          };
        }
        
        // 区分题型并记录数据
        domainData[domain].totalCount++;
        
        if (result.questionType === 'single') {
          // 选择题
          domainData[domain].singleCount++;
          if (result.isPassed) {
            domainData[domain].singleCorrect++;
            // 选择题正确计100分
            domainData[domain].totalScore += 100;
          }
        } else if (result.questionType === 'judge') {
          // 判断题
          domainData[domain].judgeCount++;
          if (result.isPassed) {
            domainData[domain].judgeCorrect++;
            // 判断题正确计100分
            domainData[domain].totalScore += 100;
          }
        } else if (result.questionType === 'essay') {
          // 问答题
          domainData[domain].essayCount++;
          const score = result.qualityScore || 0;
          domainData[domain].essayTotalScore += score;
          // 问答题直接使用原始分数
          domainData[domain].totalScore += score;
        }
      });
      
      // 转换为图表所需的数据格式
      // 只保留有题目的领域，并按题目数量排序
      const domainEntries = Object.entries(domainData)
        .filter(([_, data]) => data.totalCount > 0)
        .sort((a, b) => b[1].totalCount - a[1].totalCount);
        
      // 如果领域过多，只取前8个
      const topDomains = domainEntries.slice(0, 8);
      
      // 计算各领域的平均得分
      const domains = topDomains.map(([domain]) => domain);
      const domainAvgScores = topDomains.map(([_, data]) => {
        if (data.totalCount === 0) return 0;
        // 计算平均分数
        return Math.round(data.totalScore / data.totalCount * 10) / 10;
      });
      
      // 如果没有数据，显示空图
      if (domains.length === 0) {
        chart.setOption({
          title: {
            text: '暂无领域数据',
            left: 'center',
            top: 'center'
          }
        });
        return;
      }
      
      // 配置图表
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          },
          formatter: function(params) {
            const domain = params[0].name;
            const score = params[0].value;
            const data = topDomains.find(([d]) => d === domain)[1];
            
            let result = `<div style="font-weight:bold">${domain}</div>`;
            result += `<div>平均得分: ${score}分</div>`;
            result += `<div>题目总数: ${data.totalCount}题</div>`;
            
            // 添加题型明细
            if (data.singleCount > 0) {
              const singleAccuracy = Math.round(data.singleCorrect / data.singleCount * 100);
              result += `<div>选择题: ${data.singleCount}题 (正确率${singleAccuracy}%)</div>`;
            }
            
            if (data.judgeCount > 0) {
              const judgeAccuracy = Math.round(data.judgeCorrect / data.judgeCount * 100);
              result += `<div>判断题: ${data.judgeCount}题 (正确率${judgeAccuracy}%)</div>`;
            }
            
            if (data.essayCount > 0) {
              const essayAvg = Math.round(data.essayTotalScore / data.essayCount * 10) / 10;
              result += `<div>问答题: ${data.essayCount}题 (平均${essayAvg}分)</div>`;
            }
            
            return result;
          }
        },
        grid: {
          left: '0%',
          right: '0%',
          bottom: '0%',
          top: '10%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          data: domains,
          axisLabel: {
            interval: 0,
            rotate: domains.length > 5 ? 30 : 0,
            fontSize: 12
          }
        },
        yAxis: {
          type: 'value',
          name: '平均得分',
          min: 0,
          max: 100,
          axisLabel: {
            formatter: '{value}分'
          }
        },
        series: [
          {
            name: '领域平均得分',
            type: 'bar',
            barWidth: '60%',
            data: domainAvgScores.map((score, index) => ({
              value: score,
              // 根据分数设置不同颜色
              itemStyle: {
                color: score >= 80 ? '#52c41a' : (score >= 60 ? '#faad14' : '#f5222d')
              }
            })),
            label: {
              show: true,
              position: 'top',
              formatter: '{c}分',
              fontSize: 12
            }
          }
        ]
      };
      
      chart.setOption(option);
    },
    
    getLongestResponseType() {
      if (this.auditResults.length === 0) return '未知';
      
      // 按题型分组计算平均响应时间
      const questionTypes = {
        'single': '选择题',
        'judge': '判断题', 
        'essay': '问答题'
      };
      
      const typeAvgTimes = {};
      
      Object.keys(questionTypes).forEach(type => {
        const results = this.auditResults.filter(r => r.questionType === type);
        if (results.length > 0) {
          typeAvgTimes[type] = {
            name: questionTypes[type],
            avgTime: results.reduce((sum, r) => sum + (r.responseTime || 0), 0) / results.length
          };
        }
      });
      
      // 找出平均响应时间最长的题型
      let maxTime = 0;
      let slowestType = '未知';
      
      for (const type in typeAvgTimes) {
        if (typeAvgTimes[type].avgTime > maxTime) {
          maxTime = typeAvgTimes[type].avgTime;
          slowestType = typeAvgTimes[type].name;
        }
      }
      
      return slowestType;
    },
    
    
    // 计算报告数据
    calculateReportData() {
      // 当前模型名称
      this.currentModel = this.selectedModels || '未选择';
      
      // 计算统计指标
      let totalResponseTime = 0;
      let correctCount = 0;
      let totalInferenceTime = 0;
      let totalMemoryUsage = 0;
      let totalComputeLoad = 0;
      let essayScoreSum = 0;
      let essayCount = 0;
      let maxResponseTime = 0;
      
      // 题型响应时间统计
      const typeTimes = {
        single: [],
        judge: [],
        essay: []
      };
      
      this.auditResults.forEach(result => {
        // 响应时间
        if (result.responseTime) {
          totalResponseTime += result.responseTime;
          
          // 按题型记录响应时间
          if (typeTimes[result.questionType]) {
            typeTimes[result.questionType].push(result.responseTime);
          }
        }
        
        // 正确率
        if (result.isPassed) {
          correctCount++;
        }
        
        // 推理时间
        if (result.inferenceTime) {
          totalInferenceTime += result.inferenceTime;
        }
        
        // 内存使用
        if (result.memoryUsage) {
          totalMemoryUsage += result.memoryUsage;
        }
        
        // 计算负载
        if (result.computeLoad) {
          totalComputeLoad += result.computeLoad;
        }
        
        // 问答题分数
        if (result.questionType === 'essay' && result.qualityScore) {
          essayScoreSum += result.qualityScore;
          essayCount++;
        }
      });
      
      // 计算平均值
      this.averageResponseTime = this.auditResults.length > 0 
        ? Math.round(totalResponseTime / this.auditResults.length) 
        : 0;
        
      this.correctRate = this.auditResults.length > 0 
        ? Math.round(correctCount / this.auditResults.length * 100) 
        : 0;
        
      this.averageInferenceTime = this.auditResults.length > 0 
        ? Math.round(totalInferenceTime / this.auditResults.length) 
        : 0;
        
      this.averageMemoryUsage = this.auditResults.length > 0 
        ? Math.round(totalMemoryUsage / this.auditResults.length) 
        : 0;
        
      this.averageComputeLoad = this.auditResults.length > 0 
        ? Math.round(totalComputeLoad / this.auditResults.length) 
        : 0;
        
      this.essayAverageScore = essayCount > 0 
        ? Math.round(essayScoreSum / essayCount * 10) / 10 
        : 0;
        
      // 计算题型最大响应时间
      let maxType = '';
      let maxTypeTime = 0;
      
      for (const type in typeTimes) {
        if (typeTimes[type].length > 0) {
          const avgTime = typeTimes[type].reduce((sum, time) => sum + time, 0) / typeTimes[type].length;
          if (avgTime > maxTypeTime) {
            maxTypeTime = avgTime;
            maxType = type;
          }
        }
      }
      
      this.maxTypeResponseTime = Math.round(maxTypeTime);
    },
  
    
    // 获取格式名称
    getFormatName(format) {
      const formatNames = {
        pdf: 'PDF',
        html: 'HTML'
      };
      
      return formatNames[format] || format;
    },
  

    // closeReportPreview 方法 - 关闭报告预览
    closeReportPreview() {
      this.reportPreviewVisible = false;
      
      // 清空report-document内的内容
      const reportDocument = document.querySelector('.report-document');
      if (reportDocument) {
        reportDocument.innerHTML = '';
      }
    },
    
    // 从会话存储中加载数据
    loadSessionData() {
      try {
        // 加载题库数据
        const sessionData = sessionStorage.getItem('questionBank');
        if (sessionData) {
          const parsedQuestions = JSON.parse(sessionData);
          // 更新题库选择列表
          this.availableQuestions = parsedQuestions.map(q => ({
            id: q.id,
            prompt: q.prompt,
            type: q.type,
            selected: true
          }));
          
          // 按题型分组
          this.updateQuestionGroups(this.availableQuestions);
          console.log(`已从会话中恢复${this.availableQuestions.length}道题目`);
        } 
        
        // 加载审计结果
        const auditData = sessionStorage.getItem('auditResults');
        if (auditData) {
          this.auditResults = JSON.parse(auditData);
          console.log(`已从会话中恢复${this.auditResults.length}条审计结果`);
          
          if (this.auditResults.length > 0) {
            // 重新计算统计数据
            this.statsSummary = this.calculateStatisticsFromResults(this.auditResults);
            
            // 数据加载完成后初始化所有图表
            this.$nextTick(() => {
              this.initializeAllCharts();
            });
          }
        }
      } catch (error) {
        console.error('从会话加载数据失败:', error);
      }
    },
    
    // 清空所有审计结果
    clearAllResults() {
      this.$confirm({
        title: '确认清空所有结果',
        content: '此操作将删除所有测试结果，无法恢复。确定要继续吗？',
        okText: '确定',
        okType: 'danger',
        cancelText: '取消',
        onOk: () => {
          this.auditResults = [];
          this.statsSummary = null;
          
          // 清空会话存储
          sessionStorage.removeItem('auditResults');
          
          // 清空图表
          this.destroyCharts();
          
          this.$message.success('已清空所有测试结果');
        },
      });
    },
  },
  // 生命周期钩子
  mounted() {
    // 添加窗口大小变化监听器
    window.addEventListener('resize', this.handleResize);
    
    // 延迟初始化图表，确保DOM已渲染
    this.$nextTick(() => {
      this.initializeAllCharts();
    });
  },
  
  updated() {
    // 组件更新后重新调整图表大小
    this.$nextTick(() => {
      this.handleResize();
    });
  },
  
  // 销毁前清理
  beforeDestroy() {
    // 移除窗口大小变化监听器
    window.removeEventListener('resize', this.handleResize);
  },
};
</script>

<style lang="scss" scoped>
.data-audit-container {
  padding: 10px;
}
.header-card{
  background: linear-gradient(135deg, #f5f7fa, #ebf0f6);
}
.mb-5 {
  margin-bottom: 5px;
}

.mb-15 {
  margin-bottom: 15px;
}

.mb-24 {
  margin-bottom: 24px;
}

.font-bold {
  font-weight: 600;
  color: #1f2937;
}

.card-header {
  display: flex;
  flex-direction: column;
  margin-bottom: 1.5rem;
  position: relative;
  text-align: center;
}

.card-header h3 {
  font-size: 18px;
  margin-bottom: 8px;
  color: #1f2937;
}

.control-panel{
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s;
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


.audit-btn {
  margin-top: 24px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-content {
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-content svg {
  margin-right: 8px;
}

.audit-results {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stat-card {
  height: 100px;
  border-radius: 12px;
  background-color: white;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 16px;
  display: flex;
  align-items: center;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
  color: white;
}

.quality-icon {
  background-color: #1890ff;
}

.distribution-icon {
  background-color: #fa8c16;
}

.validity-icon {
  background-color: #52c41a;
}

.difficulty-icon {
  background-color: #722ed1;
}

.stat-content {
  flex: 1;
}

.stat-title {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
  margin-bottom: 4px;
}

.stat-value {
  font-size: 24px;
  font-weight: 600;
  color: #1f2937;
}
.aaa{
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 8px;
  color: #1f2937;
}
.questions-display,
.empty-state-card {
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
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

.import-options {
  padding: 8px 0;
}

.import-radio-group {
  display: flex;
  gap: 16px;
  width: 100%;
}

.file-upload-area {
  margin-top: 16px;
}

.file-info {
  margin-top: 16px;
}

.ant-upload-drag-icon {
  margin-bottom: 8px;
}

.ant-upload-text {
  margin-bottom: 4px;
  font-size: 16px;
}

.ant-upload-hint {
  font-size: 13px;
  color: rgba(0, 0, 0, 0.45);
}

.import-module-message {
  margin-top: 16px;
}

.section-container {
  margin-bottom: 15px;
}

.section-icon {
  margin-right: 8px;
}

.model-select {
  width: 100%;
}

.select-tip {
  margin-left: 18px;
  font-size: 13px;
  color: rgba(0, 0, 0, 0.45);
}

.audit-mode-cards {
  display: flex;
  gap: 16px;
  margin-top: 12px;
  margin-bottom: 24px;
}

.audit-mode-card {
  width: 48%;
  padding: 12px;
  border: 1px solid #d9d9d9;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  align-items: center;
  position: relative;

  &:hover {
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transform: translateY(-2px);
  }

  &.active {
    border-color: #1890ff;
    background-color: #e6f7ff;
  }

  .mode-icon {
    width: 44px;
    height: 44px;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(24, 144, 255, 0.1);
    border-radius: 8px;
    margin-right: 12px;
  }
  
  .mode-rule-based {
    background-color: rgba(24, 144, 255, 0.1);
    color: #1890ff;
  }
  
  .mode-model-assisted {
    background-color: rgba(82, 196, 26, 0.1);
    color: #52c41a;
  }

  .mode-content {
    text-align: left;
    flex: 1;
  }

  .mode-title {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
  }

  .mode-desc {
    font-size: 13px;
    color: rgba(0, 0, 0, 0.65);
  }
  
  .mode-checkbox {
    margin-left: 8px;
  }
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 48px;
}

.loading-text {
  margin-top: 16px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.result-display-card {
  margin-top: 24px;
}

.result-tabs {
  .ant-tabs-nav {
    margin-bottom: 0;
  }
}

.filter-row {
  margin-bottom: 20px;
}

.result-list {
  .ant-collapse-header {
    padding: 8px 0;
  }
}

.result-detail {
  .section-header {
    margin-bottom: 8px;
  }
}

.detail-section {
  margin-bottom: 16px;
}

.section-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.section-header svg {
  margin-right: 8px;
}

.input-content {
  margin-bottom: 8px;
}

.output-content {
  margin-bottom: 8px;
}

.audit-result {
  margin-bottom: 16px;
}

.result-items {
  margin-bottom: 8px;
}

.item-label {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.item-value {
  font-size: 14px;
  font-weight: 600;
  color: #1f2937;
}

.feedback-section {
  margin-top: 8px;
}

.feedback-header {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 8px;
}

.feedback-content {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.action-section {
  margin-top: 16px;
}

.empty-results {
  text-align: center;
  padding: 48px;
}

.report-container {
  padding: 24px;
}

.report-options {
  margin-bottom: 24px;
}

.report-actions {
  text-align: right;
}

.report-preview {
  margin-top: 24px;
}

.preview-container {
  text-align: center;
}

.preview-placeholder {
  display: inline-block;
}

.preview-text {
  margin-top: 16px;
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.review-modal-content {
  padding: 24px;
}

.review-question-card {
  margin-bottom: 16px;
}

.review-question-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.review-question-index {
  font-size: 14px;
  font-weight: 600;
}

.review-question-content {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.review-answer-card {
  margin-bottom: 16px;
}

.review-answer-content {
  margin-bottom: 8px;
}

.review-answer-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.review-meta-item {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.review-result-radio {
  margin-bottom: 16px;
}

.review-actions {
  text-align: right;
}

// 新增样式 - 保留
.question-cell {
  display: flex;
  align-items: center;
  
  .question-index {
    background-color: rgba(24, 144, 255, 0.1);
    color: #1890ff;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    margin-right: 10px;
    flex-shrink: 0;
  }
  
  .question-text {
    flex: 1;
    overflow: hidden;
    text-overflow: ellipsis;
  }
}

.essay-answer {
  max-height: 200px;
  overflow-y: auto;
  white-space: pre-wrap;
  background-color: #f8f8f8;
  padding: 8px;
  border-radius: 4px;
}

.expanded-row-detail {
  padding: 16px;
  
  .detail-card {
    margin-bottom: 16px;
    
    .answer-detail {
      max-height: 300px;
      overflow-y: auto;
      background-color: #f5f5f5;
      padding: 12px;
      border-radius: 4px;
      white-space: pre-wrap;
      font-family: 'Courier New', monospace;
    }
  }
  
  .metrics-card {
    margin-bottom: 16px;
    
    .metrics-radar-chart {
      height: 300px;
      margin-bottom: 16px;
    }
    
    .metrics-table {
      margin-top: 16px;
    }
  }
  
  .feedback-content {
    padding: 8px 0;
  }
}

.radar-chart-wrapper {
  height: 400px;
  width: 100%;
}

.chart-wrapper {
  height: 300px;
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.metrics-table-container {
  padding: 16px;
  background-color: #f9fafb;
  border-radius: 8px;
}

.model-scores {
  display: flex;
  flex-direction: column;
}

.model-score-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.model-name {
  width: 100px;
  flex-shrink: 0;
  font-weight: 500;
}

.metrics-name {
  font-weight: 600;
  color: rgba(0, 0, 0, 0.85);
}

// 新增样式末尾添加
.transform-item {
  height: 88px;
  display: flex;
  align-items: center;
  padding: 16px;
  border-radius: 16px;
  margin-bottom: 16px;
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
  font-size: 16px;
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

// 题目列表样式
.questions-list {
  margin-bottom: 24px;
}
.questions-play{
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.question-panel {
  margin-bottom: 16px;
  
  &.pass-panel {
    .ant-collapse-header {
      color: #52c41a;
    }
  }
  
  &.fail-panel {
    .ant-collapse-header {
      color: #f5222d;
    }
  }
}

.question-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.original-question-section, 
.transformed-question-section {
  border: 1px solid #ebedf0;
  border-radius: 8px;
  padding: 16px;
  height: 100%;
}

.original-question-section {
  background-color: #f9fafb;
}

.transformed-question-section {
  background-color: #f0f9ff;
  
  &.invalid-transformation {
    background-color: #fff1f0;
    border-color: #ffccc7;
  }
}

.options-list {
  display: flex;
  flex-direction: column;
}

.option-item {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.option-letter {
  font-size: 14px;
  font-weight: 600;
  margin-right: 8px;
}

.option-text {
  font-size: 14px;
  color: rgba(0, 0, 0, 0.65);
}

.chart-placeholder {
  background-color: #f9fafb;
  border-radius: 8px;
  padding: 32px;
  min-height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-content {
  color: #8c8c8c;
  font-size: 16px;
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
.pagination-info {
  padding-top: 15px;
}

.chart-panel {
  margin-top: 45px;
  border-radius: 12px;
  transition: all 0.3s;
  border-top: 1px dashed #e5e7eb;
}


.chart-container {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 10px;
  min-height: 300px;
  height: 100%;
  width: 100%;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}


.chart-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #1f2937;
  text-align: center;
}

.chart-container:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  cursor: pointer;
}

.response-time-chart {
  height: 400px;
  width: 100%;
}

.question-type-chart {
  height: 400px;
  width: 100%;
}

.resource-usage-chart {
  height: 400px;
  width: 100%;
}

.a-card .chart-container {
  box-shadow: none;
  margin-bottom: 0;
  height: 100%;
}

.a-card .chart-wrapper {
  height: 100%;
  min-height: 280px;
}

/* 响应式调整 */
@media (max-width: 1200px) {
  .a-card .chart-wrapper {
    min-height: 250px;
  }
}

@media (max-width: 768px) {
  .a-card .chart-wrapper {
    min-height: 220px;
  }
}

.filtered-content {
  margin: 8px 0;
  border-left: 3px solid #faad14;
  padding-left: 8px;
}

.essay-answer {
  white-space: pre-wrap;
  max-height: 300px;
  overflow-y: auto;
  padding: 8px;
  background-color: #f9f9f9;
  border-radius: 4px;
}

.expanded-row .expanded-row-detail {
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 增强展开动画效果 */
.ant-table-expanded-row {
  overflow: hidden;
}

.ant-table-expanded-row .expanded-row-detail {
  animation: expandAnimation 0.5s ease;
  transform-origin: top;
}

@keyframes expandAnimation {
  0% {
    opacity: 0;
    transform: scaleY(0.6) translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: scaleY(1) translateY(0);
  }
}

.audit-table{
  margin-bottom: 24px;
  width: 100%; // 确保宽度占满父容器
  overflow-x: auto; // 当内容溢出时提供水平滚动
  
}
.detail-button {
  transition: transform 0.3s ease;
}

.detail-button:hover {
  transform: scale(1.3);
  color: #1890ff;
}

/* 报告生成相关样式 */
.report-card {
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
  overflow: hidden;
  border: 1px solid #f0f2f5;
}

.report-config-panel {
  padding: 24px;
  background-color: #f9fafb;
  border-radius: 8px;
  height: 100%;
  border: 1px solid #f0f2f5;
}

.config-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 24px;
  position: relative;
  text-align: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #cfd1d7;
}

.format-form-item {
  margin-bottom: 24px;
  font-weight: bold;
}

.format-form-item :deep(.ant-form-item-label) {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 15px;
  color: #1f2937;
}

.content-form-item {
  margin-bottom: 28px;
  font-weight: bold;
  border-bottom: 1px solid #cfd1d7;
}

.content-form-item :deep(.ant-form-item-label) {
  font-weight: 600;
  margin-bottom: 8px;
  font-size: 15px;
  color: #1f2937;
}

.format-radio-group {
  display: flex;
  gap: 16px;
  width: 100%;
}

.format-radio-button {
  flex: 1;
  text-align: center;
  height: 46px;
  line-height: 46px;
  border-radius: 8px;
}

.format-icon {
  margin-right: 8px;
  font-size: 16px;
}

.format-text {
  font-size: 15px;
  font-weight: 500;
}

.content-checkbox-group {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.checkbox-row {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

.checkbox-item {
  display: flex;
  align-items: center;
  width: 48%;
}

.content-checkbox {
  font-size: 14px;
}

.report-action-buttons {
  display: flex;
  justify-content: space-between;
  margin-top: 32px;
  gap: 12px;
}

.custom-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 15px;
  font-weight: 500;
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  flex: 1;
  outline: none;
}

.custom-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.custom-button .anticon {
  margin-right: 8px;
  font-size: 16px;
}

.preview-button {
  background-color: #f9f9f9;
  border: 1px solid #e8e8e8;
  color: #333;
}

.preview-button:hover {
  background-color: #f0f9ff;
  transform: translateY(-2px);
  border-color: #1890ff;
  color: #1890ff;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.1);
}

.generate-button {
  background-color: #f9f9f9;
  border: 1px solid #e8e8e8;
  color: #333;
}

.generate-button:hover {
  background-color: #f0f9ff;
  transform: translateY(-2px);
  border-color: #1890ff;
  color: #1890ff;
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.1);
}

.download-button {
  background-color: #1890ff;
  color: white;
}

.download-button:hover {
  background-color: #40a9ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(24, 144, 255, 0.2);
}

.close-button {
  background-color: rgba(0, 0, 0, 0.1);
  color: white;
}

.close-button:hover {
  background-color: rgba(0, 0, 0, 0.2);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.header-download-button {
  background-color: rgba(255, 255, 255, 0.2);
  color: white;
  margin-left: 8px;
  padding: 0 12px;
  height: 36px;
  flex: initial;
}

.header-download-button:hover {
  background-color: rgba(255, 255, 255, 0.3);
}

.header-close-button {
  background-color: rgba(0, 0, 0, 0.15);
  color: white;
  margin-left: 8px;
  padding: 0 12px;
  height: 36px;
  flex: initial;
}

.header-close-button:hover {
  background-color: rgba(0, 0, 0, 0.25);
}

.report-preview-container {
  display: flex;
  flex-direction: column;
  height: 600px;
  border: 1px solid #e6e9ed;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  background-color: white;
}

.empty-preview-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 48px;
  text-align: center;
  background-color: #fafbfc;
}

.empty-preview-icon {
  font-size: 72px;
  color: #d9d9d9;
  margin-bottom: 24px;
  transition: all 0.3s;
}

.empty-preview-text {
  font-size: 20px;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 12px;
}

.empty-preview-subtext {
  font-size: 16px;
  color: #8c8c8c;
  max-width: 280px;
  text-align: center;
  line-height: 1.5;
}

.report-preview-panel {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
  animation: fadeIn 0.3s ease-in-out;
}

.report-preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 24px;
  background-color: #f9fafb;
  border-bottom: 1px solid #e6e9ed;
}

.preview-title {
  font-size: 18px;
  font-weight: 600;
  color: #1f2937;
  margin: 0;
}

.preview-actions {
  display: flex;
}

.report-document {
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  background-color: white;
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.03);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 自定义Radio按钮样式 */
.format-radio-group .ant-radio-button-wrapper:before {
  display: none !important;
  width: 0 !important;
  background-color: transparent !important;
}

.custom-radio-group {
  display: flex;
  gap: 16px;
  width: 100%;
}

.custom-radio-button {
  flex: 1;
  text-align: center;
  height: 46px;
  line-height: 46px;
  border-radius: 8px;
  transition: all 0.3s;
  background-color: #f9f9f9;
  border: 1px solid #e8e8e8;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
}

.custom-radio-button.active {
  background-color: #e6f7ff;
  border-color: #1890ff;
  color: #1890ff;
}

.custom-radio-button.active .format-icon,
.custom-radio-button.active .format-text {
  color: #1890ff;
}

.custom-radio-button:hover {
  background-color: #f0f9ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

/* 自定义Button样式 */
.custom-button {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 20px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 15px;
  font-weight: 500;
  border: 1px solid #e8e8e8;
  background-color: #f9f9f9;
  color: #333;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  flex: 1;
  outline: none;
  margin-left: 8px;
}

.custom-button .anticon {
  margin-right: 8px;
  font-size: 16px;
  color: #1890ff;
}

.header-download-button {
  background-color: #f9f9f9;
  color: #333;
  margin-left: 8px;
  padding: 0 12px;
  height: 36px;
  flex: initial;
  border: 1px solid #e8e8e8;
}

.header-download-button:hover {
  background-color: #f0f9ff;
  color: #1890ff;
  border-color: #1890ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.header-close-button {
  background-color: #f9f9f9;
  color: #333;
  margin-left: 8px;
  padding: 0 12px;
  height: 36px;
  flex: initial;
  border: 1px solid #e8e8e8;
}

.header-close-button:hover {
  background-color: #f0f9ff;
  color: #1890ff;
  border-color: #1890ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}
</style>
  
  