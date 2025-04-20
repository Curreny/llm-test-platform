from flask import Flask, redirect, send_from_directory, jsonify, request, send_file
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import logging
import time
import requests
# 导入题库管理模块
from question_generate import QuestionGenerateManager, ExportManager
# 导入题目扩展模块
from question_expansion import transform_question_bank, export_expanded_question_bank
# 导入审核模块
from question_audit import SUPPORTED_MODELS, batch_process_questions
# 导入报告生成模块
from report_generator import ReportGenerator

# 创建 logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # 设置最低等级，记录所有信息

# 日志格式
formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s')

# 文件 Handler（日志写入 app.log）
file_handler = logging.FileHandler('app.log', mode='a', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)  # 也设成最低等级
file_handler.setFormatter(formatter)

# 控制台 Handler（可选，输出到终端）
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# 添加 Handler
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# # 示例输出
# logger.debug("调试信息")
# logger.info("一般信息")
# logger.warning("警告信息")
# logger.error("错误信息")
# logger.critical("严重错误")

app = Flask(__name__, static_folder='../dist/static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# 全局变量保存变形题库
transformed_question_bank = []

# 启动时间戳，用于前端检测后端是否重启
STARTUP_TIMESTAMP = str(int(time.time()))

# ==================== SDK相关API ====================

@app.route('/api/sdk/download', methods=['GET'])
def download_sdk():
    """从 PyPI 获取 modelsafety 最新版本的源码包下载链接，并重定向触发下载"""
    try:
        response = requests.get("https://pypi.org/pypi/modelsafety/json")
        response.raise_for_status()
        data = response.json()
        version = data["info"]["version"]
        for file in data["urls"]:
            if file["packagetype"] == "sdist":
                tarball_url = file["url"]
                print(f"最新版本：{version}，准备跳转下载链接")
                return redirect(tarball_url)
        return "未找到源码分发的安装包。", 404
    except Exception as e:
        return "获取 SDK 包信息失败，请稍后重试。", 500


# ==================== 审核模块 API 路由 ====================

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

# 报告生成API路由
@app.route('/api/audit/generate-report', methods=['POST'])
def generate_report():
    """生成审计报告"""
    try:
        data = request.json
        results = data.get('results', [])
        summary = data.get('summary', {})
        report_format = data.get('format', 'pdf')  # 默认PDF格式
        sections = data.get('sections', ['summary', 'performance', 'charts', 'recommendations'])
        
        logger.info(f"接收到报告生成请求: 格式={report_format}, 部分={sections}, 结果数量={len(results)}")
        
        if not results:
            return jsonify({
                'success': False,
                'message': '没有审计结果，无法生成报告'
            }), 400
        
        # 检查格式
        if report_format not in ['pdf', 'html']:
            return jsonify({
                'success': False,
                'message': f'不支持的报告格式: {report_format}'
            }), 400
        
        # 生成报告
        output, filename = ReportGenerator.generate_report(
            results, 
            summary, 
            report_format, 
            sections
        )
        
        # 从内存直接发送文件
        mimetype = {
            'pdf': 'application/pdf',
            'html': 'text/html'
        }.get(report_format, 'application/octet-stream')
        
        return send_file(
            output,
            as_attachment=True,
            download_name=filename,
            mimetype=mimetype
        )
    
    except Exception as e:
        logger.error(f"生成报告时出错: {str(e)}", exc_info=True)
        return jsonify({
            'success': False,
            'message': f'生成报告时出错: {str(e)}'
        }), 500

@app.route('/api/audit/preview-report', methods=['POST'])
def preview_report():
    """预览报告API"""
    try:
        data = request.json
        
        if not data or 'results' not in data:
            return jsonify({
                'success': False,
                'message': '缺少必要的结果数据'
            }), 400
        
        results = data.get('results', [])
        summary = data.get('summary', {})
        sections = data.get('sections', ['summary', 'performance', 'charts', 'recommendations'])
        
        if not results:
            return jsonify({
                'success': False,
                'message': '审计结果为空，无法生成报告'
            }), 400
            
        # 使用ReportGenerator生成预览HTML
        preview_data = ReportGenerator.generate_preview(results, summary, sections)
        
        return jsonify({
            'success': True,
            'preview': preview_data['html'],
            'data': preview_data['data']
        })
        
    except Exception as e:
        print(f"生成报告预览时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': f'生成预览失败: {str(e)}'
        }), 500

# 前端路由
@app.route('/', defaults={'path': ''})
@app.route('/cover')
@app.route('/question-generate')
@app.route('/question-expansion')
@app.route('/data-audit')
@app.route('/api-integration')
@app.route('/sign-in')
@app.route('/sign-up')


def frontend_routes(path=None, subpath=None):
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