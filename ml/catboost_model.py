# --------------------------------------------------
# 文件名: catboost_model
# 创建时间: 2024/1/29 16:06
# 描述:
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
from catboost import CatBoostRegressor
from sklearn.metrics import mean_squared_error as mse
from sklearn.model_selection import train_test_split


ni_data_set_path = './dataset/ni_ml_dataset.csv'
ni_df = pd.read_csv(ni_data_set_path)
print(ni_df.columns)

y = ni_df.avg_lat
col = [e for e in ni_df.columns if e != 'avg_lat']
X = ni_df[col]

# 切分数据集为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建CatBoost回归模型, epochs只设置了50轮为了快速示范, 在实际问题中可能需要更多轮数
model = CatBoostRegressor(loss_function='RMSE', iterations=50)

# 训练模型, 你可能希望在这步设置更多参数, 例如学习率，深度等
model.fit(X_train, y_train, verbose=False)

# 进行预测
predictions = model.predict(X_test)

# 计算MSE
print("MSE: ", mse(y_test, predictions))
