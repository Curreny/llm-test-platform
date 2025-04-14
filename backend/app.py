from flask import Flask, redirect, send_from_directory, jsonify, request, send_file
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import logging
from io import BytesIO
import json
import time
import zipfile  # 添加zipfile用于创建SDK包

# 导入题库管理模块
from question_generate import QuestionGenerateManager, ExportManager
# 导入题目扩展模块
from question_expansion import transform_question_bank, export_expanded_question_bank
# 导入审核模块
from question_audit import SUPPORTED_MODELS, batch_process_questions
# 导入报告生成模块
from report_generator import ReportGenerator

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../dist/static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# 全局变量保存变形题库
transformed_question_bank = []

# 启动时间戳，用于前端检测后端是否重启
STARTUP_TIMESTAMP = str(int(time.time()))

# SDK包版本
SDK_VERSION = "0.1.0"

# SDK API密钥管理
SDK_API_KEYS = {
    "demo_key": {
        "owner": "Demo User", 
        "created_at": "2025-04-01", 
        "permissions": ["generate", "transform", "audit"]
    }
}

# 审核模块 API 路由
@app.route('/api/audit/test-models', methods=['POST'])
def test_models():
    """测试模型响应"""
    try:
        data = request.json
        questions = data.get('questions', [])
        models = data.get('models', [])
        audit_mode = data.get('auditMode', 'rule-based')
        
        logger.info(f"接收到测试请求: 题目数量={len(questions)}, 模型={models}, 审核模式={audit_mode}")
        
        if not questions:
            return jsonify({
                "success": False,
                "message": "没有提供题目数据"
            }), 400
        
        if not models:
            return jsonify({
                "success": False,
                "message": "没有选择测试模型"
            }), 400
        
        # 验证模型是否支持
        unsupported_models = [model for model in models if model not in SUPPORTED_MODELS]
        if unsupported_models:
            return jsonify({
                "success": False,
                "message": f"以下模型不受支持: {', '.join(unsupported_models)}",
                "supportedModels": SUPPORTED_MODELS
            }), 400
        
        # 确保每个问题都有必要的字段
        for i, question in enumerate(questions):
            # 确保有问题内容
            if not question.get('问题'):
                logger.warning(f"问题 {i+1} 缺少内容字段")
                question['问题'] = f"测试问题 {i+1}"
            
            # 确保有类型
            if not question.get('题型'):
                logger.warning(f"问题 {i+1} 缺少类型字段，默认为essay")
                question['题型'] = '简答题'
                
            # 确保有ID
            if not question.get('ID'):
                question['ID'] = f"q{i+1}"
        
        # 处理问题
        logger.info(f"开始处理题目...")
        results, summary = batch_process_questions(questions, models, audit_mode)
        logger.info(f"处理完成: 总数={summary['totalCount']}, 通过率={summary['passRate']}%")
        
        return jsonify({
            "success": True,
            "results": results,
            "summary": summary
        })
    
    except Exception as e:
        logger.error(f"测试模型时出错: {str(e)}", exc_info=True)
        return jsonify({
            "success": False,
            "message": f"测试模型时出错: {str(e)}"
        }), 500

@app.route('/api/audit/list-models', methods=['GET'])
def list_models():
    """获取支持的模型列表"""
    try:
        models = [{"name": model, "available": True} for model in SUPPORTED_MODELS]
        
        return jsonify({
            "success": True,
            "models": models
        })
    
    except Exception as e:
        logger.error(f"获取模型列表时出错: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取模型列表时出错: {str(e)}"
        }), 500

@app.route('/api/audit/save-review', methods=['POST'])
def save_review():
    """保存人工审核结果"""
    try:
        data = request.json
        review_item = data.get('reviewItem', {})
        
        if not review_item or not review_item.get('id'):
            return jsonify({
                "success": False,
                "message": "未提供有效的审核项目"
            }), 400
        
        # 实际项目中，这里会保存到数据库
        # 这里简单返回成功
        return jsonify({
            "success": True,
            "message": "审核结果已保存",
            "data": review_item
        })
    
    except Exception as e:
        logger.error(f"保存审核结果时出错: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"保存审核结果时出错: {str(e)}"
        }), 500

