import json
import random

def pick_SafetyBench(num_questions):
    file_path = 'SafetyBench_data.json'
    try:
        # 加载 JSON 数据
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        
        # 确保数据是一个列表
        if not isinstance(data, list):
            raise ValueError("JSON 文件必须包含一个题目列表。")
        
        # 随机选择指定数量的题目
        selected_questions = random.sample(data, min(num_questions, len(data)))
        
        # 打印选中的题目
        for i, question in enumerate(selected_questions, 1):
            print(f"题目 {i}: {question}")
    
    except FileNotFoundError:
        print(f"错误：未找到文件 {file_path}")
    except json.JSONDecodeError:
        print("错误：解析 JSON 失败，请检查文件格式。")
    except ValueError as e:
        print(f"错误：{e}")



# 调用函数
pick_SafetyBench(50)