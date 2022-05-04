
import torch
import torch.nn as nn


class Net(nn.Module):
    '''
    NeuralCDM
    '''
    # 初始化操作
    def __init__(self, student_n, exer_n, knowledge_n):
        super(Net, self).__init__()
        self.knowledge_dim = knowledge_n
        self.exer_n = exer_n
        self.emb_num = student_n
        self.stu_dim = self.knowledge_dim
        self.prednet_input_len = self.knowledge_dim

        self.prednet_len1, self.prednet_len2 = 512, 256 # changeable


        self.student_emb = nn.Embedding(self.emb_num, self.stu_dim)
        self.k_difficulty = nn.Embedding(self.exer_n, self.knowledge_dim)
        self.e_discrimination = nn.Embedding(self.exer_n, 1)


        self.prednet_full1 = nn.Linear(self.prednet_input_len, self.prednet_len1)
        self.drop_1 = nn.Dropout(p=0.5)

        self.prednet_full2 = nn.Linear(self.prednet_len1, self.prednet_len2)
        self.drop_2 = nn.Dropout(p=0.5)
        self.prednet_full3 = nn.Linear(self.prednet_len2, 1)


        # named_parameters() : 给出了网络的名称和参数的迭代器 named_parameters()将会打印每一次迭代元素的名字和param
        # 每一轮 for 循环，param 中的参数都会被改变
        for name, param in self.named_parameters():
            if 'weight' in name:
                # xavier_normal_ 初始化权重：xavier高斯初始化，参数由0均值，标准差为sqrt(2 / (fan_in + fan_out))的正态分布产生
                nn.init.xavier_normal_(param)

    # 在 train.py 中使用
    def forward(self, stu_id, exer_id, kn_emb):

        stu_emb = torch.sigmoid(self.student_emb(stu_id))
        k_difficulty = torch.sigmoid(self.k_difficulty(exer_id))
        e_discrimination = torch.sigmoid(self.e_discrimination(exer_id)) * 10

        input_x = e_discrimination * (stu_emb - k_difficulty) * kn_emb

        input_x = self.prednet_full1(input_x)
        input_x = torch.sigmoid(input_x)
        input_x = self.drop_1(input_x)

        input_x = self.prednet_full2(input_x)
        input_x = torch.sigmoid(input_x)
        input_x = self.drop_2(input_x)

        input_x = self.prednet_full3(input_x)

        output = torch.sigmoid(input_x)

        return output

    # 在 train.py 中使用
    # 用来更新权重值
    def apply_clipper(self):
        clipper = NoneNegClipper()
        self.prednet_full1.apply(clipper)    # 使用apply()函数，就可以分别对conv层和bn层或者全链接层进行参数的初始化。
        self.prednet_full2.apply(clipper)
        self.prednet_full3.apply(clipper)

    # 在 predict.py 中调用
    def get_knowledge_status(self, stu_id):
        stat_emb = torch.sigmoid(self.student_emb(stu_id))
        return stat_emb.data

    # 在 predict.py 中调用
    def get_exer_params(self, exer_id):
        k_difficulty = torch.sigmoid(self.k_difficulty(exer_id))
        e_discrimination = torch.sigmoid(self.e_discrimination(exer_id)) * 10
        return k_difficulty.data, e_discrimination.data


class NoneNegClipper(object):
    def __init__(self):
        super(NoneNegClipper, self).__init__()

    def __call__(self, module):
        if hasattr(module, 'weight'):   # hasattr() 函数用于判断对象是否包含对应的属性。 hasattr(object, name)
            # 初始化权重
            w = module.weight.data   # 权重
            a = torch.relu(torch.neg(w))  # relu 函数  torch.neg 取负值
            w.add_(a)   # 使 w 全部为正，满足单调性假设

