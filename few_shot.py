from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 加载模型和分词器
model_name = ""
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True).half().cuda()
model.eval()

# 1-shot 示例数据
one_shot_example = {
    "年级": "四年级",
    "任务": "选择正确答案",
    "题目": "水是由什么组成的？",
    "选项": "A. 氧气和氢气  B. 二氧化碳  C. 氢气和氦气",
    "答案": "A",
    "提示": "水的化学式是H2O。",
    "知识点": "水的组成",
    "解题思路": "水是由氢元素和氧元素组成的。",
    "主题": "物质科学",
    "类别": "基础知识",
    "技能": "分析与推理"
}

# 需要预测的数据
input_data = {
    "年级": "四年级",
    "任务": "选择正确答案",
    "题目": "植物进行光合作用需要哪些要素？",
    "选项": "A. 太阳光、水、二氧化碳  B. 水和土壤  C. 只有阳光",
    "答案": "",  
    "提示": "植物需要阳光和空气中的二氧化碳进行光合作用。",
    "知识点": "",  
    "解题思路": "",  
    "主题": "生命科学",
    "类别": "基础知识",
    "技能": "分析与推理"
}

# 构造 Prompt
prompt = f"""You are a primary school student at the specified grade level. 
Please choose the correct answer from the options provided for the question.
The topics, subjects, and skills are intended to aid in generating a solution.
Your response should include the knowledge point and problem-solving approach.

[Input of Model]:
Question: {one_shot_example['题目']}  
Option: {one_shot_example['选项']}  
Skills: {one_shot_example['技能']}

Context: {one_shot_example['提示']}  
Topic: {one_shot_example['主题']}  
Disciplines: {one_shot_example['类别']}

[Output of Model]:
Answer: The answer is {one_shot_example['答案']}.  
Knowledge Point: {one_shot_example['知识点']}  
Problem-Solving Approach: {one_shot_example['解题思路']}  

[Input of Model]:
Question: {input_data['题目']}  
Option: {input_data['选项']}  
Skills: {input_data['技能']}

Context: {input_data['提示']}  
Topic: {input_data['主题']}  
Disciplines: {input_data['类别']}

[Output of Model]:
Answer: The answer is"""

# 进行推理
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
with torch.no_grad():
    output = model.generate(**inputs, max_length=512, pad_token_id=tokenizer.eos_token_id)

# 解码结果
generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
print(generated_text)