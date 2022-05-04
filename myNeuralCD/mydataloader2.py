import json

import torch


class TrainDataLoader(object):
    '''
    data loader for training
    '''

    def __init__(self):
        self.batch_size = 8
        self.ptr = 0
        self.data = []

        data_file = './data/train_set.json'
        config_file = './data/config.txt'  # Number of Students, Number of Exercises, Number of Knowledge Concepts
        with open(data_file, encoding='utf8') as i_f:  # 打开 Json 文件
            self.data = json.load(i_f)  # 读取 json 文件
        with open(config_file) as i_f:  # 打开配置文件
            i_f.readline()  # 读取配置文件
            _, _, knowledge_n = i_f.readline().split(',')  # 获取知识点的数量
        self.knowledge_dim = int(knowledge_n)  # knowledge_dim : 知识点的数量

    def next_batch(self):
        # 每次对32个log进行处理
        if self.is_end():
            return None, None, None, None
        # 学号、考试题目、知识点、label 标签
        input_stu_ids, input_exer_ids, input_knowedge_embs, ys = [], [], [], []

        # count： 0~31
        for count in range(self.batch_size):
            log = self.data[self.ptr + count]
            # knowledge_emb ：一个长度为123的列表，数字全为0
            knowledge_emb = [0.] * self.knowledge_dim  # 知识点的维度 * 0;
            for knowledge_code in log['knowledge_code']:
                # 将具体考察的知识点 变为 1，one-hot 向量
                knowledge_emb[knowledge_code] = 1.0
            # 将一个batch(32个)的具体的学生号提取出来加入到列表中
            input_stu_ids.append(log['user_id'])  # 提取出学生号
            input_exer_ids.append(log['exer_id'])  # 提取出试题号
            input_knowedge_embs.append(knowledge_emb)  # 提取出考察了哪一道知识点（相当于 Q矩阵 ）
            # ys是label， 也就是数据集中的score，作答的情况，做对了为1，做错了为0，每一次得到长度为32的向量
            y = log['score']
            ys.append(y)

        # 第一次0~31，第二次32~63.....
        self.ptr += self.batch_size
        return torch.LongTensor(input_stu_ids), torch.LongTensor(input_exer_ids), torch.Tensor(
            input_knowedge_embs), torch.LongTensor(ys)

    # 判断是否训练完所有数据
    def is_end(self):
        if self.ptr + self.batch_size > len(self.data):
            return True
        else:
            return False

    def reset(self):
        self.ptr = 0


# 验证集和测试集
class ValTestDataLoader(object):
    def __init__(self, d_type='validation'):
        self.ptr = 0
        self.data = []
        self.d_type = d_type

        if d_type == 'validation':
            data_file = './data/val_set.json'
        else:
            data_file = './data/test_set.json'
        config_file = './data/config.txt'
        with open(data_file, encoding='utf8') as i_f:
            self.data = json.load(i_f)
        with open(config_file) as i_f:
            i_f.readline()
            _, _, knowledge_n = i_f.readline().split(',')
            self.knowledge_dim = int(knowledge_n)

    def next_batch(self):
        if self.is_end():
            return None, None, None, None
        logs = self.data[self.ptr]['logs']
        user_id = self.data[self.ptr]['user_id']
        input_stu_ids, input_exer_ids, input_knowledge_embs, ys = [], [], [], []
        for log in logs:
            input_stu_ids.append(user_id)
            input_exer_ids.append(log['exer_id'])
            knowledge_emb = [0.] * self.knowledge_dim
            for knowledge_code in log['knowledge_code']:
                knowledge_emb[knowledge_code] = 1.0
            input_knowledge_embs.append(knowledge_emb)
            y = log['score']
            ys.append(y)
        self.ptr += 1
        return torch.LongTensor(input_stu_ids), torch.LongTensor(input_exer_ids), torch.Tensor(
            input_knowledge_embs), torch.LongTensor(ys)

    def is_end(self):
        if self.ptr >= len(self.data):
            return True
        else:
            return False

    def reset(self):
        self.ptr = 0
