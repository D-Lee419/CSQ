import os
import json
import random
from pathlib import Path

# ========== 配置文件路径 ==========
RAW_FILE_PATH = ""
PROCESSED_PATH = Path("./processed/")
PROCESSED_TRAIN_FILE = PROCESSED_PATH.joinpath('train_processed.jsonl')

SPLIT_OUTPUT_PATH = Path("./finetune_demo/data/")
TRAIN_FILE = SPLIT_OUTPUT_PATH.joinpath('train_data.jsonl')
VAL_FILE = SPLIT_OUTPUT_PATH.joinpath('val_data.jsonl')
TEST_FILE = SPLIT_OUTPUT_PATH.joinpath('test_data.jsonl')

# ========== 数据预处理部分 ==========
def generate_datasets(raw_file_path: str):
    """将原始JSON文件转换为训练用JSONL格式"""
    if not PROCESSED_PATH.exists():
        PROCESSED_PATH.mkdir(parents=True, exist_ok=True)

    with open(raw_file_path, 'r', encoding='utf-8') as src_file, \
         open(PROCESSED_TRAIN_FILE, 'w', encoding='utf-8') as dst_file:
        data = json.load(src_file)
        for key, value in data.items():
            try:
                # 构建系统提示（包含年级、主题、类别、技能）
                system_prompt = (
                    f"回答学生的问题，给出正确答案和对应的思维过程。\n"
                    f"年级：{value['年级']}\n"
                    f"主题：{value['主题']}\n"
                    f"类别：{value['类别']}\n"
                    f"技能：{value['技能']}"
                )
                
                # 构建用户消息（仅包含题目和选项）
                user_content = (
                    f"题目：{value['题目']}\n"
                    f"选项：{'，'.join(value['选项'])}"
                )
                
                # 构建助手回复
                answer_index = value['答案'] - 1
                assistant_content = (
                    f"正确答案：{value['选项'][answer_index]}\n"
                    f"思维过程：{value['知识点']} -> {value['解题思路']}"
                )
                
                # 组装完整对话结构
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_content},
                    {"role": "assistant", "content": assistant_content}
                ]
                
                # 写入处理后的文件
                dst_file.write(json.dumps({"messages": messages}, ensure_ascii=False) + "\n")
                
            except Exception as e:
                print(f"处理条目 {key} 时出错: {str(e)}")
                continue

# ========== 数据拆分部分 ==========
def read_jsonl(file_path: str):
    """读取JSONL文件"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f]

def split_dataset(data: list, ratios: tuple = (0.8, 0.1, 0.1)):
    """按比例拆分数据集"""
    random.shuffle(data)
    total = len(data)
    train_end = int(total * ratios[0])
    val_end = train_end + int(total * ratios[1])
    return data[:train_end], data[train_end:val_end], data[val_end:]

def write_jsonl(data: list, file_path: Path):
    """写入JSONL文件"""
    with open(file_path, 'w', encoding='utf-8') as f:
        for item in data:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")

def process_pipeline():
    """完整处理流程"""
    # Step 1: 生成初始数据集
    print("正在生成预处理数据...")
    generate_datasets(RAW_FILE_PATH)
    
    # Step 2: 读取并拆分数据
    print("正在拆分数据集...")
    dataset = read_jsonl(PROCESSED_TRAIN_FILE)
    train, val, test = split_dataset(dataset)
    
    # Step 3: 写入拆分结果
    if not SPLIT_OUTPUT_PATH.exists():
        SPLIT_OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    
    write_jsonl(train, TRAIN_FILE)
    write_jsonl(val, VAL_FILE)
    write_jsonl(test, TEST_FILE)
    print(f"数据处理完成！\n训练集: {len(train)}条\n验证集: {len(val)}条\n测试集: {len(test)}条")

if __name__ == "__main__":
    process_pipeline()