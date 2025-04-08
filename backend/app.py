from flask import Flask, redirect, send_from_directory, jsonify, request, send_file
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import logging
from io import BytesIO

# 导入题库管理模块
from question_generate import QuestionGenerateManager, ExportManager
# 导入题目扩展模块
from question_expansion import transform_question_bank, export_expanded_question_bank

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../dist/static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# 全局变量保存变形题库
transformed_question_bank = []

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
        evaluate_similarity = data.get('evaluate_similarity', True)
        similarity_threshold = data.get('similarity_threshold', 0.8)
        
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
            method=method, 
            evaluate_similarity=evaluate_similarity,
            similarity_threshold=similarity_threshold
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

@app.route('/api/questions/get-transformed', methods=['GET'])
def get_transformed_questions():
    """获取已保存的变形题库"""
    global transformed_question_bank
    try:
        return jsonify({
            'success': True,
            'message': f'获取到{len(transformed_question_bank)}道变形题目',
            'data': transformed_question_bank
        })
    
    except Exception as e:
        logger.error(f"获取变形题库时出错: {str(e)}")
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

@app.route('/api/questions/save-transformed', methods=['POST'])
def save_transformed_questions():
    """保存变形后的题库"""
    global transformed_question_bank
    try:
        data = request.get_json()
        questions = data.get('questions', [])
        
        if not questions:
            return jsonify({
                'success': False,
                'message': '没有可保存的题目'
            }), 400
        
        transformed_question_bank = questions
        
        return jsonify({
            'success': True,
            'message': f'成功保存{len(questions)}道变形题目',
            'data': {
                'count': len(questions)
            }
        })
    
    except Exception as e:
        logger.error(f"保存变形题库时出错: {str(e)}")
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

# 前端路由
@app.route('/', defaults={'path': ''})
@app.route('/cover')
@app.route('/question-generate')
@app.route('/question-expansion')

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