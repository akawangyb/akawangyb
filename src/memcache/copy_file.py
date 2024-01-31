# --------------------------------------------------
# 文件名: copy_file
# 创建时间: 2024/1/31 22:54
# 描述: 把刚才生成的数据集拷贝到指定文件夹进一步处理
# 作者: WangYuanbo
# --------------------------------------------------
import os
import shutil

# 获得当前工作目录
current_dir = os.getcwd()

# 获得所有子目录和文件
all_files_and_dirs = os.listdir(current_dir)

# 过滤出所有的子目录,排除solo
sub_dirs = [d for d in all_files_and_dirs if os.path.isdir(os.path.join(current_dir, d))]
sub_dirs = [x for x in sub_dirs if not x.startswith('solo')]

# sub_dirs.remove()
target_dir = '../../dataset/ml_dataset'
# target_dir = '../../tmp'
for sub_dir in sub_dirs:
    father_dir = os.path.join(current_dir, sub_dir)
    son_dir = os.path.join(father_dir, "processed_file")
    for file_name in os.listdir(son_dir):
        # print(file_name)
        if file_name.endswith('.dataset.csv'):
            print(file_name)
            shutil.copy(os.path.join(son_dir, file_name), target_dir)
