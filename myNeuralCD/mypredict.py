import json

import torch
import numpy as np
from sklearn.metrics import roc_auc_score
from mydataloader import ValTestDataLoader
from mymodel import Net


# can be changed according to math1_information.txt
student_n = 4209  # 考生人数
exer_n = 20  # 试题数量
knowledge_n = 11  # 知识点数量


def test(epoch):
    data_loader = ValTestDataLoader('test')
    net = Net(student_n, exer_n, knowledge_n)
    device = torch.device('cpu')
    print('testing model...')
    data_loader.reset()
    load_snapshot(net, './model/model_epoch' + str(epoch))
    net = net.to(device)
    net.eval()

    correct_count, exer_count = 0, 0
    pred_all, label_all = [], []
    while not data_loader.is_end():
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels = data_loader.next_batch()
        input_stu_ids, input_exer_ids, input_knowledge_embs, labels = input_stu_ids.to(device), input_exer_ids.to(
            device), input_knowledge_embs.to(device), labels.to(device)
        out_put = net(input_stu_ids, input_exer_ids, input_knowledge_embs)
        out_put = out_put.view(-1)
        # compute accuracy
        for i in range(len(labels)):
            if (labels[i] == 1 and out_put[i] > 0.5) or (labels[i] == 0 and out_put[i] < 0.5):
                correct_count += 1
        exer_count += len(labels)
        pred_all += out_put.tolist()
        label_all += labels.tolist()

    pred_all = np.array(pred_all)
    label_all = np.array(label_all)
    print(pred_all)
    print(len(pred_all))
    print(label_all)
    print(len(label_all))
    # print(pred_all[0:30])
    # print(label_all[0:30])
    # compute accuracy
    accuracy = correct_count / exer_count
    # compute RMSE
    rmse = np.sqrt(np.mean((label_all - pred_all) ** 2))
    # compute AUC
    auc = roc_auc_score(label_all, pred_all)
    print('epoch= %d, accuracy= %f, rmse= %f, auc= %f' % (epoch, accuracy, rmse, auc))
    with open('./result/model_test.txt', 'a', encoding='utf8') as f:
        f.write('epoch= %d, accuracy= %f, rmse= %f, auc= %f\n' % (epoch, accuracy, rmse, auc))


def load_snapshot(model, filename):
    f = open(filename, 'rb')
    model.load_state_dict(torch.load(f, map_location=lambda s, loc: s))
    f.close()


def get_status():
    '''
    学生的知识状态
    An example of getting student's knowledge status
    :return:
    '''
    net = Net(student_n, exer_n, knowledge_n)
    load_snapshot(net, './model/model_epoch5')       # load model
    net.eval()
    status = []
    # with open('./result/student_stat.txt', 'w', encoding='utf8') as output_file:
    for stu_id in range(student_n):
        # get knowledge status of student with stu_id (index)
        status.append(net.get_knowledge_status(torch.LongTensor([stu_id])).tolist()[0])
        # output_file.write(str(status) + '\n')
    with open('./result/student_stat.json', 'w', encoding='utf8') as output_file: json.dump(status,
                                                                                            output_file,
                                                                                            indent=4,
                                                                                            ensure_ascii=False)



def get_exer_params():
    '''
    知识点难度和区分度
    An example of getting exercise's parameters (knowledge difficulty and exercise discrimination)
    :return:
    '''
    net = Net(student_n, exer_n, knowledge_n)
    load_snapshot(net, 'model/model_epoch5')    # load model
    net.eval()
    exer_params_dict = {}
    for exer_id in range(exer_n):
        # get knowledge difficulty and exercise discrimination of exercise with exer_id (index)
        k_difficulty, e_discrimination = net.get_exer_params(torch.LongTensor([exer_id]))
        exer_params_dict[exer_id] = (k_difficulty.tolist()[0], e_discrimination.tolist()[0])
    # with open('./result/exer_params.txt', 'w', encoding='utf8') as o_f: o_f.write(str(exer_params_dict))
    with open('./result/exer_params.json', 'w', encoding='utf8') as output_file: json.dump(exer_params_dict, output_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    # if (len(sys.argv) != 2) or (not sys.argv[1].isdigit()):
    #     print('command:\n\tpython predict.py {epoch}\nexample:\n\tpython predict.py 70')
    #     exit(1)

    # global student_n, exer_n, knowledge_n
    with open('./data/config.txt') as i_f:
        i_f.readline()
        student_n, exer_n, knowledge_n = list(map(eval, i_f.readline().split(',')))

    # test(int(sys.argv[1]))
    test(1)
    get_status()
    get_exer_params()