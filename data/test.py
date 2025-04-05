import json
import os

def extract_true_false_questions(input_file, output_file, filtered_output_file):
    """
    从SafetyBench数据集中提取判断题
    判断题的options中通常只有两个选项，并且是以下几种形式：
    1. ["是。","否。"]
    2. ["对", "错"]
    3. ["正确", "错误"]
    
    同时将原数据集中的判断题移除并重新排序ID
    """
    # 读取原始数据
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    print(f"原始数据共有 {len(data)} 道题目")
    
    # 判断题特征列表
    true_false_patterns = [
        ["是。", "否。"],
        ["对", "错"],
        ["正确", "错误"],
        ["是", "否"],
        ["对。", "错。"],
        ["√", "×"]
    ]
    
    # 提取判断题
    true_false_questions = []
    non_true_false_questions = []
    
    for question in data:
        is_true_false = False
        
        if "options" in question and len(question["options"]) == 2:
            options = question["options"]
            for pattern in true_false_patterns:
                # 检查是否与某种判断题模式匹配
                if (options[0].strip() == pattern[0] and options[1].strip() == pattern[1]) or \
                   (options[1].strip() == pattern[0] and options[0].strip() == pattern[1]):
                    true_false_questions.append(question.copy())
                    is_true_false = True
                    break
        
        if not is_true_false:
            non_true_false_questions.append(question.copy())
    
    print(f"判断题共有 {len(true_false_questions)} 道")
    print(f"非判断题共有 {len(non_true_false_questions)} 道")
    
    # 重新排序判断题ID
    for i, question in enumerate(true_false_questions, 1):
        question["id"] = i
    
    # 重新排序非判断题ID
    for i, question in enumerate(non_true_false_questions, 1):
        question["id"] = i
    
    # 保存判断题到新文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(true_false_questions, f, ensure_ascii=False, indent=4)
    
    # 保存非判断题(过滤后的原始数据)到文件
    with open(filtered_output_file, 'w', encoding='utf-8') as f:
        json.dump(non_true_false_questions, f, ensure_ascii=False, indent=4)
    
    print(f"判断题已保存到 {output_file}")
    print(f"非判断题已保存到 {filtered_output_file}")
    
    return true_false_questions, non_true_false_questions

if __name__ == "__main__":
    # 路径配置
    current_dir = os.path.dirname(os.path.abspath(__file__))
    input_file = os.path.join(current_dir, "SafetyBench_data.json")
    output_file = os.path.join(current_dir, "SafetyBench_true_false.json")
    filtered_output_file = os.path.join(current_dir, "SafetyBench_filtered.json")
    
    # 提取判断题并过滤原数据
    true_false_questions, non_true_false_questions = extract_true_false_questions(
        input_file, output_file, filtered_output_file
    )
    
    # 输出前5道判断题作为示例
    try:
        print("\n前5道判断题示例:")
        for i, q in enumerate(true_false_questions[:5], 1):
            print(f"{i}. {q['prompt']} [选项: {q['options']}]")
            
        print("\n前5道非判断题示例:")
        for i, q in enumerate(non_true_false_questions[:5], 1):
            print(f"{i}. {q['prompt']}")
    except Exception as e:
        print(f"读取结果时出错: {e}")
        
    print("\n是否要将过滤后的非判断题保存回原文件？")
    response = input("输入 'Y' 确认，任意其他键取消: ")
    
    if response.strip().upper() == 'Y':
        # 将过滤后的非判断题保存回原始文件
        with open(input_file, 'w', encoding='utf-8') as f:
            json.dump(non_true_false_questions, f, ensure_ascii=False, indent=4)
        print(f"已将过滤后的非判断题保存回原文件 {input_file}")
    else:
        print("操作取消，原文件未修改")
