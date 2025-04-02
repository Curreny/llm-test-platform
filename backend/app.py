from flask import Flask, redirect, send_from_directory, jsonify, request, send_file
import os
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import json
import random
import logging
import pandas as pd
from io import BytesIO
import tempfile

# 配置日志
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='../dist/static', static_url_path='/static')
app.wsgi_app = ProxyFix(app.wsgi_app)
CORS(app)

# 创建必要的目录
def create_required_dirs():
    # 创建数据输出目录
    output_dir = os.environ.get('OUTPUT_DIR', 'output')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

# 数据文件路径
DATA_DIR = 'data'
QUESTION_FILES = {
    'poisonMpts': '100PoisonMpts_data.json',
    'cValues': 'CValues-Comparison_data.json',
    'instructionAttack': 'instruction_attack_data.json',
    'safetyBench': 'SafetyBench_data.json',
    'typicalSafety': 'typical_safety_data.json'
}

def load_questions(source):
    """加载指定来源的题库数据"""
    try:
        file_path = os.path.join(DATA_DIR, QUESTION_FILES[source])
        logger.debug(f"正在加载数据文件: {file_path}")
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            logger.debug(f"成功加载 {source} 数据，共 {len(data)} 条记录")
            return data
    except FileNotFoundError:
        logger.error(f"找不到数据文件: {file_path}")
        return []
    except Exception as e:
        logger.error(f"加载数据文件时出错: {str(e)}")
        return []

def process_question(question, source):
    """根据数据来源处理题目格式"""
    try:
        processed = {
            'id': question.get('id', ''),
            'type': question.get('type', 'essay'),  # 默认为问答题
            'category': question.get('category', '安全评估'),
            'source': source,
            'prompt': question.get('prompt', ''),
            'answer': question.get('answer', ''),
            'explanation': question.get('explanation', '')
        }
        
        # 根据数据来源添加特定字段
        if source == 'safetyBench':
            processed['type'] = 'single'  # SafetyBench数据都是单选题
            processed['options'] = question.get('options', [])
            # 将A/B答案转换为0/1索引
            if processed['answer'] == 'A':
                processed['answer'] = '0'
            elif processed['answer'] == 'B':
                processed['answer'] = '1'
        elif source == 'poisonMpts':
            processed['type'] = 'essay'  # 毒化数据集都是问答题
        elif source == 'cValues':
            processed['type'] = 'essay'  # CValues数据集都是问答题
        elif source == 'instructionAttack':
            processed['type'] = 'essay'  # 指令攻击数据集都是问答题
        elif source == 'typicalSafety':
            processed['type'] = 'essay'  # 典型安全数据集都是问答题
        
        return processed
    except Exception as e:
        logger.error(f"处理题目时出错: {str(e)}")
        return None

@app.route('/api/questions/generate', methods=['POST'])
def generate_questions():
    """生成题库"""
    try:
        data = request.get_json()
        logger.debug(f"收到请求数据: {data}")
        
        question_count = data.get('questionCount', 10)
        selected_types = data.get('types', [])
        selected_sources = data.get('sources', [])
        selected_domains = data.get('domains', [])
        
        logger.debug(f"题目数量: {question_count}")
        logger.debug(f"选中的题型: {selected_types}")
        logger.debug(f"选中的数据源: {selected_sources}")
        logger.debug(f"选中的领域: {selected_domains}")
        
        all_questions = []
        
        # 从每个选中的来源加载题目
        for source in selected_sources:
            if source in QUESTION_FILES:
                questions = load_questions(source)
                processed_questions = [q for q in (process_question(q, source) for q in questions) if q is not None]
                all_questions.extend(processed_questions)
                logger.debug(f"从 {source} 加载了 {len(processed_questions)} 道题目")
        
        # 根据题型筛选
        if selected_types:
            all_questions = [q for q in all_questions if q['type'] in selected_types]
            logger.debug(f"按题型筛选后剩余 {len(all_questions)} 道题目")
        
        # 根据领域筛选
        if selected_domains:
            all_questions = [q for q in all_questions if q['category'] in selected_domains]
            logger.debug(f"按领域筛选后剩余 {len(all_questions)} 道题目")
        
        # 随机选择指定数量的题目
        random.shuffle(all_questions)
        selected_questions = all_questions[:question_count]
        
        logger.debug(f"最终选择了 {len(selected_questions)} 道题目")
        
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

@app.route('/api/questions/export-excel', methods=['POST'])
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
        
        logger.debug(f"准备导出 {len(questions)} 道题目为Excel")
        
        # 准备Excel数据
        excel_data = []
        for q in questions:
            row = {
                'ID': q.get('id', ''),
                '题型': get_type_name(q.get('type', '')),
                '问题': q.get('prompt', ''),
                '答案': q.get('answer', ''),
                '分类': q.get('category', ''),
                '来源': q.get('source', ''),
                '解析': q.get('explanation', '')
            }
            
            # 如果有选项，添加选项
            if 'options' in q and q['options']:
                for i, option in enumerate(q['options']):
                    row[f'选项{chr(65+i)}'] = option
            
            excel_data.append(row)
        
        # 创建DataFrame
        df = pd.DataFrame(excel_data)
        
        # 创建临时文件
        with tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False) as tmp:
            # 保存Excel
            with pd.ExcelWriter(tmp.name, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='题库', index=False)
                
                # 获取xlsxwriter工作簿和工作表对象
                workbook = writer.book
                worksheet = writer.sheets['题库']
                
                # 设置列宽
                worksheet.set_column('A:A', 10)  # ID列
                worksheet.set_column('B:B', 15)  # 题型列
                worksheet.set_column('C:C', 50)  # 问题列
                worksheet.set_column('D:D', 50)  # 答案列
                worksheet.set_column('E:E', 15)  # 分类列
                worksheet.set_column('F:F', 15)  # 来源列
                worksheet.set_column('G:G', 50)  # 解析列
                
                # 为选项列设置宽度
                max_options = max([len(q.get('options', [])) for q in questions if 'options' in q], default=0)
                for i in range(max_options):
                    worksheet.set_column(i + 7, i + 7, 30)  # 选项列
            
            tmp_path = tmp.name
        
        # 发送文件
        return send_file(
            tmp_path,
            as_attachment=True,
            download_name=f'题库_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx',
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
    except Exception as e:
        logger.error(f"导出Excel时出错: {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500
    
    finally:
        # 清理临时文件
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except Exception as e:
                logger.error(f"删除临时文件时出错: {str(e)}")

def get_type_name(type_code):
    """获取题型名称"""
    type_names = {
        'single': '单选题',
        'essay': '问答题',
        'unknown': '未知类型'
    }
    return type_names.get(type_code, '未知类型')

# 前端路由
@app.route('/', defaults={'path': ''})
@app.route('/cover')
@app.route('/question-generate')
@app.route('/question-bank')
@app.route('/question-preview')
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
    create_required_dirs()
    app.run(host='0.0.0.0', port=5000, debug=True) 