# --------------------------------------------------
# 文件名: GBDT_model
# 创建时间: 2024/1/29 18:48
# 描述:
# 作者: WangYuanbo
# --------------------------------------------------
import pandas as pd
from sklearn.ensemble import  GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer

ni_data_set_path = './dataset/ni_ml_dataset.csv'
ni_df = pd.read_csv(ni_data_set_path)
print(ni_df.columns)

y = ni_df.avg_lat
col = [e for e in ni_df.columns if e != 'avg_lat']
X = ni_df[col]

# 分割训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 初始化GBDT模型
gbdt_model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42)

# 训练模型
gbdt_model.fit(X_train, y_train)

# 使用模型预测
predictions = gbdt_model.predict(X_test)