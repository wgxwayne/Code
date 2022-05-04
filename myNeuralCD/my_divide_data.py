import json
import random

from tqdm import tqdm

# min_log = 15  # 至少要做15道题目，该被试才能被统计上


def divide_data():
    '''
    1. delete students who have fewer than min_log response logs
    2. divide dataset into train_set, val_set and test_set (0.7:0.1:0.2) 将数据集分为训练集，验证集和测试集
    :return:
    '''
    with open('data/log_data.json', encoding='utf8') as i_f:
        stus = json.load(i_f)

    # 1. delete students who have fewer than min_log response logs
    # 删除少于最少答题数 (log_num) 的学生

    # stu_i = 0
    # while stu_i < len(stus):
    #     if stus[stu_i]['log_num'] < min_log:
    #         del stus[stu_i]   # 删除
    #         stu_i -= 1
    #     stu_i += 1


    # 2. divide dataset into train_set, val_set and test_set
    # 将 数据集划分为 训练集，验证集和测试集
    train_slice, train_set, val_set, test_set = [], [], [], []
    for stu in tqdm(stus):  # for 循环遍历每一个学生
        user_id = stu['user_id']  # 提取出学生号

        # 字典的形式存储学生号
        # stu_train 是三元组，{学号，题目数量，每一题的答题情况}
        stu_train = {'user_id': user_id}
        stu_val = {'user_id': user_id}
        stu_test = {'user_id': user_id}

        # 将每一个学生的答题情况分为三部分，循环遍历所有学生
        train_size = int(stu['log_num'] * 0.7)  # 训练集占 70%
        val_size = int(stu['log_num'] * 0.1)  # 验证集占 10%
        test_size = stu['log_num'] - train_size - val_size  # 测试集占 20%

        logs = []  # 新建列表将所有 log 提取出来放入
        for log in stu['logs']:
            logs.append(log)
        random.shuffle(logs)  # 打乱顺序
        stu_train['log_num'] = train_size  # 每一个学生的答题数量
        stu_train['logs'] = logs[:train_size]  # 划分logs
        stu_val['log_num'] = val_size
        stu_val['logs'] = logs[train_size:train_size+val_size]
        stu_test['log_num'] = test_size
        stu_test['logs'] = logs[-test_size:]

        train_slice.append(stu_train)
        val_set.append(stu_val)
        test_set.append(stu_test)

        # shuffle logs in train_slice together, get train_set
        for log in stu_train['logs']:
            train_set.append({'user_id': user_id, 'exer_id': log['exer_id'], 'score': log['score'],
                              'knowledge_code': log['knowledge_code']})
    # 大的for循环到此为止

    random.shuffle(train_set)
    # 全部保存到文件里面
    print("正在保存......")
    with open('data/train_slice.json', 'w', encoding='utf8') as output_file:
        json.dump(train_slice, output_file, indent=4, ensure_ascii=False)
    with open('data/train_set.json', 'w', encoding='utf8') as output_file:
        json.dump(train_set, output_file, indent=4, ensure_ascii=False)
    with open('data/val_set.json', 'w', encoding='utf8') as output_file:
        json.dump(val_set, output_file, indent=4, ensure_ascii=False)    # 直接用test_set作为val_set
    with open('data/test_set.json', 'w', encoding='utf8') as output_file:
        json.dump(test_set, output_file, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    print("正在划分数据集......")
    divide_data()
    print("数据集划分保存完成......")