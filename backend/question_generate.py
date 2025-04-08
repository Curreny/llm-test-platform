import os
import json
import random
import logging
from io import BytesIO
import pandas as pd

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 数据文件路径
DATA_DIR = 'data'
QUESTION_FILES = {
    '100PoisonMpts': '100PoisonMpts.json',
    'CValues-Comparison': 'CValues-Comparison.json',
    'instruction_attack': 'instruction_attack.json',
    'SafetyBench_choice': 'SafetyBench_choice.json',  # 新的单选题文件
    'SafetyBench_judge': 'SafetyBench_judge.json',    # 新的判断题文件
    'typical_safety': 'typical_safety.json'
}

class QuestionGenerateManager:
    """题库管理类，负责题库数据的加载、处理和生成"""
    
    # 添加一个类变量来存储当前生成的题库
    current_question_bank = []
    
    @staticmethod
    def load_questions(source):
        """加载指定来源的题库数据"""
        try:
            file_path = os.path.join(DATA_DIR, QUESTION_FILES[source])
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data
        except FileNotFoundError:
            logger.error(f"找不到数据文件: {file_path}")
            return []
        except Exception as e:
            logger.error(f"加载数据文件时出错: {str(e)}")
            return []

    @staticmethod
    def process_question(question, source):
        """根据数据来源处理题目格式"""
        try:
            processed = {
                'id': question.get('id', ''),
                'type': question.get('type', 'essay'),  # 默认为问答题
                'domain': question.get('domain', 'Other domain'),
                'source': source,
                'prompt': question.get('prompt', ''),
                'answer': question.get('answer', '')
            }
            
            # 根据数据来源添加特定字段
            if source == 'SafetyBench_choice':
                processed['type'] = 'single'  # SafetyBench单选题
                processed['options'] = question.get('options', [])
            elif source == 'SafetyBench_judge':
                processed['type'] = 'judge'  # SafetyBench判断题
                processed['options'] = question.get('options', [])
            elif source == '100PoisonMpts':
                processed['type'] = 'essay'  # 毒化数据集都是问答题
            elif source == 'CValues-Comparison':
                processed['type'] = 'essay'  # CValues数据集都是问答题
            elif source == 'instruction_attack':
                processed['type'] = 'essay'  # 指令攻击数据集都是问答题
            elif source == 'typical_safety':
                processed['type'] = 'essay'  # 典型安全数据集都是问答题
            
            return processed
        except Exception as e:
            logger.error(f"处理题目时出错: {str(e)}")
            return None

    @classmethod
    def generate_question_bank(cls, types_request, selected_domains=None):
        """生成题库"""
        try:
            all_questions = []
            
            # 从所有来源加载题目
            for source in QUESTION_FILES:
                questions = cls.load_questions(source)
                processed_questions = [q for q in (cls.process_question(q, source) for q in questions) if q is not None]
                all_questions.extend(processed_questions)
            
            # 根据领域筛选
            if selected_domains:
                all_questions = [q for q in all_questions if q['domain'] in selected_domains]
            
            # 根据题型和数量筛选
            selected_questions = []
            for type_request in types_request:
                question_type = type_request.get('type')
                count = type_request.get('count', 0)
                
                if question_type and count > 0:
                    type_questions = [q for q in all_questions if q['type'] == question_type]
                    random.shuffle(type_questions)
                    selected_questions.extend(type_questions[:count])
            
            # 更新当前题库
            cls.current_question_bank = selected_questions
            
            return selected_questions
        except Exception as e:
            logger.error(f"生成题库时出错: {str(e)}")
            raise

    @classmethod
    def get_current_question_bank(cls):
        """获取当前题库"""
        return cls.current_question_bank

    @classmethod
    def clear_question_bank(cls):
        """清空当前题库"""
        cls.current_question_bank = []
        return True

    @staticmethod
    def get_type_name(type_code):
        """获取题型名称"""
        type_names = {
            'single': '单选题',
            'judge': '判断题',
            'essay': '问答题',
            'unknown': '未知类型'
        }
        return type_names.get(type_code, '未知类型')

class ExportManager:
    """导出管理类，负责题库的导出功能"""
    
    @staticmethod
    def prepare_export_data(questions):
        """准备导出数据的通用方法"""
        if not questions:
            raise ValueError('没有可导出的题目')
        
        export_data = []
        for index, q in enumerate(questions, 1):
            row = {
                'ID': index,
                '题型': QuestionGenerateManager.get_type_name(q.get('type', '')),
                '问题': q.get('prompt', ''),
                '答案': q.get('answer', ''),
                '领域': q.get('domain', ''),
                '来源': q.get('source', '')
            }
            
            # 如果有选项，添加选项
            if 'options' in q and q['options']:
                for i, option in enumerate(q['options']):
                    row[f'选项{chr(65+i)}'] = option
            
            export_data.append(row)
        
        return export_data

    @classmethod
    def export_to_excel(cls, questions):
        """导出题库为Excel文件"""
        try:
            excel_data = cls.prepare_export_data(questions)
            
            # 创建DataFrame
            df = pd.DataFrame(excel_data)
            
            # 创建内存文件对象
            output = BytesIO()
            
            # 保存Excel到内存流
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='题库', index=False)
                
                # 获取xlsxwriter工作簿和工作表对象
                worksheet = writer.sheets['题库']
                
                # 设置列宽
                worksheet.set_column('A:A', 10)  # ID列
                worksheet.set_column('B:B', 15)  # 题型列
                worksheet.set_column('C:C', 50)  # 问题列
                worksheet.set_column('D:D', 50)  # 答案列
                worksheet.set_column('E:E', 15)  # 分类列
                worksheet.set_column('F:F', 15)  # 来源列
                
                # 为选项列设置宽度
                max_options = max([len(q.get('options', [])) for q in questions if 'options' in q], default=0)
                for i in range(max_options):
                    worksheet.set_column(i + 7, i + 7, 30)  # 选项列
            
            # 重置流的位置到开始处
            output.seek(0)
            
            # 生成下载文件名
            filename = f'题库_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
            
            return output, filename
        except Exception as e:
            logger.error(f"导出Excel时出错: {str(e)}")
            raise

    @classmethod
    def export_to_json(cls, questions):
        """导出题库为JSON文件"""
        try:
            json_data = cls.prepare_export_data(questions)
            
            # 将数据转换为JSON字符串
            json_str = json.dumps(json_data, ensure_ascii=False, indent=2)
            
            # 创建内存文件对象
            output = BytesIO(json_str.encode('utf-8'))
            
            # 生成下载文件名
            filename = f'题库_{pd.Timestamp.now().strftime("%Y%m%d_%H%M%S")}.json'
            
            return output, filename
        except Exception as e:
            logger.error(f"导出JSON时出错: {str(e)}")
            raise 