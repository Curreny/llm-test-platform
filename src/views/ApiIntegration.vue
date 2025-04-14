<template>
  <div class="api-integration-container">
    <!-- 页面标题部分 -->
    <a-row :gutter="24" class="mb-24">
      <a-col :span="24">
        <a-card :bordered="false" class="header-card">
          <div class="card-header mb-15">
            <h2 class="font-bold">API集成模块</h2>
          </div>
          <p class="problem-text">
            提供完善的API接口，支持题库生成、题目变形、结果审核等功能的外部集成，方便第三方系统对接使用。
          </p>
        </a-card>
      </a-col>
    </a-row>

    <!-- API信息和测试区域 -->
    <a-row :gutter="24" class="mb-24">
      <!-- API列表 -->
      <a-col :span="24" :lg="8" class="mb-24">
        <a-card :bordered="false" class="api-list-card">
          <div class="card-header mb-15">
            <h3 class="font-bold">API接口列表</h3>
          </div>
          <a-menu mode="inline" :default-selected-keys="['1']" @select="handleApiSelect">
            <a-menu-item key="1">
              <div class="api-menu-item">
                <span class="api-method post">POST</span>
                <span class="api-path">/api/questions/generate</span>
              </div>
              <div class="api-description">生成题库接口</div>
            </a-menu-item>
            <a-menu-item key="2">
              <div class="api-menu-item">
                <span class="api-method post">POST</span>
                <span class="api-path">/api/questions/transform</span>
              </div>
              <div class="api-description">题目变形接口</div>
            </a-menu-item>
            <a-menu-item key="3">
              <div class="api-menu-item">
                <span class="api-method post">POST</span>
                <span class="api-path">/api/audit/result</span>
              </div>
              <div class="api-description">结果审核接口</div>
            </a-menu-item>
            <a-menu-item key="4">
              <div class="api-menu-item">
                <span class="api-method get">GET</span>
                <span class="api-path">/api/questions</span>
              </div>
              <div class="api-description">获取题库列表</div>
            </a-menu-item>
            <a-menu-item key="5">
              <div class="api-menu-item">
                <span class="api-method get">GET</span>
                <span class="api-path">/api/report/generate</span>
              </div>
              <div class="api-description">生成观测报告</div>
            </a-menu-item>
          </a-menu>
        </a-card>
      </a-col>

      <!-- API详情和测试工具 -->
      <a-col :span="24" :lg="16">
        <a-card :bordered="false" class="api-detail-card">
          <div class="card-header mb-15">
            <h3 class="font-bold">{{ currentApi.title }}</h3>
            <a-tag :color="currentApi.method === 'POST' ? 'blue' : 'green'">{{ currentApi.method }}</a-tag>
          </div>
          
          <div class="api-section">
            <div class="section-title">基本信息</div>
            <div class="section-content">
              <div class="info-item">
                <span class="info-label">接口URL：</span>
                <span class="info-value">{{ currentApi.url }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">描述：</span>
                <span class="info-value">{{ currentApi.description }}</span>
              </div>
              <div class="info-item">
                <span class="info-label">Content-Type：</span>
                <span class="info-value">application/json</span>
              </div>
            </div>
          </div>

          <div class="api-section">
            <div class="section-title">请求参数</div>
            <div class="section-content">
              <a-table 
                :columns="paramColumns" 
                :data-source="currentApi.params" 
                :pagination="false"
                size="small"
              />
            </div>
          </div>

          <div class="api-section">
            <div class="section-title">API测试</div>
            <div class="section-content">
              <a-textarea 
                v-model="requestBody" 
                :rows="6" 
                placeholder="请输入请求体 JSON" 
                class="mb-15"
              />
              <div class="test-actions mb-15">
                <a-button type="primary" @click="testApi" :loading="isTestingApi">
                  <span>发送请求</span>
                </a-button>
                <a-button @click="resetApiTest" class="ml-10">
                  <span>重置</span>
                </a-button>
              </div>
              <div v-if="apiResponse" class="api-response">
                <div class="response-header">
                  <span>响应结果</span>
                  <span class="status" :class="{ 'success': apiResponseStatus === 200 }">
                    状态码：{{ apiResponseStatus }}
                  </span>
                </div>
                <a-textarea 
                  v-model="apiResponse" 
                  :rows="8" 
                  class="response-body"
                  disabled
                />
              </div>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- API密钥管理 -->
    <a-row :gutter="24" class="mb-24">
      <a-col :span="24">
        <a-card :bordered="false" class="api-key-card">
          <div class="card-header mb-15">
            <h3 class="font-bold">API密钥管理</h3>
          </div>
          <div class="api-key-section">
            <div class="api-key-info">
              <div class="key-label">您的API密钥</div>
              <div class="key-value-container">
                <input 
                  type="text" 
                  :value="showKey ? apiKey : '******************************'" 
                  class="key-value" 
                  readonly
                />
                <a-button 
                  class="key-action" 
                  type="link" 
                  @click="toggleShowKey"
                >
                  <a-icon :type="showKey ? 'eye-invisible' : 'eye'" />
                </a-button>
                <a-button 
                  class="key-action" 
                  type="link" 
                  @click="copyApiKey"
                >
                  <a-icon type="copy" />
                </a-button>
              </div>
            </div>
            <div class="api-key-actions">
              <a-button type="primary" @click="regenerateApiKey">
                <span>重新生成密钥</span>
              </a-button>
            </div>
          </div>
        </a-card>
      </a-col>
    </a-row>

    <!-- API集成示例 -->
    <a-row :gutter="24">
      <a-col :span="24">
        <a-card :bordered="false" class="api-code-examples">
          <div class="card-header mb-15">
            <h3 class="font-bold">集成示例代码</h3>
          </div>
          <a-tabs default-active-key="1">
            <a-tab-pane key="1" tab="Python">
              <pre class="code-block">
              </pre>
            </a-tab-pane>
          </a-tabs>
        </a-card>
      </a-col>
    </a-row>
  </div>
</template>

<script>
export default {
  name: 'ApiIntegration',
  data() {
    return {
      // API列表数据
      apiList: [
        {
          id: '1',
          title: '生成题库接口',
          method: 'POST',
          url: '/api/questions/generate',
          description: '根据指定的题目类型和数量生成测试题库',
          params: [
            { key: 'types', name: 'types', type: 'array', required: true, description: '题目类型数组，可选值：single, judge, essay' },
            { key: 'count', name: 'count', type: 'object', required: true, description: '各类型题目数量，如 {"single": 10, "judge": 5}' },
          ],
          sampleRequest: '{\n  "types": ["single", "judge"],\n  "count": {\n    "single": 10,\n    "judge": 5\n  }\n}'
        },
        {
          id: '2',
          title: '题目变形接口',
          method: 'POST',
          url: '/api/questions/transform',
          description: '对现有题目进行变形处理，支持多种变形方式',
          params: [
            { key: 'questions', name: 'questions', type: 'array', required: true, description: '题目对象数组' },
            { key: 'method', name: 'method', type: 'string', required: true, description: '变形方法，可选值：语序变换, 同义词替换, 选项扰动, 上下文调整' },
          ],
          sampleRequest: '{\n  "questions": [\n    {\n      "id": "q1",\n      "type": "single",\n      "prompt": "什么是人工智能？",\n      "options": ["选项A", "选项B", "选项C", "选项D"],\n      "answer": "A"\n    }\n  ],\n  "method": "语序变换"\n}'
        },
        {
          id: '3',
          title: '结果审核接口',
          method: 'POST',
          url: '/api/audit/result',
          description: '对大模型输出结果进行审核，检查是否符合预期',
          params: [
            { key: 'questions', name: 'questions', type: 'array', required: true, description: '问题数组' },
            { key: 'responses', name: 'responses', type: 'array', required: true, description: '大模型回答数组' },
            { key: 'audit_mode', name: 'audit_mode', type: 'string', required: false, description: '审核模式，默认为auto' },
          ],
          sampleRequest: '{\n  "questions": [\n    {\n      "id": "q1",\n      "prompt": "什么是人工智能？"\n    }\n  ],\n  "responses": [\n    {\n      "question_id": "q1",\n      "response": "人工智能是计算机科学的一个子领域..."\n    }\n  ],\n  "audit_mode": "auto"\n}'
        },
        {
          id: '4',
          title: '获取题库列表',
          method: 'GET',
          url: '/api/questions',
          description: '获取系统中已生成的题库列表',
          params: [
            { key: 'page', name: 'page', type: 'number', required: false, description: '页码，默认为1' },
            { key: 'limit', name: 'limit', type: 'number', required: false, description: '每页数量，默认为20' },
            { key: 'type', name: 'type', type: 'string', required: false, description: '题目类型过滤' },
          ],
          sampleRequest: ''
        },
        {
          id: '5',
          title: '生成观测报告',
          method: 'GET',
          url: '/api/report/generate',
          description: '基于测试结果生成大模型能力观测报告',
          params: [
            { key: 'test_id', name: 'test_id', type: 'string', required: true, description: '测试ID' },
            { key: 'format', name: 'format', type: 'string', required: false, description: '报告格式，可选值：json, pdf, html' },
          ],
          sampleRequest: ''
        },
      ],
      // 当前选中的API
      currentApiId: '1',
      // 表格列定义
      paramColumns: [
        { title: '参数名', dataIndex: 'name', key: 'name' },
        { title: '类型', dataIndex: 'type', key: 'type' },
        { title: '必填', dataIndex: 'required', key: 'required', 
          customRender: (text) => text ? '是' : '否' },
        { title: '描述', dataIndex: 'description', key: 'description' },
      ],
      // API测试数据
      requestBody: '',
      apiResponse: '',
      apiResponseStatus: null,
      isTestingApi: false,
      // API密钥
      apiKey: 'sk-123456789abcdef0123456789abcdef0',
      showKey: false
    }
  },
  computed: {
    // 当前选中的API详情
    currentApi() {
      return this.apiList.find(api => api.id === this.currentApiId) || this.apiList[0];
    }
  },
  mounted() {
    // 初始化请求示例
    this.resetApiTest();
  },
  methods: {
    // 选择API
    handleApiSelect(e) {
      this.currentApiId = e.key;
      this.resetApiTest();
    },
    // 测试API
    testApi() {
      this.isTestingApi = true;
      
      // 模拟API调用
      setTimeout(() => {
        const success = Math.random() > 0.2; // 80%的成功率
        this.apiResponseStatus = success ? 200 : 400;
        
        if (success) {
          if (this.currentApi.method === 'GET') {
            if (this.currentApi.id === '4') {
              // 获取题库列表
              this.apiResponse = JSON.stringify({
                status: "success",
                data: {
                  total: 38,
                  page: 1,
                  limit: 20,
                  questions: Array.from({length: 5}, (_, i) => ({
                    id: `q${i+1}`,
                    type: i % 2 === 0 ? 'single' : 'judge',
                    prompt: `示例题目 ${i+1}`,
                    created_at: new Date().toISOString()
                  }))
                }
              }, null, 2);
            } else {
              // 生成报告
              this.apiResponse = JSON.stringify({
                status: "success",
                data: {
                  report_id: "rep_" + Math.random().toString(36).substring(2, 10),
                  url: "https://example.com/reports/12345",
                  created_at: new Date().toISOString()
                }
              }, null, 2);
            }
          } else {
            if (this.currentApi.id === '1') {
              // 生成题库响应
              this.apiResponse = JSON.stringify({
                status: "success",
                data: {
                  job_id: "job_" + Math.random().toString(36).substring(2, 10),
                  estimated_time: "30s",
                  questions_count: 15
                }
              }, null, 2);
            } else if (this.currentApi.id === '2') {
              // 题目变形响应
              this.apiResponse = JSON.stringify({
                status: "success",
                data: {
                  original_count: 1,
                  transformed_count: 1,
                  questions: [
                    {
                      id: "q1_transformed",
                      original_id: "q1",
                      type: "single",
                      prompt: "在当今科技领域，人工智能被定义为什么？",
                      options: ["选项A", "选项B", "选项C", "选项D"],
                      answer: "A",
                      transformation_method: "语序变换",
                      is_valid: true
                    }
                  ]
                }
              }, null, 2);
            } else {
              // 结果审核响应
              this.apiResponse = JSON.stringify({
                status: "success",
                data: {
                  audit_results: [
                    {
                      question_id: "q1",
                      is_valid: true,
                      score: 0.92,
                      feedback: "回答符合预期，内容准确"
                    }
                  ],
                  summary: {
                    total: 1,
                    valid: 1,
                    invalid: 0,
                    avg_score: 0.92
                  }
                }
              }, null, 2);
            }
          }
        } else {
          // 错误响应
          this.apiResponse = JSON.stringify({
            status: "error",
            error: {
              code: "invalid_request",
              message: "请求参数格式错误或缺少必要参数",
              details: "请检查API文档并修正请求格式"
            }
          }, null, 2);
        }
        
        this.isTestingApi = false;
      }, 1000);
    },
    // 重置API测试
    resetApiTest() {
      this.apiResponse = '';
      this.apiResponseStatus = null;
      this.requestBody = this.currentApi.sampleRequest || '';
    },
    // 显示/隐藏API密钥
    toggleShowKey() {
      this.showKey = !this.showKey;
    },
    // 复制API密钥
    copyApiKey() {
      navigator.clipboard.writeText(this.apiKey).then(() => {
        this.$message.success('API密钥已复制到剪贴板');
      }).catch(err => {
        this.$message.error('复制失败: ' + err);
      });
    },
    // 重新生成API密钥
    regenerateApiKey() {
      this.$confirm({
        title: '重新生成API密钥',
        content: '确定要重新生成API密钥吗？旧密钥将立即失效，所有使用旧密钥的应用将无法访问API。',
        okText: '确定',
        cancelText: '取消',
        onOk: () => {
          // 模拟生成新密钥
          this.apiKey = 'sk-' + Math.random().toString(36).substring(2, 30);
          this.$message.success('API密钥已重新生成');
        }
      });
    }
  }
}
</script>

<style scoped>
.api-integration-container {
  padding: 24px;
}

.header-card {
  margin-bottom: 24px;
  background: linear-gradient(to bottom, rgba(33, 150, 243, 0.8), rgba(255, 255, 255, 0.4));
  color: #fff;
  border-radius: 10px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}

.api-menu-item {
  display: flex;
  align-items: center;
  font-weight: 500;
}

.api-method {
  display: inline-block;
  padding: 2px 6px;
  border-radius: 4px;
  margin-right: 8px;
  font-size: 12px;
  font-weight: 600;
}

.post {
  background-color: #1890ff;
  color: #fff;
}

.get {
  background-color: #52c41a;
  color: #fff;
}

.api-path {
  font-family: monospace;
}

.api-description {
  font-size: 12px;
  color: rgba(0, 0, 0, 0.45);
  margin-top: 4px;
  padding-left: 36px;
}

.api-section {
  margin-bottom: 24px;
}

.section-title {
  font-weight: 600;
  margin-bottom: 12px;
  color: #333;
}

.info-item {
  margin-bottom: 8px;
  display: flex;
}

.info-label {
  font-weight: 500;
  min-width: 100px;
}

.ml-10 {
  margin-left: 10px;
}

.api-response {
  border: 1px solid #eee;
  border-radius: 4px;
}

.response-header {
  padding: 8px 12px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
}

.status {
  font-family: monospace;
  color: #f5222d;
}

.status.success {
  color: #52c41a;
}

.response-body {
  border: none;
  border-radius: 0 0 4px 4px;
}

.api-key-section {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.key-label {
  font-weight: 500;
  margin-bottom: 8px;
}

.key-value-container {
  display: flex;
  align-items: center;
  background-color: #f5f5f5;
  border: 1px solid #d9d9d9;
  border-radius: 4px;
  padding: 4px 12px;
  width: 500px;
}

.key-value {
  border: none;
  background: none;
  flex: 1;
  font-family: monospace;
  outline: none;
}

.code-block {
  background-color: #f5f5f5;
  border-radius: 4px;
  padding: 16px;
  overflow: auto;
  font-family: monospace;
  font-size: 13px;
  line-height: 1.5;
}

.mb-15 {
  margin-bottom: 15px;
}

.mb-24 {
  margin-bottom: 24px;
}
</style>
