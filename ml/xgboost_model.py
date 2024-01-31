# --------------------------------------------------
# 文件名: xgboost
# 创建时间: 2024/1/29 15:31
# 描述:
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
from lightgbm import LGBMRegressor
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split

import xgboost as xgb

ni_data_set_path = './dataset/ni_ml_dataset.csv'
ni_df = pd.read_csv(ni_data_set_path)
print(ni_df.columns)

y = ni_df.avg_lat
col = [e for e in ni_df.columns if e != 'avg_lat']
X = ni_df[col]

## 将数据分为训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 实例化一个LightGBM回归模型
model = LGBMRegressor(n_estimators=100)

# 训练模型
model.fit(X_train, y_train)

# 使用模型进行预测
y_pred = model.predict(X_test)

# 计算均方误差
mse = mean_squared_error(y_test, y_pred)
print("MSE: ", mse)

