# --------------------------------------------------
# 文件名: linear_regression
# 创建时间: 2024/1/29 15:20
# 描述: 利用线性模型预测性能下降因子
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

ni_data_set_path = './dataset/ni_ml_dataset.csv'
ni_df = pd.read_csv(ni_data_set_path)
print(ni_df.columns)

y = ni_df.avg_lat
col = [e for e in ni_df.columns if e != 'avg_lat']
X = ni_df[col]

# 首先，我们需要将数据集分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建一个线性回归模型
model = LinearRegression()

# 使用训练数据来训练模型
model.fit(X_train, y_train)

# 对测试集进行预测
predictions = model.predict(X_test)

# 计算预测结果和真实值之间的均方误差（MSE）
mse = mean_squared_error(y_test, predictions)

print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
