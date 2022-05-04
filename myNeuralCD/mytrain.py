
import numpy as np
import torch
import torch.nn as nn
from sklearn.metrics import roc_auc_score

from mymodel import Net
import torch.optim as optim
from mydataloader import TrainDataLoader
from mydataloader import ValTestDataLoader

student_n = 4209  # 考生人数
exer_n = 20  # 试题数量
knowledge_n = 11  # 知识点数量

batch_size = 8
epoch_n = 10
device = torch.device('cuda:0')

score = np.loadtxt('../dataset/Math1/data.txt', delimiter='\t')   # 4209 x 20 原始数据，相当于标签
# print(score)

q_matrix = np.loadtxt('../dataset/Math1/q.txt', delimiter='\t')  # 20 x 11
# print(q_matrix)


# 训练集
def train():
    # 加载数据, 返回的数据有：1、学生学号编号、2、考试题目编号、3、知识点编号、4、label 标签（得分）
    data_loader = TrainDataLoader()

    # 神经网络，传入参数取训练 1、学生学号编号、2、考试题目编号、3、知识点编号
    # 输出一些网络参数
    net = Net(student_n, exer_n, knowledge_n)

    net = net.to(device)  # 运用 GPU

    # 优化器
    optimizer = optim.Adam(net.parameters(), lr=0.002)   # 学习率是0.002
    print('training model...')

    # 损失函数
    loss_function = nn.NLLLoss()

    for epoch in range(epoch_n):
        data_loader.reset()
        running_loss = 0.0
        batch_count = 0
        while not data_loader.is_end():
            batch_count += 1
            # 每次都是从train_set 拿出batch_size个log 进行数据的处理和运算
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels = data_loader.next_batch()
            input_stu_ids, input_exer_ids, input_knowledge_embs, labels = \
                input_stu_ids.to(device), input_exer_ids.to(device), input_knowledge_embs.to(device), labels.to(device)

            # optimizer.zero_grad()意思是把梯度置零，也就是把loss关于weight的导数变成0
            optimizer.zero_grad()

            # input_knowledge_embs 是Q矩阵
            output_1 = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)  # batch_size x 1
            output_0 = torch.ones(output_1.size()).to(device) - output_1  # batch_size x 1    # 1 - output1
            output = torch.cat((output_0, output_1), 1)  # batch_size x 2  (output_0, output_1) 其中 output_0 + output_1 = 1

            # grad_penalty = 0
            # torch.log 以 e 为底的对数
            # 损失函数
            loss = loss_function(torch.log(output), labels)
            # 反向传播计算得到每个参数的梯度值
            loss.backward()
            # 最后通过梯度下降执行一步参数更新，optimizer只负责通过梯度下降进行优化，而不负责产生梯度，梯度是tensor.backward()方法产生的。
            optimizer.step()

            # 在一批之后对权重进行初始化操作
            net.apply_clipper()

            running_loss += loss.item()

            if batch_count % 100 == 99:   # 每两百次输出结果
                print('[%d, %5d] loss: %.3f' % (epoch + 1, batch_count + 1, running_loss / 200))
                running_loss = 0.0

        # validate and save current model every epoch
        # 验证
        rmse, auc = validate(net, epoch)
        save_snapshot(net, './model/model_epoch' + str(epoch + 1))  # 保存模型


# 保存文件
def save_snapshot(model, filename):
    f = open(filename, 'wb')
    torch.save(model.state_dict(), f)
    f.close()


# 验证集
def validate(model, epoch):
    data_loader = ValTestDataLoader('validation')  # 加载验证集
    net = Net(student_n, exer_n, knowledge_n)
    print('validating model...')
    data_loader.reset()
    # load model parameters
    net.load_state_dict(model.state_dict())
    net = net.to(device)
    net.eval()

    correct_count, exer_count = 0, 0
    batch_count, batch_avg_loss = 0, 0.0
    pred_all, label_all = [], []
    while not data_loader.is_end():
        batch_count += 1
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels = data_loader.next_batch()
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels = input_stu_ids.to(device), input_exer_ids.to(
            device), input_knowledge_embs.to(device), labels.to(device)

        # print(input_stu_ids, input_exer_ids, input_knowledge_embs, labels)


        output = net.forward(input_stu_ids, input_exer_ids, input_knowledge_embs)



        output = output.view(-1)   # 将output里面的所有维度数据转化成一维的，并且按先后顺序排列。
        # compute accuracy
        for i in range(len(labels)):
            if (labels[i] == 1 and output[i] > 0.5) or (labels[i] == 0 and output[i] < 0.5):
                correct_count += 1
        exer_count += len(labels)
        pred_all += output.to(torch.device('cpu')).tolist()
        label_all += labels.to(torch.device('cpu')).tolist()

    pred_all = np.array(pred_all)
    label_all = np.array(label_all)
    # compute accuracy
    accuracy = correct_count / exer_count
    # compute RMSE
    rmse = np.sqrt(np.mean((label_all - pred_all) ** 2))
    # compute AUC
    auc = roc_auc_score(label_all, pred_all)
    print('epoch= %d, accuracy= %f, rmse= %f, auc= %f' % (epoch+1, accuracy, rmse, auc))
    with open('./result/model_val.txt', 'a', encoding='utf8') as f:
        f.write('epoch= %d, accuracy= %f, rmse= %f, auc= %f\n' % (epoch+1, accuracy, rmse, auc))

    return rmse, auc



if __name__ == '__main__':
    with open('./data/config.txt') as i_f:
        i_f.readline()
        student_n, exer_n, knowledge_n = list(map(eval, i_f.readline().split(',')))

    train()