@app.route('/api/questions/generate', methods=['POST'])
def generate_questions():
    """生成题库"""
    try:
        data = request.get_json()
        
        types_request = data.get('typesRequest', [])
        selected_domains = data.get('domains', [])
        
        # 使用题库管理类生成题库
        selected_questions = QuestionGenerateManager.generate_question_bank(types_request, selected_domains)
        
        return jsonify({
            'success': True,
            'data': selected_questions
        })
    except Exception as e:
        logger.error(f"生成题库时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/questions/export-xlsx', methods=['POST'])
def export_excel():
    """导出题库为Excel文件"""
    try:
        data = request.get_json()
        questions = data.get('data', [])
        
        if not questions:
            return jsonify({
                'success': False,
                'message': '没有可导出的题目'
            }), 400
        
        # 使用导出管理类导出Excel
        output, filename = ExportManager.export_to_excel(questions)
        
        # 从内存直接发送文件
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        logger.error(f"导出Excel时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/questions/export-json', methods=['POST'])
def export_json():
    """导出题库为JSON文件"""
    try:
        data = request.get_json()
        questions = data.get('data', [])
        
        if not questions:
            return jsonify({
                'success': False,
                'message': '没有可导出的题目'
            }), 400
        
        logger.debug(f"准备导出 {len(questions)} 道题目为JSON")
        
        # 使用导出管理类导出JSON
        output, filename = ExportManager.export_to_json(questions)
        
        # 从内存直接发送文件
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
    
    except Exception as e:
        logger.error(f"导出JSON时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/questions/current-bank', methods=['GET'])
def get_current_bank():
    """获取当前题库"""
    try:
        # 获取当前题库
        current_questions = QuestionGenerateManager.get_current_question_bank()
        
        return jsonify({
            'success': True,
            'data': current_questions
        })
    except Exception as e:
        logger.error(f"获取当前题库时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/questions/clear-bank', methods=['POST'])
def clear_bank():
    """清空当前题库"""
    try:
        # 清空当前题库
        QuestionGenerateManager.clear_question_bank()
        
        return jsonify({
            'success': True,
            'message': '题库已清空'
        })
    except Exception as e:
        logger.error(f"清空题库时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# 新增: 题目扩展API
@app.route('/api/questions/transform', methods=['POST'])
def transform_questions():
    """变形题库"""
    try:
        data = request.get_json()
        questions = data.get('questions', [])
        method = data.get('method', '语序变换')
        
        if not questions:
            return jsonify({
                'success': False,
                'message': '没有可变形的题目'
            }), 400
        
        # 记录请求信息用于调试
        logger.info(f"变形请求: 方法={method}, 题目数量={len(questions)}")
        logger.info(f"原始题目IDs: {[q.get('id') for q in questions]}")
        
        # 使用题目扩展模块变形题目
        result = transform_question_bank(
            questions, 
            method=method
        )
        
        # 增强变形结果，确保包含ID信息
        if result.get('success', False) and result.get('data'):
            for transformed in result['data']:
                # 确保每个变形后的题目都有id和original_id字段
                if 'original_id' not in transformed:
                    item_index = result['data'].index(transformed)
                    if item_index < len(questions):
                        transformed['original_id'] = questions[item_index].get('id', f"q{item_index}")
                        
            # 记录变形结果用于调试
            logger.info(f"变形结果: 成功={result.get('success')}, 题目数量={len(result.get('data', []))}")
            logger.info(f"变形后题目IDs: {[(t.get('id'), t.get('original_id')) for t in result.get('data', [])]}")
        
        return jsonify(result)
    
    except Exception as e:
        logger.error(f"变形题目时出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500



@app.route('/api/questions/transformed-bank', methods=['GET'])
def get_transformed_bank():
    """获取拓展题库（原始题目和变形题目）"""
    global transformed_question_bank
    try:
        # 获取当前题库
        original_questions = QuestionGenerateManager.get_current_question_bank()
        
        # 提供整个拓展题库，包括原始题目和变形题目
        return jsonify({
            'success': True,
            'data': {
                'originalQuestions': original_questions,
                'transformedQuestions': transformed_question_bank
            }
        })
    except Exception as e:
        logger.error(f"获取拓展题库时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/questions/clear-transformed', methods=['POST'])
def clear_transformed_questions():
    """清空变形题库"""
    global transformed_question_bank
    try:
        transformed_question_bank = []
        
        return jsonify({
            'success': True,
            'message': '成功清空变形题库'
        })
    
    except Exception as e:
        logger.error(f"清空变形题库时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500


@app.route('/api/questions/export-transformed-json', methods=['POST'])
def export_transformed_json():
    """导出拓展题库为JSON文件，包含原始题目和变形后有效的题目"""
    try:
        data = request.get_json()
        original_questions = data.get('originalQuestions', [])
        transformed_questions = data.get('transformedQuestions', [])
        
        if not original_questions and not transformed_questions:
            return jsonify({
                'success': False,
                'message': '没有可导出的题目'
            }), 400
        
        logger.debug(f"准备导出拓展题库为JSON（原始题目: {len(original_questions)}, 变形题目: {len(transformed_questions)}）")
        
        # 使用question_expansion模块导出JSON
        output, filename = export_expanded_question_bank(original_questions, transformed_questions, format='json')
        
        # 从内存直接发送文件
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/json'
        )
    
    except Exception as e:
        logger.error(f"导出拓展题库JSON时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@app.route('/api/questions/export-transformed-xlsx', methods=['POST'])
def export_transformed_excel():
    """导出拓展题库为Excel文件，包含原始题目和变形后有效的题目"""
    try:
        data = request.get_json()
        original_questions = data.get('originalQuestions', [])
        transformed_questions = data.get('transformedQuestions', [])
        
        if not original_questions and not transformed_questions:
            return jsonify({
                'success': False,
                'message': '没有可导出的题目'
            }), 400
        
        logger.debug(f"准备导出拓展题库为Excel（原始题目: {len(original_questions)}, 变形题目: {len(transformed_questions)}）")
        
        # 使用question_expansion模块导出Excel
        output, filename = export_expanded_question_bank(original_questions, transformed_questions, format='xlsx')
        
        # 从内存直接发送文件
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        logger.error(f"导出拓展题库Excel时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

# SDK相关API路由
@app.route('/api/sdk/download', methods=['GET'])
def download_sdk():
    """下载SDK包"""
    try:
        # 创建内存中的ZIP文件
        memory_file = BytesIO()
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 添加SDK包的文件
            
            # 添加setup.py
            setup_py = f"""
from setuptools import setup, find_packages

setup(
    name="safety_bench_sdk",
    version="{SDK_VERSION}",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "pandas>=1.0.0",
        "python-dotenv>=0.15.0",
    ],
    author="Safety Bench Team",
    author_email="support@safetybench.com",
    description="Python SDK for Safety Bench Platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://safetybench.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
"""
            zf.writestr('setup.py', setup_py)
            
            # 添加README.md
            readme_md = """# Safety Bench SDK

Python SDK for Safety Bench Platform

## 安装

```bash
pip install safety_bench_sdk
```

## 使用方法

```python
from safety_bench_sdk import SafetyBenchClient

# 初始化客户端
client = SafetyBenchClient(api_key="your_api_key")

# 生成问题
questions = client.generate_questions(types=["single", "judge"], count={"single": 10, "judge": 5})

# 变形问题
transformed = client.transform_questions(questions, method="语序变换")

# 审核模型响应
audit_results = client.audit_responses(questions, responses, models=["gpt-3.5-turbo", "claude-2"])

# 获取报告
report = client.generate_report(audit_results, format="pdf")
```
"""
            zf.writestr('README.md', readme_md)
            
            # 创建SDK包结构
            
            # __init__.py
            init_py = """from .client import SafetyBenchClient

__version__ = "{}"
""".format(SDK_VERSION)
            zf.writestr('safety_bench_sdk/__init__.py', init_py)
            
            # client.py
            client_py = """import requests
import os
import json
from typing import List, Dict, Any, Optional, Union
import logging

class SafetyBenchClient:
    \"\"\"Safety Bench API 客户端\"\"\"
    
    def __init__(self, api_key: str = None, base_url: str = "https://api.safetybench.com"):
        self.api_key = api_key or os.environ.get("SAFETY_BENCH_API_KEY")
        if not self.api_key:
            raise ValueError("API key is required. Set it during initialization or with SAFETY_BENCH_API_KEY environment variable.")
        
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })
    
    def generate_questions(self, types: List[str], count: Dict[str, int]) -> List[Dict]:
        \"\"\"生成题库
        
        Args:
            types: 题目类型列表，如 ["single", "judge", "essay"]
            count: 各类型题目数量，如 {"single": 10, "judge": 5}
            
        Returns:
            生成的题目列表
        \"\"\"
        response = self.session.post(
            f"{self.base_url}/api/questions/generate",
            json={"typesRequest": types, "domains": [], "count": count}
        )
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            raise Exception(f"API返回错误: {data.get('message', '未知错误')}")
        
        return data.get("data", [])
    
    def transform_questions(self, questions: List[Dict], method: str = "语序变换") -> Dict:
        \"\"\"变形题库
        
        Args:
            questions: 题目列表
            method: 变形方法，可选值: 语序变换, 同义词替换, 选项扰动, 上下文调整
            
        Returns:
            变形结果
        \"\"\"
        response = self.session.post(
            f"{self.base_url}/api/questions/transform",
            json={"questions": questions, "method": method}
        )
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            raise Exception(f"API返回错误: {data.get('message', '未知错误')}")
        
        return data.get("data", {})
    
    def audit_responses(self, questions: List[Dict], responses: List[Dict], 
                       models: List[str], audit_mode: str = "rule-based") -> Dict:
        \"\"\"审核模型响应
        
        Args:
            questions: 题目列表
            responses: 模型回答列表
            models: 要测试的模型列表
            audit_mode: 审核模式，可选值: rule-based, content-based, combination
            
        Returns:
            审核结果
        \"\"\"
        response = self.session.post(
            f"{self.base_url}/api/audit/test-models",
            json={
                "questions": questions,
                "models": models,
                "auditMode": audit_mode
            }
        )
        response.raise_for_status()
        data = response.json()
        
        if not data.get("success"):
            raise Exception(f"API返回错误: {data.get('message', '未知错误')}")
        
        return {
            "results": data.get("results", []),
            "summary": data.get("summary", {})
        }
    
    def generate_report(self, audit_results: Dict, format: str = "pdf", 
                       sections: List[str] = ["summary", "performance", "charts", "recommendations"]) -> bytes:
        \"\"\"生成审计报告
        
        Args:
            audit_results: 审核结果
            format: 报告格式, 可选值: pdf, html
            sections: 报告包含的部分
            
        Returns:
            报告内容的二进制数据
        \"\"\"
        response = self.session.post(
            f"{self.base_url}/api/audit/generate-report",
            json={
                "results": audit_results.get("results", []),
                "summary": audit_results.get("summary", {}),
                "format": format,
                "sections": sections
            }
        )
        response.raise_for_status()
        return response.content
"""
            zf.writestr('safety_bench_sdk/client.py', client_py)
            
            # models.py
            models_py = """from typing import List, Dict, Any, Optional, Union
from dataclasses import dataclass


@dataclass
class Question:
    \"\"\"问题数据结构\"\"\"
    id: str
    prompt: str
    type: str
    options: Optional[List[str]] = None
    answer: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Question':
        return cls(
            id=data.get('id', ''),
            prompt=data.get('问题', ''),
            type=data.get('题型', ''),
            options=data.get('选项', []),
            answer=data.get('答案', '')
        )
    
    def to_dict(self) -> Dict:
        result = {
            'id': self.id,
            '问题': self.prompt,
            '题型': self.type,
        }
        if self.options:
            result['选项'] = self.options
        if self.answer:
            result['答案'] = self.answer
        return result


@dataclass
class AuditResult:
    \"\"\"审核结果数据结构\"\"\"
    question_id: str
    model: str
    response: str
    is_pass: bool
    score: float
    reason: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'AuditResult':
        return cls(
            question_id=data.get('question_id', ''),
            model=data.get('model', ''),
            response=data.get('response', ''),
            is_pass=data.get('is_pass', False),
            score=data.get('score', 0.0),
            reason=data.get('reason')
        )
"""
            zf.writestr('safety_bench_sdk/models.py', models_py)
            
            # utils.py
            utils_py = """import os
import json
import pandas as pd
from typing import List, Dict, Any, Optional, Union
import logging

def load_questions_from_json(file_path: str) -> List[Dict]:
    \"\"\"从JSON文件加载问题\"\"\"
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_questions_to_json(questions: List[Dict], file_path: str) -> None:
    \"\"\"将问题保存到JSON文件\"\"\"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(questions, f, ensure_ascii=False, indent=2)

def load_questions_from_excel(file_path: str) -> List[Dict]:
    \"\"\"从Excel文件加载问题\"\"\"
    df = pd.read_excel(file_path)
    questions = []
    for _, row in df.iterrows():
        question = {k: v for k, v in row.items() if not pd.isna(v)}
        questions.append(question)
    return questions

def save_report_to_file(report_content: bytes, file_path: str) -> None:
    \"\"\"将报告保存到文件\"\"\"
    with open(file_path, 'wb') as f:
        f.write(report_content)
"""
            zf.writestr('safety_bench_sdk/utils.py', utils_py)
        
        # 设置文件指针到开始位置
        memory_file.seek(0)
        
        # 发送ZIP文件
        return send_file(
            memory_file,
            as_attachment=True,
            download_name=f"safety_bench_sdk-{SDK_VERSION}.zip",
            mimetype='application/zip'
        )
    
    except Exception as e:
        logger.error(f"下载SDK时出错: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"下载SDK时出错: {str(e)}"
        }), 500

@app.route('/api/sdk/docs', methods=['GET'])
def get_sdk_docs():
    """获取SDK文档"""
    try:
        docs = {
            "version": SDK_VERSION,
            "description": "Safety Bench Python SDK",
            "installation": "pip install safety_bench_sdk",
            "endpoints": [
                {
                    "name": "generate_questions",
                    "description": "生成题库",
                    "parameters": {
                        "types": "题目类型列表，如 [\"single\", \"judge\", \"essay\"]",
                        "count": "各类型题目数量，如 {\"single\": 10, \"judge\": 5}"
                    },
                    "example": "client.generate_questions(types=[\"single\", \"judge\"], count={\"single\": 10, \"judge\": 5})"
                },
                {
                    "name": "transform_questions",
                    "description": "变形题库",
                    "parameters": {
                        "questions": "题目列表",
                        "method": "变形方法，可选值: 语序变换, 同义词替换, 选项扰动, 上下文调整"
                    },
                    "example": "client.transform_questions(questions, method=\"语序变换\")"
                },
                {
                    "name": "audit_responses",
                    "description": "审核模型响应",
                    "parameters": {
                        "questions": "题目列表",
                        "responses": "模型回答列表",
                        "models": "要测试的模型列表",
                        "audit_mode": "审核模式，可选值: rule-based, content-based, combination"
                    },
                    "example": "client.audit_responses(questions, responses, models=[\"gpt-3.5-turbo\", \"claude-2\"])"
                },
                {
                    "name": "generate_report",
                    "description": "生成审计报告",
                    "parameters": {
                        "audit_results": "审核结果",
                        "format": "报告格式, 可选值: pdf, html",
                        "sections": "报告包含的部分，可选值: summary, performance, charts, recommendations"
                    },
                    "example": "client.generate_report(audit_results, format=\"pdf\")"
                }
            ]
        }
        
        return jsonify({
            "success": True,
            "data": docs
        })
    
    except Exception as e:
        logger.error(f"获取SDK文档时出错: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"获取SDK文档时出错: {str(e)}"
        }), 500

@app.route('/api/sdk/api-keys', methods=['GET', 'POST', 'DELETE'])
def manage_api_keys():
    """管理API密钥"""
    try:
        if request.method == 'GET':
            # 获取API密钥列表（实际项目中，应该基于身份验证来筛选可见的密钥）
            # 这里简单返回模拟数据
            keys_info = [
                {"key": f"{k[:4]}...{k[-4:]}", "owner": v["owner"], "created_at": v["created_at"], "permissions": v["permissions"]}
                for k, v in SDK_API_KEYS.items()
            ]
            
            return jsonify({
                "success": True,
                "data": keys_info
            })
            
        elif request.method == 'POST':
            # 生成新的API密钥
            data = request.get_json()
            owner = data.get('owner', 'Unknown User')
            permissions = data.get('permissions', ["generate", "transform", "audit"])
            
            # 生成随机API密钥（实际项目中，应使用更安全的方法）
            import uuid
            new_key = f"sk-{uuid.uuid4().hex}"
            
            # 存储API密钥（实际项目中，应存储在数据库中）
            SDK_API_KEYS[new_key] = {
                "owner": owner,
                "created_at": time.strftime("%Y-%m-%d"),
                "permissions": permissions
            }
            
            return jsonify({
                "success": True,
                "data": {
                    "key": new_key,
                    "owner": owner,
                    "created_at": SDK_API_KEYS[new_key]["created_at"],
                    "permissions": permissions
                }
            })
            
        elif request.method == 'DELETE':
            # 删除API密钥
            data = request.get_json()
            key = data.get('key')
            
            if not key or key not in SDK_API_KEYS:
                return jsonify({
                    "success": False,
                    "message": "无效的API密钥"
                }), 400
            
            # 删除密钥
            del SDK_API_KEYS[key]
            
            return jsonify({
                "success": True,
                "message": "API密钥已删除"
            })
            
    except Exception as e:
        logger.error(f"管理API密钥时出错: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"管理API密钥时出错: {str(e)}"
        }), 500

# 前端路由
@app.route('/', defaults={'path': ''})
@app.route('/cover')
@app.route('/question-generate')
@app.route('/question-expansion')
@app.route('/data-audit')
@app.route('/api-integration')  # 添加SDK页面路由
def frontend_routes(path=None):
    return send_from_directory('../dist', 'index.html')

# 处理静态资源
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('../dist', filename)

# 默认错误处理
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"code": 404, "message": "Not Found", "data": {}}), 404

@app.errorhandler(500)
def server_error(e):
    return jsonify({"code": 500, "message": str(e), "data": {}}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)