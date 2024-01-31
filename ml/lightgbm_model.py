# --------------------------------------------------
# 文件名: lightgb,_model
# 创建时间: 2024/1/29 15:42
# 描述:
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn import datasets
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

ni_data_set_path = './dataset/ni_ml_dataset.csv'
ni_df = pd.read_csv(ni_data_set_path)
print(ni_df.columns)

y = ni_df.avg_lat
col = [e for e in ni_df.columns if e != 'avg_lat']
X = ni_df[col]

# 划分训练集和测试集：
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=42)

#
# 实例化一个LightGBM分类器模型:
model = LGBMClassifier(n_estimators=100)

# 对模型进行训练
model.fit(X_train, X_test)

# 进行预测
y_predict = model.predict(X_test)

# 计算预测结果和真实值之间的均方误差（MSE）
mse = mean_squared_error(y_test, y_predict)
print("MSE: %f" % (mse))