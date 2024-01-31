# --------------------------------------------------
# 文件名: data_utils
# 创建时间: 2024/1/30 9:56
# 描述: 处理year数据
# 作者: WangYuanbo
# --------------------------------------------------
import os

import pandas as pd
from sklearn.model_selection import train_test_split

# 加载数据
data = pd.read_csv("yearpredictionmsd/YearPredictionMSD.txt", header=None)

# 提取出训练集部分
train_data = data[:463715]

# # 在训练集中提取出特征和标签
# X_train = train_data.iloc[:, 1:]
# y_train = train_data.iloc[:, 0]

# 在训练集中再划分出验证集
train_set, val_set = train_test_split(train_data, test_size=0.2, random_state=42)

# 提取出原始数据集中的测试集部分
test_set = data[463715:]

# # 在测试集中提取出特征和标签
# X_test = test_data.iloc[:, 1:]
# y_test = test_data.iloc[:, 0]

father_dir = 'yearpred'
if not os.path.exists(father_dir):
    os.makedirs(father_dir)

# 输出为pkl文件
# data.to_pickle(os.path.join(father_dir, "YearPrediction.pkl"))

train_set.to_csv(os.path.join(father_dir, "train.csv"), index=False)
val_set.to_csv(os.path.join(father_dir, "valid.csv"), index=False)
test_set.to_csv(os.path.join(father_dir, "test.csv"), index=False)
