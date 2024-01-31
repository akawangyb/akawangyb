# --------------------------------------------------
# 文件名: process_ml_dataset
# 创建时间: 2024/1/31 22:22
# 描述: 合并得到最后数据集
# 作者: WangYuanbo
# --------------------------------------------------
import os

import pandas as pd

# 获得当前工作目录
current_dir = os.getcwd()

# 获得所有子目录和文件
all_files_and_dirs = os.listdir(current_dir)

# 过滤出所有的文件
sub_dirs = [d for d in all_files_and_dirs if not os.path.isdir(os.path.join(current_dir, d))]

# 排除自己
src_name = os.path.basename(__file__)
sub_dirs.remove(src_name)

# 读取所有的csv
csv_list = [pd.read_csv(x) for x in sub_dirs]

# 使用concat函数将数据框列表连接成一个数据框
df_combined = pd.concat(csv_list, ignore_index=True)

# 将连接后的数据框保存为新的CSV文件
df_combined.to_csv("dataset.csv", index=False)


