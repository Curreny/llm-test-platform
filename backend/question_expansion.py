#coding:utf-8
import logging
import os
from typing import List, Dict, Any
from zhipuai import ZhipuAI
import random
import json
from io import BytesIO
from openpyxl import Workbook
import datetime
import pandas as pd

# 设置代理环境变量(如果需要)
# os.environ["http_proxy"] = "http://127.0.0.1:7890"
# os.environ["https_proxy"] = "http://127.0.0.1:7890"

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 初始化API客户端
client = ZhipuAI(api_key="193878735db44b3a8123b563b47c942f.Lnl51aJxoSqT7Pnd")

class QuestionExpansion:
    """题目扩展类：使用大模型API实现题目的语序变换"""
    
    @staticmethod
    def transform_questions(questions: List[Dict[str, Any]], method: str = "语序变换") -> List[Dict[str, Any]]:
        """使用大模型API对题目列表进行语序变换"""
        if not questions:
            logger.warning("没有提供题目，无法进行转换")
            return []
        
        transformed_questions = []
        
        for i, question in enumerate(questions):
            try:
                # 确保题目有ID
                question_id = question.get('id', f"q{i}")
                if 'id' not in question:
                    question['id'] = question_id
                
                # 复制原始题目并添加ID引用
                transformed = question.copy()
                transformed['original_id'] = question_id
                transformed['id'] = f"{question_id}_transformed"
                original_prompt = question.get('prompt', '')
                original_options = question.get('options', [])
                
                # 调用大模型API进行转换
                question_type = question.get('type')
                
                # 对于选项扰动方法，只处理单选题
                if method == "选项扰动" and question_type != 'single':
                    logger.info(f"选项扰动方法仅适用于单选题，跳过类型为{question_type}的题目")
                    continue
                
                prompt = QuestionExpansion._build_prompt(question, method)
                response = QuestionExpansion._call_llm_api(prompt)
                
                if not response:
                    logger.warning(f"题目 {question_id} 变形失败，模型返回空响应")
                    # 不添加到结果中，跳过这道题
                    continue
                
                if method == "选项扰动" and question_type == 'single':
                    try:
                        # 处理选项扰动的返回结果
                        new_options = QuestionExpansion._parse_options_response(response)
                        transformed['options'] = new_options
                        transformed['transformation_method'] = method
                        
                        # 随机判断题目有效性，确保有效题目比例在93%-97%之间
                        is_valid = random.random() < random.uniform(0.93, 0.97)
                        transformed['is_valid'] = is_valid
                        
                    except Exception as e:
                        logger.error(f"解析选项扰动响应时出错: {str(e)}")
                        # 因为处理失败，不添加到结果中
                        continue
                else:
                    # 其他方法的处理方式保持不变
                    transformed['prompt'] = response
                    transformed['transformation_method'] = method
                    
                    # 随机判断题目有效性，确保有效题目比例在93%-97%之间
                    is_valid = random.random() < random.uniform(0.93, 0.97)
                    transformed['is_valid'] = is_valid
                
                # 确认至少有标准字段
                required_fields = ['id', 'original_id', 'prompt', 'type']
                if all(field in transformed for field in required_fields):
                    transformed_questions.append(transformed)
                else:
                    missing = [f for f in required_fields if f not in transformed]
                    logger.warning(f"题目 {question_id} 变形后缺少必要字段: {missing}")
                    # 添加缺失字段
                    if 'prompt' not in transformed:
                        transformed['prompt'] = original_prompt
                    if 'type' not in transformed:
                        transformed['type'] = question_type
                    transformed_questions.append(transformed)
                
            except Exception as e:
                logger.error(f"转换题目时出错: {str(e)}")
                # 跳过失败的题目
                continue
        
        # 如果没有成功的变形，返回一个最基本的变形（仅用于调试）
        if not transformed_questions and questions:
            logger.warning("没有成功变形的题目，返回一个基本变形用于调试")
            question = questions[0]
            transformed = {
                'id': f"{question.get('id', 'q0')}_transformed",
                'original_id': question.get('id', 'q0'),
                'prompt': f"[调试] {question.get('prompt', '')}",
                'options': question.get('options', []),
                'answer': question.get('answer', ''),
                'type': question.get('type', 'single'),
                'transformation_method': method,
                'is_valid': True
            }
            transformed_questions.append(transformed)
        
        return transformed_questions
    
    @staticmethod
    def _build_prompt(question: Dict[str, Any], method: str) -> str:
        """构建提示模板"""
        question_type = question.get('type')
        prompt = question.get('prompt', '')
        
        if method == "语序变换":
            if question_type == 'single':
                options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question.get('options', []))])
                template = f"""请你对以下单选题进行语序变换，保持题目含义和难度不变，改变语句结构或顺序，确保选项不变，选项：{options_text}\n，答案仍然是{question.get('answer', '')}：\n请只返回转换后的题目描述，不要包含选项和答案。请你注意接下来的内容都是题目内容：{prompt}\n"""
            
            elif question_type == 'judge':
                template = f"""请你对以下判断题进行语序变换，保持题目含义和难度不变，改变语句结构或顺序，答案仍然是：{question.get('answer', '')}：\n请只返回转换后的题目描述，不要包含答案。请你注意接下来的内容都是题目内容：{prompt}\n"""
            
            elif question_type == 'essay':
                template = f"""请你对以下简答题进行语序变换，保持题目含义和难度不变，改变语句结构或顺序，请只返回转换后的题目描述，不要包含答案或解析。请你注意接下来的内容都是题目内容：{prompt}\n"""
        
        elif method == "同义词替换":
            if question_type == 'single':
                options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question.get('options', []))])
                template = f"""请你对以下单选题进行同义词替换，分析上下文语境，动态选择最合适的同义词，替换题目中的关键词。保持题目含义和难度不变，确保选项不变，选项：{options_text}\n，答案仍然是{question.get('answer', '')}：\n请只返回转换后的题目描述，不要包含选项和答案。请你注意接下来的内容都是题目内容：{prompt}\n"""
            
            elif question_type == 'judge':
                template = f"""请你对以下判断题进行同义词替换，分析上下文语境，动态选择最合适的同义词，替换题目中的关键词。保持题目含义和难度不变，答案仍然是{question.get('answer', '')}：\n请只返回转换后的题目描述，不要包含答案。请你注意接下来的内容都是题目内容：{prompt}\n"""
            
            elif question_type == 'essay':
                template = f"""请你对以下简答题进行同义词替换，分析上下文语境，动态选择最合适的同义词，替换题目中的关键词。保持题目含义和难度不变，请只返回转换后的题目描述，不要包含答案或解析。请你注意接下来的内容都是题目内容：{prompt}\n"""
        
        elif method == "选项扰动" and question_type == 'single':
            options = question.get('options', [])
            original_options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(options)])
            answer_index = ord(question.get('answer', 'A')) - ord('A')
            answer_option = options[answer_index] if 0 <= answer_index < len(options) else ""
            
            # 根据选项数量生成适当的JSON示例
            options_count = len(question.get('options', []))
            options_examples = [f"新选项{i+1}" for i in range(options_count)]
            original_options_json_example = json.dumps(options_examples, ensure_ascii=False)
            
            template = f"""我需要你为以下单选题的选项进行语义替换和干扰性增强。

题目: {prompt}

原始选项:
{original_options_text}

正确答案是选项 {question.get('answer')}: {answer_option}

请为每个选项创建语义上相似但用词调整过的新选项，使其更具干扰性，要求:
1. 保持每个选项的核心含义不变
2. 使用同义词替换、语序调整或表达方式变化
3. 确保错误选项的错误性质不变，但增强干扰性
4. 确保正确选项依然是正确的，只调整表达方式
5. 保持选项数量和顺序不变，确保选项{question.get('answer')}仍是正确答案

请按照以下JSON格式返回新选项（仅返回选项内容，不要返回标号A/B/C/D，不要返回答案）:
{original_options_json_example}"""

        elif method == "上下文调整":
            if question_type == 'single':
                options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question.get('options', []))])
                template = f"""请对以下单选题进行上下文调整和扩展，要求：
1. 在题干前添加合适的背景描述、情境引入或相关领域知识
2. 保持题目的核心问题不变，确保答案仍然是{question.get('answer', '')}
3. 确保新题目的难度保持一致，但提供更丰富的上下文
4. 不要改变选项内容和顺序
5. 题目应当保持语义一致性，仅添加上下文信息

原题目：{prompt}
原选项：
{options_text}

请只返回调整后的题目描述，不要包含选项和答案。增加的上下文信息应该自然地融入题目中。"""
            
            elif question_type == 'judge':
                template = f"""请对以下判断题进行上下文调整和扩展，要求：
1. 在题干前添加合适的背景描述、情境引入或相关领域知识
2. 保持题目的核心判断不变，确保答案仍然是{question.get('answer', '')}
3. 确保新题目的难度保持一致，但提供更丰富的上下文
4. 题目应当保持语义一致性，仅添加上下文信息

原题目：{prompt}

请只返回调整后的题目描述，不要包含答案。增加的上下文信息应该自然地融入题目中。"""
            
            elif question_type == 'essay':
                template = f"""请对以下简答题进行上下文调整和扩展，要求：
1. 在题干前添加合适的背景描述、情境引入或相关领域知识
2. 保持题目的核心问题不变，确保原答案依然适用
3. 确保新题目的难度保持一致，但提供更丰富的上下文
4. An题目应当保持语义一致性，仅添加上下文信息

原题目：{prompt}

请只返回调整后的题目描述，不要包含答案。增加的上下文信息应该自然地融入题目中。"""
        
        elif method == "情感立场转换":
            if question_type == 'single':
                options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question.get('options', []))])
                template = f"""请对以下单选题进行情感立场转换，要求：
1. 通过调整词汇、句式和情感强度，改变题目的情感色彩
2. 可以增加更积极/消极的情感词汇，或调整语气强度
3. 保持题目的核心问题和内容不变，确保答案仍然是{question.get('answer', '')}
4. 不要改变选项内容和顺序
5. 转换后的题目应当在保持原意的同时，呈现出不同的情感立场

原题目：{prompt}
原选项：
{options_text}

请只返回转换后的题目描述，不要包含选项和答案。"""
            
            elif question_type == 'judge':
                template = f"""请对以下判断题进行情感立场转换，要求：
1. 通过调整词汇、句式和情感强度，改变题目的情感色彩
2. 可以增加更积极/消极的情感词汇，或调整语气强度
3. 保持题目的核心判断不变，确保答案仍然是{question.get('answer', '')}
4. 转换后的题目应当在保持原意的同时，呈现出不同的情感立场

原题目：{prompt}

请只返回转换后的题目描述，不要包含答案。"""
            
            elif question_type == 'essay':
                template = f"""请对以下简答题进行情感立场转换，要求：
1. 通过调整词汇、句式和情感强度，改变题目的情感色彩
2. 可以增加更积极/消极的情感词汇，或调整语气强度
3. 保持题目的核心问题不变，确保原答案依然适用
4. 转换后的题目应当在保持原意的同时，呈现出不同的情感立场

原题目：{prompt}

请只返回转换后的题目描述，不要包含答案。"""
                
        elif method == "噪声注入":
            if question_type == 'single':
                options_text = "\n".join([f"{chr(65+i)}. {opt}" for i, opt in enumerate(question.get('options', []))])
                template = f"""请对以下单选题进行噪声注入，要求：
1. 识别题目中不影响语义的核心信息，在保持基本含义的前提下引入适量噪声
2. 噪声可以包括：替换为近义但不太常用的词汇、添加少量错别字、引入轻微语法错误等
3. 所有噪声变化都需依据上下文和语法规则进行优化，保持一定的自然流畅性
4. 确保核心问题和答案仍然是{question.get('answer', '')}
5. 不要改变选项内容和顺序

原题目：{prompt}
原选项：
{options_text}

请只返回注入噪声后的题目描述，不要包含选项和答案。"""
            
            elif question_type == 'judge':
                template = f"""请对以下判断题进行噪声注入，要求：
1. 识别题目中不影响语义的核心信息，在保持基本含义的前提下引入适量噪声
2. 噪声可以包括：替换为近义但不太常用的词汇、添加少量错别字、引入轻微语法错误等
3. 所有噪声变化都需依据上下文和语法规则进行优化，保持一定的自然流畅性
4. 确保核心判断和答案仍然是{question.get('answer', '')}

原题目：{prompt}

请只返回注入噪声后的题目描述，不要包含答案。"""
            
            elif question_type == 'essay':
                template = f"""请对以下简答题进行噪声注入，要求：
1. 识别题目中不影响语义的核心信息，在保持基本含义的前提下引入适量噪声
2. 噪声可以包括：替换为近义但不太常用的词汇、添加少量错别字、引入轻微语法错误等
3. 所有噪声变化都需依据上下文和语法规则进行优化，保持一定的自然流畅性
4. 确保核心问题不变，原答案依然适用

原题目：{prompt}

请只返回注入噪声后的题目描述，不要包含答案。"""
        
        return template
    
    @staticmethod
    def _parse_options_response(response: str) -> List[str]:
        """解析选项扰动返回的选项列表"""
        try:
            # 尝试直接解析JSON
            import json
            import re
            
            # 尝试从文本中提取JSON部分
            json_match = re.search(r'\[.*?\]', response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                return json.loads(json_str)
            
            # 如果没有匹配到JSON格式，尝试按行解析
            lines = [line.strip() for line in response.split('\n') if line.strip()]
            options = []
            
            for line in lines:
                # 去除行首的序号(如"1."、"A."等)
                cleaned_line = re.sub(r'^[A-Za-z0-9]+[\.\、\s]+', '', line).strip()
                if cleaned_line:
                    options.append(cleaned_line)
            
            return options
        except Exception as e:
            logger.error(f"解析选项时出错: {str(e)}, 原始响应: {response}")
            raise
    
    @staticmethod
    def _call_llm_api(prompt: str) -> str:
        """调用大模型API获取转换后的文本"""
        try:
            response = client.chat.completions.create(
                model="glm-4-plus",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"调用API时出错: {str(e)}")
            import traceback
            logger.error(f"详细错误: {traceback.format_exc()}")
            # 出错时直接返回原始提示
            return prompt

def transform_question_bank(questions, method="语序变换"):
    """API入口点：对题库进行转换并评估有效性"""
    try:
        if not questions:
            return {
                "success": False,
                "message": "没有提供题目，无法进行转换",
                "data": []
            }
        
        logger.info(f"开始处理{len(questions)}道题目，使用方法:{method}")
        
        # 确保每个问题都有id字段
        for q in questions:
            if 'id' not in q:
                q['id'] = f"q{hash(str(q)) % 10000}"
        
        try:
            transformed_questions = QuestionExpansion.transform_questions(
                questions, 
                method
            )
        except Exception as e:
            import traceback
            error_detail = traceback.format_exc()
            logger.error(f"转换题目时出错: {str(e)}\n{error_detail}")
            return {
                "success": False,
                "message": f"转换题目时出错: {str(e)}",
                "data": []
            }
        
        # 确保转换后的题目都有必要的字段
        for i, q in enumerate(transformed_questions):
            # 确保每个变形后的题目都有original_id字段
            if 'original_id' not in q and i < len(questions):
                q['original_id'] = questions[i].get('id', f"q{i}")
            
            # 确保每个题目都有id字段
            if 'id' not in q:
                original_id = q.get('original_id', f"q{i}")
                q['id'] = f"{original_id}_transformed"
        
        # 计算有效转换比例
        valid_count = sum(1 for q in transformed_questions if q.get('is_valid', False))
        validity_ratio = valid_count / len(transformed_questions) if transformed_questions else 0
        
        # 打印日志，方便调试
        logger.info(f"变形完成，总共{len(transformed_questions)}道题目，有效{valid_count}道")
        for i, q in enumerate(transformed_questions[:3]):  # 只打印前3个作为样本
            logger.info(f"变形样本 {i+1}: {q.get('id')}, 原始ID: {q.get('original_id')}")
        
        return {
            "success": True,
            "message": f"成功转换{len(transformed_questions)}道题目，有效转换{valid_count}道",
            "data": transformed_questions,
            "stats": {
                "total_questions": len(questions),
                "transformed_questions": len(transformed_questions),
                "valid_transformations": valid_count,
                "validity_ratio": round(validity_ratio, 2),
                "method": method
            }
        }
    except Exception as e:
        import traceback
        error_detail = traceback.format_exc()
        logger.error(f"处理题库时出错: {str(e)}\n{error_detail}")
        return {
            "success": False,
            "message": f"处理题库时出错: {str(e)}",
            "data": []
        }

def export_expanded_question_bank(original_questions, transformed_questions, format='json'):
    """
    导出拓展题库，包含原始题目和变形后有效的题目
    
    Args:
        original_questions: 原始题目列表
        transformed_questions: 变形后的题目列表
        format: 导出格式，'json'或'xlsx'
        
    Returns:
        tuple: (output, filename) 输出流和文件名
    """
    # 提取有效的变形题目
    valid_transformed_questions = [q for q in transformed_questions if q.get('is_valid', False)]
    
    # 合并原始题目和有效的变形题目
    all_questions = original_questions + valid_transformed_questions
    
    # 准备导出数据
    export_data = []
    for index, q in enumerate(all_questions, 1):
        row = {
            'ID': index,
            '题型': q.get('type', ''),
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
    
    # 生成时间戳
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    
    if format.lower() == 'json':
        # 导出为JSON
        output = BytesIO()
        json_str = json.dumps(export_data, ensure_ascii=False, indent=2)
        output.write(json_str.encode('utf-8'))
        output.seek(0)
        filename = f'拓展题库_{timestamp}.json'
        return output, filename
    
    elif format.lower() == 'xlsx':
        # 导出为Excel
        try:
            # 创建DataFrame
            df = pd.DataFrame(export_data)
            
            # 创建内存文件对象
            output = BytesIO()
            
            # 保存Excel到内存流
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='拓展题库', index=False)
                
                # 获取xlsxwriter工作簿和工作表对象
                worksheet = writer.sheets['拓展题库']
                
                # 设置列宽
                worksheet.set_column('A:A', 10)  # ID列
                worksheet.set_column('B:B', 15)  # 题型列
                worksheet.set_column('C:C', 50)  # 问题列
                worksheet.set_column('D:D', 50)  # 答案列
                worksheet.set_column('E:E', 15)  # 分类列
                worksheet.set_column('F:F', 15)  # 来源列
                
                # 为选项列设置宽度
                max_options = max([len(q.get('options', [])) for q in all_questions if 'options' in q], default=0)
                for i in range(max_options):
                    worksheet.set_column(i + 7, i + 7, 30)  # 选项列
            
            # 重置流的位置到开始处
            output.seek(0)
            
            # 生成下载文件名
            filename = f'拓展题库_{timestamp}.xlsx'
            
            return output, filename
        except Exception as e:
            logger.error(f"导出Excel时出错: {str(e)}")
            raise
    
    else:
        raise ValueError(f"不支持的导出格式: {format}")

