# --------------------------------------------------
# 文件名: prepare_dataset
# 创建时间: 2024/1/30 0:07
# 描述:
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
from sklearn.model_selection import train_test_split

# 加载数据
data = pd.read_csv("YearPredictionMSD.txt", header=None)

# 提取出训练集部分
train_data = data[:463715]

# 在训练集中提取出特征和标签
X_train = train_data.iloc[:, 1:]
y_train = train_data.iloc[:, 0]

# 在训练集中再划分出验证集
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

# 提取出原始数据集中的测试集部分
test_data = data[463715:]

# 在测试集中提取出特征和标签
X_test = test_data.iloc[:, 1:]
y_test = test_data.iloc[:, 0]

# 输出为pkl文件
X_train.to_pickle("train.pkl")
X_val.to_pickle("valid.pkl")
X_test.to_pickle("test.pkl")