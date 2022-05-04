import json
import random
from tqdm import tqdm
import numpy as np

scores = np.loadtxt('../dataset/Math1/data.txt', delimiter='\t')  # 4209 x 20 原始数据，相当于标签
q_matrix = np.loadtxt('../dataset/Math1/q.txt', delimiter='\t')  # 20 x 11


train_set = []
for i in tqdm(range(scores.shape[0])):
    for j in range(scores.shape[1]):
        user_id = i
        exer_id = j
        if scores[i][j] > 0.5:
            score = 1.0
        else:
            score = 0.0


        log = []
        for k in range(q_matrix.shape[1]):
            if(q_matrix[j][k]) == 1:
                log.append(k)
        knowledge_code = log

        train_set.append({'user_id': user_id, 'exer_id': exer_id, 'score': score, 'knowledge_code': knowledge_code})
random.shuffle(train_set)

with open('train_set.json', 'w', encoding='utf8') as output_file: json.dump(train_set, output_file, indent=4, ensure_ascii=False)




# 这是总的数据集，按照表格的顺序逐个提取出来的
log_data = []
for i in tqdm(range(scores.shape[0])):
    user_id = i
    log_num = scores.shape[1]
    logs = []
    for j in range(log_num):
        exer_id = j

        if scores[i][j] > 0.5:
            score = 1.0
        else:
            score = 0.0

        knowledge_code = []
        for n in range(q_matrix.shape[1]):
            if (q_matrix[j][n]) == 1:
                knowledge_code.append(n)
        logs.append({'exer_id': exer_id, 'score': score, 'knowledge_code': knowledge_code})

    log_data.append({'user_id': user_id, 'log_num': log_num, 'logs': logs})

print("正在写入文件......")
with open('log_data.json', 'w', encoding='utf8') as output_file: json.dump(log_data, output_file, indent=4, ensure_ascii=False)











