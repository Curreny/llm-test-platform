# ModelSafety SDK

ModelSafety SDK是一个Python工具包，用于评估和审核大型语言模型的安全性、性能和合规性。SDK提供简单易用的API接口，帮助开发者和研究人员进行大模型安全测试。

## 功能特点

- **题库生成**：自动生成多种类型的测试问题，包括单选题、判断题和问答题
- **题目变形**：对现有题目进行多种变形，增强测试的全面性和鲁棒性
- **模型测试**：发送问题到大模型并获取回答
- **响应审核**：对模型回答进行安全性、准确性和合规性评估
- **报告生成**：生成详细的评测报告

## 安装方法

### 方法一：通过pip安装

```bash
pip install modelsafety
```

### 方法二：从源码安装

```bash
git clone https://github.com/Curreny/modelsafety-sdk.git
cd modelsafety-sdk
pip install -e .
```

## 快速开始

### 初始化客户端

```python
from modelsafety import ModelSafetyClient

# 初始化客户端
client = ModelSafetyClient(base_url="http://localhost:5000")
```

### 题库生成

```python
# 生成题库
question_data = {
    "typesRequest": [
        {"type": "single", "count": 5},
        {"type": "judge", "count": 5},
        {"type": "essay", "count": 5}
    ]
}
result = client.generate_questions_directly(question_data)
questions = result.get("data", [])
```

### 题目变形

```python
# 变形题目
transform_data = {
    "questions": questions,
    "method": "语序变换"  # 可选: 语序变换, 同义词替换, 选项扰动, 上下文调整, 情感立场转换, 噪声注入
}
transform_result = client.transform_questions_directly(transform_data)
transformed_questions = transform_result.get("data", [])
```

### 模型测试与审核

```python
# 测试和审核模型
audit_data = {
    "questions": questions[:3],  # 选择前3个问题进行测试
    "models": ["gpt-4", "glm-4"],
    "auditMode": "rule-based"  # 可选: rule-based, ml-based, hybrid
}
audit_result = client.audit_model_directly(audit_data)

# 打印审核结果
if audit_result and audit_result.get("success", False):
    summary = audit_result.get("summary", {})
    print("\n审核摘要:")
    for model, metrics in summary.items():
        print(f"模型: {model}")
        for metric, value in metrics.items():
            if isinstance(value, (int, float)):
                print(f"  {metric}: {value:.2f}")
```

## 更多示例

更多使用示例请参考`demo.py`文件。

## API文档

详细的API文档请访问我们的[官方文档网站](https://modelsafety.example.com/docs)。

## 许可证

本项目采用MIT许可证。详情请参阅LICENSE文件。