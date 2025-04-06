<template>
    <div class="question-expansion-container">
      <!-- 页面标题部分 -->
      <a-row :gutter="24" class="mb-24">
        <a-col :span="24">
          <a-card :bordered="false" class="header-card">
            <div class="card-header mb-15">
              <h2 class="font-bold">观测题库拓展模块</h2>
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
          <a-card :bordered="false" class="control-panel" style="height: 500px;">
            <div class="card-header mb-15">
              <h3 class="font-bold">题库拓展设置</h3>
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
                变形方式选择
              </div>
              <a-row :gutter="16">
                <a-col :span="12">
                  <a-checkbox-group v-model="selectedTransformations">
                    <div class="transform-checkbox">
                      <a-checkbox value="paraphrase">释义变换</a-checkbox>
                    </div>
                    <div class="transform-checkbox">
                      <a-checkbox value="complexity">复杂度提升</a-checkbox>
                    </div>
                    <div class="transform-checkbox">
                      <a-checkbox value="adversarial">对抗样本生成</a-checkbox>
                    </div>
                  </a-checkbox-group>
                </a-col>
                <a-col :span="12">
                  <a-checkbox-group v-model="selectedTransformations">
                    <div class="transform-checkbox">
                      <a-checkbox value="format">格式转换</a-checkbox>
                    </div>
                    <div class="transform-checkbox">
                      <a-checkbox value="context">上下文扩充</a-checkbox>
                    </div>
                  </a-checkbox-group>
                </a-col>
              </a-row>
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
          <a-card :bordered="false" class="transform-methods" style="height:500px;">
            <div class="card-header mb-15">
              <h3 class="font-bold">变形方式说明</h3>
            </div>
  
            <a-row :gutter="16">
              <a-col :span="12" :xs="24">
                <div class="transform-item transform-item-blue">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#1890ff" aria-hidden="true">
                      <path d="M19 20H5V4h7V2H5c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2v7zM14 2l5 5h-5V2zm3 12v-2h-4v-2h4V8l4 4-4 4z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">释义变换</div>
                    <div class="transform-desc">保持语义不变，重新表述问题</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="24">
                <div class="transform-item transform-item-orange">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#fa8c16" aria-hidden="true">
                      <path d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zM7 13h2v4H7zm4-6h2v10h-2zm4 3h2v7h-2z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">复杂度提升</div>
                    <div class="transform-desc">增加问题难度和复杂性</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="24">
                <div class="transform-item transform-item-purple">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#722ed1" aria-hidden="true">
                      <path d="M12 1L3 5v6c0 5.55 3.84 10.74 9 12 5.16-1.26 9-6.45 9-12V5l-9-4zm0 10.99h7c-.53 4.12-3.28 7.79-7 8.94V12H5V6.3l7-3.11v8.8z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">对抗样本生成</div>
                    <div class="transform-desc">创建边界测试和对抗性问题</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="24">
                <div class="transform-item transform-item-green">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#52c41a" aria-hidden="true">
                      <path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">格式转换</div>
                    <div class="transform-desc">转换问题类型和呈现格式</div>
                  </div>
                </div>
              </a-col>
              <a-col :span="12" :xs="24">
                <div class="transform-item transform-item-cyan">
                  <div class="transform-icon">
                    <svg viewBox="0 0 24 24" width="28" height="28" fill="#13c2c2" aria-hidden="true">
                      <path d="M4 11h6v2H4zm0 4h6v2H4zm0-8h6v2H4zm9 0h7v10h-7zm2 2v6h3v-6z"/>
                    </svg>
                  </div>
                  <div class="transform-info">
                    <div class="transform-name">上下文扩充</div>
                    <div class="transform-desc">添加相关背景信息和上下文</div>
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
                </div>
            </a-card>
        </a-col>
  
        <!-- 变形统计卡片 -->
        <a-col :span="24" :lg="24" v-if="transformedQuestions.length > 0 && !isTransforming" class="mb-24">
          <a-row :gutter="24">
            <a-col :span="8">
              <a-card :bordered="false" class="stats-card">
                <a-statistic
                  title="题目总数"
                  :value="stats.totalQuestions"
                  :precision="0"
                  class="stats-value"
                >
                  <template #suffix>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H15M9 5C9 6.10457 9.89543 7 11 7H13C14.1046 7 15 6.10457 15 5M9 5C9 3.89543 9.89543 3 11 3H13C14.1046 3 15 3.89543 15 5" stroke="#1890ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </template>
                </a-statistic>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card :bordered="false" class="stats-card">
                <a-statistic
                  title="变形题目"
                  :value="stats.transformedCount"
                  :precision="0"
                  class="stats-value"
                >
                  <template #suffix>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M17 1L21 5M21 5L17 9M21 5H7C4.79086 5 3 6.79086 3 9V9M7 23L3 19M3 19L7 15M3 19H17C19.2091 19 21 17.2091 21 15V15" stroke="#722ed1" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </template>
                </a-statistic>
              </a-card>
            </a-col>
            <a-col :span="8">
              <a-card :bordered="false" class="stats-card">
                <a-statistic
                  title="有效性评分"
                  :value="effectivenessPercentage"
                  suffix="%"
                  :precision="1"
                  class="stats-value"
                  :value-style="{ color: effectivenessPercentage >= 90 ? '#52c41a' : '#faad14' }"
                >
                  <template #suffix>
                    <span style="margin-right: 4px">%</span>
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path d="M9 12L11 14L15 10M21 12C21 16.9706 16.9706 21 12 21C7.02944 21 3 16.9706 3 12C3 7.02944 7.02944 3 12 3C16.9706 3 21 7.02944 21 12Z" stroke="#52c41a" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </template>
                </a-statistic>
              </a-card>
            </a-col>
          </a-row>
        </a-col>
  
        <!-- 题目变形展示区 -->
        <a-col :span="24" :lg="24">
          <a-card :bordered="false" class="transformation-display">
            <div class="card-header mb-15">
              <h3 class="font-bold">题目变形预览</h3>
            </div>
            
            <!-- 有变形结果时显示 -->
            <div v-if="transformedQuestions.length > 0 && !isTransforming">
              <div v-for="(item, index) in paginatedTransformedQuestions" :key="index" class="transform-result-item">
                <a-divider orientation="left">
                  <a-tag :color="getTransformationColor(item.transformationType)">
                    {{ getTransformationName(item.transformationType) }}
                  </a-tag>
                  <span class="effectiveness-tag">
                    有效性: {{ Math.round(item.effectiveness * 100) }}%
                  </span>
                </a-divider>
                
                <a-row :gutter="24">
                  <a-col :span="12">
                    <div class="question-card original-question">
                      <div class="question-header">
                        <h4>原始题目</h4>
                        <a-tag>{{ getTypeName(item.original.type) }}</a-tag>
                      </div>
                      <div class="question-content">
                        <p>{{ item.original.prompt }}</p>
                        
                        <!-- 选择题选项 -->
                        <div v-if="item.original.type === 'single' && item.original.options" class="question-options">
                          <div v-for="(option, optIndex) in item.original.options" :key="optIndex" class="option-item">
                            <span class="option-letter">{{ String.fromCharCode(65 + optIndex) }}.</span>
                            <span class="option-text">{{ option }}</span>
                          </div>
                        </div>
                        
                        <!-- 判断题选项 -->
                        <div v-if="item.original.type === 'judge' && item.original.options" class="question-options">
                          <div v-for="(option, optIndex) in item.original.options" :key="optIndex" class="option-item">
                            <span class="option-text">{{ option }}</span>
                          </div>
                        </div>
                      </div>
                      <div class="question-answer">
                        <strong>参考答案:</strong> {{ item.original.answer }}
                      </div>
                    </div>
                  </a-col>
                  <a-col :span="12">
                    <div class="question-card transformed-question">
                      <div class="question-header">
                        <h4>变形后题目</h4>
                        <a-tag>{{ getTypeName(item.transformed.type) }}</a-tag>
                      </div>
                      <div class="question-content">
                        <p>{{ item.transformed.prompt }}</p>
                        
                        <!-- 选择题选项 -->
                        <div v-if="item.transformed.type === 'single' && item.transformed.options" class="question-options">
                          <div v-for="(option, optIndex) in item.transformed.options" :key="optIndex" class="option-item">
                            <span class="option-letter">{{ String.fromCharCode(65 + optIndex) }}.</span>
                            <span class="option-text">{{ option }}</span>
                          </div>
                        </div>
                        
                        <!-- 判断题选项 -->
                        <div v-if="item.transformed.type === 'judge' && item.transformed.options" class="question-options">
                          <div v-for="(option, optIndex) in item.transformed.options" :key="optIndex" class="option-item">
                            <span class="option-text">{{ option }}</span>
                          </div>
                        </div>
                      </div>
                      <div class="question-answer">
                        <strong>参考答案:</strong> {{ item.transformed.answer }}
                      </div>
                    </div>
                  </a-col>
                </a-row>
              </div>
              
              <!-- 分页组件 -->
              <div class="pagination-container">
                <a-pagination 
                  v-model="currentPage" 
                  :total="transformedQuestions.length" 
                  :pageSize="pageSize"
                  @change="handlePageChange"
                  show-quick-jumper
                />
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
  
  export default {
    name: 'QuestionExpansion',
    
    data() {
      return {
        // 题目导入相关状态
        importDialogVisible: false,
        isImporting: false,
        
        // 变形相关状态
        isTransforming: false,
        selectedTransformations: ['paraphrase', 'complexity'],
        transformationProgress: 0,
        transformingQuestionIndex: -1,
        
        // 题目数据
        originalQuestions: [],
        transformedQuestions: [],
        
        // 分页相关
        currentPage: 1,
        pageSize: 5,
        
        // 有效性评分
        effectivenessScores: [],
        
        // 变形方式描述
        transformationDescriptions: {
          paraphrase: '保持语义不变，重新表述问题',
          complexity: '增加问题难度和复杂性',
          adversarial: '创建边界测试和对抗性问题',
          format: '转换问题类型和呈现格式',
          context: '添加相关背景信息和上下文'
        }
      };
    },
    
    computed: {
      transformProgressPercentage() {
        if (this.originalQuestions.length === 0) return 0;
        return Math.round((this.transformationProgress / this.originalQuestions.length) * 100);
      },
      
      effectivenessPercentage() {
        if (this.effectivenessScores.length === 0) return 0;
        const average = this.effectivenessScores.reduce((sum, score) => sum + score, 0) / this.effectivenessScores.length;
        return (average * 100).toFixed(1);
      },
      
      paginatedTransformedQuestions() {
        const startIndex = (this.currentPage - 1) * this.pageSize;
        const endIndex = startIndex + this.pageSize;
        return this.transformedQuestions.slice(startIndex, endIndex);
      },
      
      stats() {
        return {
          totalQuestions: this.originalQuestions.length,
          transformedCount: this.transformedQuestions.length
        };
      }
    },
    
    methods: {
      openImportDialog() {
        this.importDialogVisible = true;
      },
      
      async importQuestionsFromGenerate() {
        this.isImporting = true;
        try {
          // 通过API直接从后端获取已生成的题库
          const response = await axios.get('http://localhost:5000/api/questions/current-bank');
          
          if (response.data.success && response.data.data.length > 0) {
            this.originalQuestions = response.data.data;
            this.transformedQuestions = [];
            this.effectivenessScores = [];
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
          // 这里可以使用 notification 或 message 组件进行提示
          console.warn('请至少选择一种变形方式');
          return;
        }
        
        // 开始变形
        this.isTransforming = true;
        this.transformationProgress = 0;
        this.transformedQuestions = [];
        this.effectivenessScores = [];
        
        try {
          // 遍历所有原始题目进行变形
          for (let i = 0; i < this.originalQuestions.length; i++) {
            this.transformingQuestionIndex = i;
            const originalQuestion = this.originalQuestions[i];
            
            // 从选中的变形方式中随机选择一种
            const transformation = this.selectedTransformations[
              Math.floor(Math.random() * this.selectedTransformations.length)
            ];
            
            // 模拟变形过程，实际项目中可能需要调用API
            await this.simulateTransformation(originalQuestion, transformation);
            
            // 更新进度
            this.transformationProgress++;
          }
        } catch (error) {
          console.error('变形题目失败:', error);
        } finally {
          this.isTransforming = false;
          this.transformingQuestionIndex = -1;
        }
      },
      
      async simulateTransformation(originalQuestion, transformationType) {
        // 模拟API调用延迟
        await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));
        
        let transformedQuestion = { ...originalQuestion };
        let effectiveness = 0.9 + Math.random() * 0.1; // 模拟90%以上的有效性
        
        // 根据不同的变形方式，对题目进行不同的变形
        switch (transformationType) {
          case 'paraphrase':
            // 释义变换
            if (originalQuestion.type === 'single') {
              transformedQuestion.prompt = `从下列选项中，选出最能代表${originalQuestion.prompt.replace('以下哪个是', '').replace('？', '')}的一项：`;
            } else if (originalQuestion.type === 'judge') {
              transformedQuestion.prompt = `判断以下说法是否正确：${originalQuestion.prompt.replace('。', '')}`;
            } else {
              transformedQuestion.prompt = `请详细阐述：${originalQuestion.prompt.replace('请解释', '').replace('。', '')}`;
            }
            break;
            
          case 'complexity':
            // 复杂度提升
            if (originalQuestion.type === 'single') {
              transformedQuestion.prompt = `在考虑实际应用场景和各种边界条件的情况下，${originalQuestion.prompt.toLowerCase()}请分析各选项并选择最准确的答案。`;
            } else if (originalQuestion.type === 'judge') {
              transformedQuestion.prompt = `深入思考后判断：在绝大多数标准实现和常见应用场景中，${originalQuestion.prompt}这一说法是否成立？`;
            } else {
              transformedQuestion.prompt = `结合实际项目经验和最新行业标准，全面分析并详细论述：${originalQuestion.prompt}`;
            }
            break;
            
          case 'adversarial':
            // 对抗样本生成
            if (originalQuestion.type === 'single') {
              transformedQuestion.prompt = `以下关于${originalQuestion.prompt.replace('以下哪个是', '').replace('？', '')}的说法中，哪一项包含了微妙的错误？`;
              // 交换答案，制造对抗样本
              if (originalQuestion.options) {
                const correctIndex = 'ABCD'.indexOf(originalQuestion.answer);
                const wrongIndex = (correctIndex + 1) % originalQuestion.options.length;
                transformedQuestion.answer = 'ABCD'[wrongIndex];
              }
            } else if (originalQuestion.type === 'judge') {
              transformedQuestion.prompt = `以下陈述可能包含微妙的错误，请仔细判断：${originalQuestion.prompt}`;
              // 反转答案
              transformedQuestion.answer = originalQuestion.answer === '正确' ? '错误' : '正确';
            } else {
              transformedQuestion.prompt = `以下观点存在一些值得商榷的地方，请指出其中的问题并给出修正：${originalQuestion.prompt.replace('请解释', '')}`;
            }
            break;
            
          case 'format':
            // 格式转换
            if (originalQuestion.type === 'single') {
              // 转换为简答题
              transformedQuestion.type = 'essay';
              transformedQuestion.prompt = `简述${originalQuestion.options[1]}概念以及它在面向对象编程中的重要性。`;
              transformedQuestion.options = null;
              transformedQuestion.answer = `${originalQuestion.options[1]}是面向对象编程的核心概念之一，它指的是将数据和方法捆绑在一起，对外部隐藏实现细节，只暴露必要的接口。它的重要性在于保护数据完整性、提高代码可维护性和重用性。`;
            } else if (originalQuestion.type === 'judge') {
              // 转换为选择题
              transformedQuestion.type = 'single';
              transformedQuestion.prompt = `关于HTTP协议的特性，下列说法正确的是：`;
              transformedQuestion.options = [
                'HTTP是一种有状态的协议，服务器会记住客户端的历史请求',
                'HTTP是一种无状态的协议，每个请求之间相互独立',
                'HTTP默认使用UDP协议作为传输层协议',
                'HTTP只支持GET请求方法'
              ];
              transformedQuestion.answer = 'B';
            } else {
              // 转换为多个判断题
              transformedQuestion.type = 'judge';
              transformedQuestion.prompt = 'REST API的主要特点之一是无状态性。';
              transformedQuestion.options = ['正确', '错误'];
              transformedQuestion.answer = '正确';
            }
            break;
            
          case 'context':
            // 上下文扩充
            if (originalQuestion.type === 'single') {
              transformedQuestion.prompt = `在开发一个电子商务网站的购物车模块时，你需要应用面向对象编程的概念。${originalQuestion.prompt}请选择最适合实现数据隐藏和接口公开的概念。`;
            } else if (originalQuestion.type === 'judge') {
              transformedQuestion.prompt = `在设计高并发Web应用时，了解协议特性至关重要。${originalQuestion.prompt}这对于负载均衡和水平扩展有何影响？`;
            } else {
              transformedQuestion.prompt = `作为一个新项目的技术负责人，你需要在微服务架构中设计API。${originalQuestion.prompt}并讨论在大规模分布式系统中如何保证这些特性。`;
            }
            break;
        }
        
        // 将变形后的题目添加到结果中
        this.transformedQuestions.push({
          original: originalQuestion,
          transformed: transformedQuestion,
          transformationType,
          effectiveness
        });
        
        // 记录有效性评分
        this.effectivenessScores.push(effectiveness);
        
        return transformedQuestion;
      },
      
      handlePageChange(page) {
        this.currentPage = page;
      },
      
      getTransformationColor(type) {
        const colorMap = {
          paraphrase: '#1890ff',
          complexity: '#fa8c16',
          adversarial: '#722ed1',
          format: '#52c41a',
          context: '#13c2c2'
        };
        return colorMap[type] || '#1890ff';
      },
      
      getTransformationName(type) {
        const nameMap = {
          paraphrase: '释义变换',
          complexity: '复杂度提升',
          adversarial: '对抗样本生成',
          format: '格式转换',
          context: '上下文扩充'
        };
        return nameMap[type] || type;
      },
      
      getTypeName(type) {
        const typeMap = {
          single: '单选题',
          judge: '判断题',
          essay: '简答题'
        };
        return typeMap[type] || type;
      }
    }
  };
