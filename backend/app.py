from flask import Flask, redirect, send_from_directory, jsonify, request, send_file
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import logging
from io import BytesIO

# 导入题库管理模块
from question_generate import QuestionGenerateManager, ExportManager

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../dist/static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

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