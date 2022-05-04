import numpy as np

# 将0, 1计分转化为多级积分
def OneToMuti(scores):
    max_score = int(np.max(scores))
    min_score = int(np.min(scores))
    len = max_score - min_score + 1  # 4 - 0 + 1 = 5 五种情况：0，1，2，3，4
    scores_result = {}
    for i in range(scores.shape[1]):  # 一列
        temp_scores = np.zeros((scores.shape[0], len))
        for j in range(len):  # (0, 4)
            temp_scores[:, j][scores[:, i] == min_score + j] = 1
        scores_result[i] = temp_scores
    print(scores_result)


# 试题最大反应计算
f= open('1.txt')
scores = np.loadtxt(f, delimiter=',')
OneToMuti(scores)

'''
4,4,3,2
3,3,3,0
3,0,2,3
3,2,2,3
3,4,4,1
'''

'''
[[0. 0. 0. 0. 1.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]]
[[0. 0. 0. 0. 1.]
 [0. 0. 0. 1. 0.]
 [1. 0. 0. 0. 0.]
 [0. 0. 1. 0. 0.]
 [0. 0. 0. 0. 1.]]
[[0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 1. 0. 0.]
 [0. 0. 1. 0. 0.]
 [0. 0. 0. 0. 1.]]
[[0. 0. 1. 0. 0.]
 [1. 0. 0. 0. 0.]
 [0. 0. 0. 1. 0.]
 [0. 0. 0. 1. 0.]
 [0. 1. 0. 0. 0.]]
'''

