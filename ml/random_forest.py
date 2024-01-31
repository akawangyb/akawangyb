# --------------------------------------------------
# 文件名: random_forest
# 创建时间: 2024/1/29 15:22
# 描述: 随机森林模型预测性能下降因子
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
# 导入所需的模块
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

ni_data_set_path = './dataset/ni_ml_dataset.csv'
ni_df = pd.read_csv(ni_data_set_path)
print(ni_df.columns)

y = ni_df.avg_lat
col = [e for e in ni_df.columns if e != 'avg_lat']
X = ni_df[col]
# 假设我们有一些输入特征存在 `X` 中，相应的目标值存在 `y` 中
# 首先，将数据集分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建随机森林模型
rf = RandomForestRegressor(n_estimators=200, max_depth=3, random_state=42)

# 使用训练数据训练模型
rf.fit(X_train, y_train)

# 对测试集进行预测
predictions = rf.predict(X_test)

# 计算预测结果和真实值之间的均方误差（MSE）
mse = mean_squared_error(y_test, predictions)

print('The Mean Squared Error of our forecasts is {}'.format(round(mse, 2)))
