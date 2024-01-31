# --------------------------------------------------
# 文件名: process_dc_log
# 创建时间: 2024/1/31 16:22
# 描述: 从dc的log里面获得时间戳和延迟的信息
#      功能就是从3个csv里面获得数据集
# 作者: WangYuanbo
# --------------------------------------------------
import os
import re

import numpy as np
import pandas as pd


def calculate_moving_average(values, window):
    """计算滑动平均。"""
    weights = np.repeat(1.0, window) / window
    smas = np.convolve(values, weights, 'valid')
    return smas


# 把原始的dclog写入到csv文件中
def write_raw_dc_log_to_csv(raw_log_path, new_log_path):
    avg_lat_index = 8
    ts_index = 0
    ts_list = []
    avg_list = []
    with open(raw_log_path, 'r') as file:
        i = 0
        for line in file:
            # 跳过前m行，假设m=10
            if i < 43:
                i += 1
                continue
            # 每四行读取一次
            if i % 4 == 0:
                # 使用逗号分割每行数据
                data = line.split(',')
                # print(data)
                # 提取avg_lat的数据
                avg_lat = float(data[avg_lat_index])
                avg_list.append(avg_lat)
                timestamp = float(data[ts_index])
                ts_list.append(timestamp)
            i += 1
        log_df = pd.DataFrame({'Timestamp': ts_list, 'avg_lat': avg_list})
        log_df.to_csv(new_log_path, index=False)


# 将3个csv文件，写成原始的数据集
def merge_raw_data(raw_service_data, raw_trouble_data, new_log_data, merged_data_path):
    key = 'Timestamp'
    df1 = pd.read_csv(raw_service_data)
    df2 = pd.read_csv(raw_trouble_data)
    df3 = pd.read_csv(new_log_data)
    merged_df = df1.merge(df2, on=key, how='outer').merge(df3, on=key, how='outer')

    merged_df = merged_df.sort_values(key, ascending=True)
    # # 转换数据单位
    # toGB = 1024 ** 3
    # toMB = 1024 ** 2
    # toMb = 1000 ** 2
    # cols = merged_df.columns.tolist()
    # cols.remove('Timestamp')
    # for col in cols:
    #     merged_df[col] = merged_df[col].round(decimals=2)
    merged_df.to_csv(merged_data_path, index=False)


# 制作可以直接使用的数据集
def process_raw_data(raw_data_path, dataset_path, basic_info):
    new_df = pd.read_csv(raw_data_path)
    # 先删除latency为空值的行
    new_df = new_df.dropna(subset=['avg_lat'])
    # 进行线性插值
    new_df = new_df.interpolate(method='linear', limit_direction='both')
    # 转换数据单位
    toGB = 1024 ** 3
    toMB = 1024 ** 2
    toMb = 1000 ** 2
    toGB_list = ['mem_usage_x', 'mem_usage_y']
    toMB_list = ['disk_in_rate_x', 'disk_in_rate_y', 'disk_out_rate_x', 'disk_out_rate_y']
    toMb_list = ['net_in_rate_x', 'net_in_rate_y', 'net_out_rate_x', 'net_out_rate_y']
    for col in toGB_list:
        new_df[col] = new_df[col] / toGB
    for col in toMB_list:
        new_df[col] = new_df[col] / toMB
    for col in toMb_list:
        new_df[col] = new_df[col] / toMb

    # cols = ['cpu_usage_y', 'mem_usage_y', 'net_in_usage_y', 'net_out_usage_y', 'disk_in_rate_y', 'disk_out_rate_y']
    # for col in cols:
    #     new_df[col] =
    new_df['cpu_usage_y'] = basic_info['cpu'] - new_df['cpu_usage_y']
    new_df['mem_usage_y'] = basic_info['mem'] - new_df['mem_usage_y']
    new_df['net_in_rate_y'] = basic_info['net_in'] - new_df['net_in_rate_y']
    new_df['net_out_rate_y'] = basic_info['net_out'] - new_df['net_out_rate_y']
    new_df['disk_in_rate_y'] = basic_info['disk_in'] - new_df['disk_in_rate_y']
    new_df['disk_out_rate_y'] = basic_info['disk_out'] - new_df['disk_out_rate_y']

    t_solo = basic_info['latency']
    new_df['avg_lat'] = new_df['avg_lat'].apply(lambda x: 1 if x < t_solo else np.exp(-(x - t_solo) / t_solo))

    cols = new_df.columns.tolist()
    cols.remove('Timestamp')
    cols.remove('avg_lat')
    for col in cols:
        new_df[col] = new_df[col].round(decimals=2)

    # 删除时间戳这一列
    new_df = new_df.drop('Timestamp', axis=1)
    new_df.to_csv(dataset_path, index=False)


# 从父目录和干扰名直接获得所有数据
def get_all(father_dir, trouble_name):
    new_dir = os.path.join(father_dir, 'processed_file')
    if not os.path.exists(new_dir):
        os.mkdir(new_dir)
    # 先获得3个原始数据路径
    service_name = "memcache"
    raw_service_data_path = os.path.join(father_dir, service_name + '.data.csv')
    raw_trouble_data_path = os.path.join(father_dir, trouble_name + '.data.csv')
    raw_log_path = os.path.join(father_dir, service_name + '.log')
    # 设置从原始log文件获得的ts-latency数据文件路径
    new_service_log_data = os.path.join(new_dir, service_name + '.log.csv')
    # 写入ts-latency数据文件文件
    write_raw_dc_log_to_csv(raw_log_path, new_service_log_data)

    # 写入三个表合并的文件
    new_merged_data_path = os.path.join(
        new_dir, service_name + '.' + trouble_name + '.merged.data.csv')

    merge_raw_data(raw_service_data=raw_service_data_path,
                   raw_trouble_data=raw_trouble_data_path,
                   new_log_data=new_service_log_data,
                   merged_data_path=new_merged_data_path)
    basic_info = {
        'cpu': 56,
        'mem': 256,
        'net_in': 1000,
        'net_out': 1000,
        'disk_in': 200,
        'disk_out': 200,
        'latency': 0.5,
    }
    dataset_path = os.path.join(new_dir, service_name + '.' + trouble_name + '.dataset.csv')
    process_raw_data(raw_data_path=new_merged_data_path,
                     dataset_path=dataset_path,
                     basic_info=basic_info)

# 获得文件夹名字的前缀,也就是trouble_name
def get_letters(s):
    match = re.match(r'([a-z]*)', s)
    return match.group(0) if match else ''

if __name__ == '__main__':
    # 获得当前工作目录
    current_dir = os.getcwd()

    # 获得所有子目录和文件
    all_files_and_dirs = os.listdir(current_dir)

    # 过滤出所有的子目录
    sub_dirs = [d for d in all_files_and_dirs if os.path.isdir(os.path.join(current_dir, d))]

    sub_dirs = [x for x in sub_dirs if not x.startswith('solo')]
    for sub_dir in sub_dirs:
        get_all(father_dir=sub_dir,trouble_name=get_letters(sub_dir))

    # print(sub_dirs)
    # get_all(father_dir='cpu20240130_0925',trouble_name='cpu')
