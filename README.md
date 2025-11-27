
# CSQ: A Chinese Elementary Science Question Dataset in Problem-Solving Process Generation

## 📖 Overview

**CSQ (Chinese Science Question)** is a high-quality dataset designed to evaluate and enhance the science problem-solving capabilities of Large Language Models (LLMs), specifically adapted to Chinese elementary school grade levels.

Although LLMs demonstrate potential in education, they often struggle to generate problem-solving processes that align with the cognitive development and knowledge structure of primary school students. CSQ addresses this by providing **12,000** examples covering four major scientific subjects, annotated with fine-grained discipline properties and grade-appropriate reasoning steps.

### Key Features

- **🇨🇳 Chinese Context:** Aligned with the *Science Curriculum Standards for Compulsory Education of China (2022)*.
- **📚 Diverse Subjects:** Covers Life Science, Physical Science, Earth & Universe Science, and Technology & Engineering.
- **🏫 Grade-Adaptive:** Annotations distinguish between Grade 1-6 cognitive levels.
- **🧠 Rich Annotations:** Each sample includes problem information, discipline properties (topic, knowledge, scientific skills), and a detailed solution thought process.


## 📂 Dataset Details

The dataset is available at [Science Data Bank](https://doi.org/10.57760/sciencedb.22816).

### Statistics

The CSQ dataset contains **12,000** questions. The distribution is as follows:

| Subject                              | Number of Questions | Percentage |
| :----------------------------------- | :-----------------: | :--------: |
| **Life Science (LS)**                |        3,660        |   30.5%    |
| **Physical Science (PS)**            |        3,746        |   31.2%    |
| **Earth and Universe Science (EUS)** |        2,526        |   21.0%    |
| **Technology and Engineering (TE)**  |        2,068        |   17.2%    |
| **Total**                            |     **12,000**      |  **100%**  |

- **Question Types:** 6,805 Multiple Choice (56.7%) and 5,195 True/False (43.3%).
- **Data Split:** Training (80%), Validation (10%), Test (10%).

### Data Structure

Each entry in `CSQ.json` contains three main components:

1.  **Problem Information:** Question text, options, type.
2.  **Discipline Properties:** Subject, Topic, Grade, Knowledge point, Scientific Skills.
3.  **Solution:** Correct answer and the *Problem-Solving Thought* (CoT).

#### Example (JSON Format)

```json
{
  "id": "10001",
  "problem_information": {
    "question": "下列能表示一条完整食物链的是？",
    "options": {
      "A": "“鼠→狼→虎”",
      "B": "“虾→鱼→鹭”",
      "C": "“水稻→鼠→猫头鹰”"
    },
    "type": "选择题"
  },
  "discipline_properties": {
    "subject": "生命科学",
    "topic": "生物与环境的相互关系",
    "grade": "五年级下册",
    "knowledge": "食物链是生产者和消费者存在的一种吃玉被吃的关系",
    "scientific_skills": [
      "比较事物的本质特征",
      "抽象出事物的本质特征"
    ]
  },
  "solution": {
    "answer": "C",
    "thought": "食物链的起点是生产者，一般是绿色植物，终点是消费者，箭头指向吃的一方。完整的食物链是水稻→鼠→猫头鹰。第一和第二个选项都缺少生产者。第三个选项正确。因此选择第三个选项。"
  }
}
```

## 🛠️ Usage

### Repository Structure

The dataset and code structure is organized as follows:

- `CSQ.json`: The main dataset file containing 12,000 samples.
- `skill_framework.csv`: The framework of scientific skills developed based on SCSCEC (2022).
- `data_p.py`: Python sample code for processing the dataset and generating question-answer pairs.
- `few-shot.py`: Sample code for performing few-shot reasoning with LLMs on the CSQ dataset.

### Data Format

The `CSQ.json` file is a list of JSON objects. Each object represents a single question entry:

| Key                     | Description                                                  |
| :---------------------- | :----------------------------------------------------------- |
| `problem_information`   | Contains the `question`, `options` (for multiple choice), and `type` (Choice/True-False). |
| `discipline_properties` | Detailed metadata including `subject` (e.g., Life Science), `topic`, `grade` level, specific `knowledge` point, and required `scientific_skills`. |
| `solution`              | Contains the correct `answer` and the `thought` (problem-solving process). |

### Quick Start

To load the dataset in Python:

```python
import json

# Load the dataset
with open('CSQ.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Access the first item
first_item = data[0]
print(f"Question: {first_item['problem_information']['question']}")
print(f"Answer: {first_item['solution']['answer']}")
print(f"Thought: {first_item['solution']['thought']}")
```

To run the few-shot evaluation (example command):

```bash
# Ensure you have the model weights and environment set up
python few-shot.py --model_path /path/to/model --data_path CSQ.json
```

---

## 📊 Experiments & Results

We conducted extensive experiments to evaluate Large Language Models (LLMs) on CSQ. We tested both zero-shot/few-shot performance and the effectiveness of fine-tuning.

### Main Results (Accuracy %)

The following table summarizes the accuracy of selected models across different subjects and grade levels:

| Model          | Setting        | Life Science | Physical Science | Earth & Univ. | Tech & Eng. | Grade 1-3 | Grade 4-6 |
| :------------- | :------------- | :----------: | :--------------: | :-----------: | :---------: | :-------: | :-------: |
| **GLM-9B**     | 0-shot         |     79.1     |       71.2       |     73.4      |    76.7     |   76.0    |   72.8    |
|                | **Fine-tuned** |   **88.1**   |     **80.9**     |   **84.1**    |  **86.2**   | **85.9**  | **84.7**  |
| **Qwen2.5-7B** | 0-shot         |     78.1     |       74.6       |     71.8      |    77.0     |   76.9    |   73.9    |
|                | **Fine-tuned** |   **89.2**   |     **84.3**     |   **85.5**    |  **84.6**   | **86.7**  | **85.7**  |
| **Yi1.5-9B**   | 0-shot         |     79.4     |       73.2       |     76.2      |    74.9     |   77.2    |   75.5    |
|                | **Fine-tuned** |   **89.1**   |     **82.3**     |   **87.1**    |  **84.6**   | **86.0**  | **85.0**  |
| **GPT-4o**     | 2-shot         |     91.6     |       86.8       |     89.7      |    89.2     |   91.4    |   87.9    |

### Qualitative Analysis

Fine-tuning on CSQ significantly improves the model's ability to generate **grade-appropriate reasoning**. 

- **Relevance & Completeness:** Fine-tuned models score higher in human evaluations (Relevance: 4.50 vs 4.10 for Yi1.5-9B).
- **Motivation/Adaptability:** The generated thoughts align better with the cognitive level of primary school students, avoiding overly complex jargon that was present in the zero-shot outputs.

---

## 📜 Citation

If you find this dataset or work useful, please cite our paper:

```bibtex
@article{CSQ2025,
  title={A Chinese Elementary Science Question Dataset in Problem-Solving Process Generation},
  author={Liu, Zhi and Li, Dong and Long, Taotao and Wen, Chaodong and Peng, Xian and Guo, Jiaxin},
  journal={Scientific Data},
  year={2025},
  publisher={Nature Publishing Group},
  doi={10.57760/sciencedb.22816}
}
```

## 🤝 Acknowledgements

This work was supported by the **National Natural Science Foundation of China** (Grant Nos. 62377016, 61937001, 62307017, 62293550, 62293555), the **AI + Examination and Evaluation Special Teaching Reform Project** of Central China Normal University, and the **Fundamental Research Funds for the Central Universities**. 

We would like to thank all the doctoral and graduate students from the Faculty of Artificial Intelligence in Education for their contributions to data collection and annotation.

## 📄 License

The CSQ dataset is released under the [**Creative Commons Attribution 4.0 International (CC BY SA 4.0)**](https://creativecommons.org/licenses/by-sa/4.0/) License. You are free to share and adapt the material for any purpose, even commercially, as long as you give appropriate credit.

```

```