</script>
  
<style lang="scss" scoped>
  .question-expansion-container {
    padding: 24px;
  
    .mb-15 {
      margin-bottom: 15px;
    }
  
    .mb-24 {
      margin-bottom: 24px;
    }
  
    .font-bold {
      font-weight: 600;
    }
  
    .problem-text {
      font-size: 14px;
      color: rgba(0, 0, 0, 0.65);
      margin-bottom: 0;
    }
  
    // 控制面板样式
    .control-panel, .transform-methods {
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      transition: all 0.3s;
  
      &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  
      .form-item {
        margin-bottom: 16px;
  
        .form-label {
          font-size: 14px;
          color: rgba(0, 0, 0, 0.65);
          margin-bottom: 8px;
          display: flex;
          align-items: center;
  
          .icon-wrapper {
            margin-right: 8px;
            display: inline-flex;
            align-items: center;
          }
        }
      }
  
      .transform-checkbox {
        margin-bottom: 10px;
      }
  
      .import-btn {
        border: 1px dashed #d9d9d9;
        font-size: 14px;
        height: 52px;
        transition: all 0.3s;
  
        &:hover {
          border-color: #40a9ff;
          color: #40a9ff;
        }
  
        .btn-content {
          display: flex;
          align-items: center;
          justify-content: center;
          
          svg {
            margin-right: 8px;
          }
        }
      }
  
      .generate-btn {
        margin-top: 24px;
        height: 48px;

        display: flex;
        align-items: center;
        justify-content: center;
  
        .btn-content {
          display: flex;
          align-items: center;
          justify-content: center;

          svg {
            margin-right: 8px;
          }
        }
      }
    }
  
    // 变形方式卡片样式
    .transform-methods {
      .transform-item {
        display: flex;
        align-items: center;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 12px;
        transition: all 0.3s;
  
        &:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
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
  
        .transform-info {
          flex: 1;
  
          .transform-name {
            font-weight: 600;
            font-size: 14px;
            margin-bottom: 4px;
          }
  
          .transform-desc {
            font-size: 12px;
            color: rgba(0, 0, 0, 0.65);
          }
        }
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
    }
  
    // 进度卡片样式
    .progress-card {
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      
      .progress-header {
        margin-bottom: 16px;
      }
      
      .progress-info {
        margin-top: 16px;
        
        .current-question {
          font-size: 14px;
          
          .question-label {
            color: rgba(0, 0, 0, 0.65);
          }
          
          .question-content {
            color: rgba(0, 0, 0, 0.85);
            font-weight: 500;
          }
        }
      }
    }
  
    // 统计卡片样式
    .stats-card {
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      
      .stats-value {
        display: flex;
        align-items: center;
        
        :deep(.ant-statistic-content-suffix) {
          display: flex;
          align-items: center;
          margin-left: 8px;
        }
      }
    }
  
    // 变形结果展示区样式
    .transformation-display {
      border-radius: 12px;
      box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
      
      .transform-result-item {
        margin-bottom: 32px;
        
        .effectiveness-tag {
          margin-left: 16px;
          color: rgba(0, 0, 0, 0.65);
          font-size: 14px;
        }
        
        .question-card {
          padding: 16px;
          border-radius: 8px;
          margin-bottom: 16px;
          
          .question-header {
            display: flex;
            align-items: center;
            margin-bottom: 12px;
            
            h4 {
              margin: 0;
              margin-right: 10px;
            }
          }
          
          .question-content {
            margin-bottom: 12px;
            
            p {
              margin-bottom: 12px;
            }
            
            .question-options {
              .option-item {
                margin-bottom: 8px;
                
                .option-letter {
                  display: inline-block;
                  width: 24px;
                  font-weight: 500;
                }
              }
            }
          }
          
          .question-answer {
            font-size: 14px;
            padding-top: 10px;
            border-top: 1px dashed #f0f0f0;
          }
        }
        
        .original-question {
          background-color: rgba(240, 242, 245, 0.4);
          border: 1px solid #f0f0f0;
        }
        
        .transformed-question {
          background-color: rgba(24, 144, 255, 0.04);
          border: 1px solid rgba(24, 144, 255, 0.15);
        }
      }
      
      .pagination-container {
        display: flex;
        justify-content: center;
        margin-top: 32px;
      }
      
      .empty-state {
        padding: 48px 0;
        text-align: center;
        
        .empty-content {
          display: inline-block;
          
          svg {
            margin-bottom: 16px;
          }
          
          .empty-text {
            color: rgba(0, 0, 0, 0.45);
            font-size: 14px;
            line-height: 1.6;
          }
          
          a {
            color: #1890ff;
            text-decoration: none;
            
            &:hover {
              text-decoration: underline;
            }
          }
        }
      }
    }
  }

  .highlight-text {
    color: #1890ff; /* Ant Design默认的主题蓝色 */
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
</style>