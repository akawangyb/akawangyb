import time
from datetime import datetime

import pandas as pd
from prometheus_api_client import PrometheusConnect

url = "http://localhost:9090"


def query_and_write_csv(container_name, nic_ID, start_time, end_time, output_path):
    # 设置数据库参数

    prom = PrometheusConnect(url=url, disable_ssl=True)
    # 设置查询指标
    cpu_usage = 'sum(irate(container_cpu_usage_seconds_total{{name="{}"}}[30s]))'.format(container_name)
    mem_usage = 'container_memory_usage_bytes{{name="{}"}}'.format(container_name)
    netin_rate = 'irate(container_network_receive_bytes_total{{name="{}", interface="{}"}}[30s])'.format(
        container_name, nic_ID)
    netout_rate = 'irate(container_network_transmit_bytes_total{{name="{}", interface="{}"}}[30s])'.format(
        container_name, nic_ID)
    diskin_rate = 'irate(container_fs_writes_bytes_total{{name="{}"}}[30s])'.format(container_name)
    diskout_rate = 'irate(container_fs_reads_bytes_total{{name="{}"}}[30s])'.format(container_name)

    metric_list = [cpu_usage, mem_usage, netin_rate, netout_rate, diskin_rate, diskout_rate]

    raw_data = []
    for e in metric_list:
        raw_data.append(prom.custom_query_range(
            query=e,
            start_time=start_time,
            end_time=end_time,
            step='5s'
        ))
        # print(raw_data[-1])
        if len(raw_data[-1]) == 0:
            raw_data.pop()
    # print(raw_data)
    raw_data = [e[0]['values'] for e in raw_data]

    df_list = [pd.DataFrame(lst, columns=['timestamp', 'value' + str(i + 1)]) for i, lst in enumerate(raw_data)]

    from functools import reduce

    df_final = reduce(lambda left, right: pd.merge(left, right, on='timestamp'), df_list)
    # print(df_final)
    # print(len(raw_data))
    # print(raw_data)
    if len(raw_data) == 6:
        df_final.columns = ["Timestamp", "cpu_usage", "mem_usage", "net_in_rate", "net_out_rate", "disk_in_rate",
                            "disk_out_rate"]
    else:
        df_final.columns = ["Timestamp", "cpu_usage", "mem_usage", "net_in_rate", "net_out_rate"]
        df_final["disk_in_rate"] = 0
        df_final["disk_out_rate"] = 0
    df_final.to_csv('{}'.format(output_path), index=False, line_terminator='\n')
    # print("数据已存入{}中.".format(output_path))


def query_and_write_csv_by_service(service_name, nic_ID, start_time, end_time, output_path):
    # 设置数据库参数

    prom = PrometheusConnect(url=url, disable_ssl=True)
    # 设置查询指标
    cpu_usage = 'sum(irate(container_cpu_usage_seconds_total{{container_label_com_docker_swarm_service_name="{}"}}[30s]))'.format(
        service_name)
    mem_usage = 'container_memory_usage_bytes{{container_label_com_docker_swarm_service_name="{}"}}'.format(
        service_name)
    netin_rate = 'irate(container_network_receive_bytes_total{{container_label_com_docker_swarm_service_name="{}", interface="{}"}}[30s])'.format(
        service_name, nic_ID)
    netout_rate = 'irate(container_network_transmit_bytes_total{{container_label_com_docker_swarm_service_name="{}", interface="{}"}}[30s])'.format(
        service_name, nic_ID)
    diskin_rate = 'irate(container_fs_writes_bytes_total{{container_label_com_docker_swarm_service_name="{}"}}[30s])'.format(
        service_name)
    diskout_rate = 'irate(container_fs_reads_bytes_total{{container_label_com_docker_swarm_service_name="{}"}}[30s])'.format(
        service_name)

    # metric_list = [cpu_usage, mem_usage, netin_rate, netout_rate, diskin_rate, diskout_rate]
    metric_list = [cpu_usage, mem_usage, netin_rate, netout_rate]
    if service_name != "dc-server":
        metric_list.append(diskin_rate)
        metric_list.append(diskout_rate)

    raw_data = []

    for e in metric_list:
        raw_data.append(prom.custom_query_range(
            query=e,
            start_time=start_time,
            end_time=end_time,
            step='5s'
        ))
        # print(raw_data[-1])

    # print(len(raw_data))

    raw_data = [e[0]['values'] for e in raw_data]
    # print(raw_data)
    # 将所有列表转换为数据框，并存储在一个新的列表中
    df_list = [pd.DataFrame(lst, columns=['timestamp', 'value' + str(i + 1)]) for i, lst in enumerate(raw_data)]

    from functools import reduce

    df_final = reduce(lambda left, right: pd.merge(left, right, on='timestamp'), df_list)
    if service_name == "dc-server":
        df_final['a'] = 0
        df_final['b'] = 0
    columns = ["Timestamp", "cpu_usage", "mem_usage", "net_in_rate", "net_out_rate", "disk_in_rate", "disk_out_rate"]
    df_final.columns = columns
    df_final.to_csv('{}'.format(output_path), index=False, line_terminator='\n')
    # print("数据已存入{}中.".format(output_path))


def run_process(cmd, filename):
    with open(filename, 'w') as f:
        import subprocess
        result = subprocess.Popen(cmd, shell=True, stdout=f)
        result.communicate()


def get_log_paths(father_dir, service_name, trouble_name, src_name):
    import os
    service_log_path = os.path.join(father_dir, service_name + ".log")
    service_data_path = os.path.join(father_dir, service_name + ".data.csv")

    trouble_log_path = os.path.join(father_dir, trouble_name + ".log")
    trouble_data_path = os.path.join(father_dir, trouble_name + ".data.csv")

    src_log_path = os.path.join(father_dir, src_name + ".log")

    return service_log_path, service_data_path, trouble_log_path, trouble_data_path, src_log_path


def log_start_time(start_time, src_name, father_dir):
    log_list = ["RUN: {}".format(src_name), "Start time：{}".format(start_time),
                "ALL will begin, your logs will be writen in {} !!!".format(father_dir)]
    return log_list


def log_end_time(start_time, end_time, father_dir):
    time_consumption = end_time - start_time
    # end_time = start_time + time_consumption
    log_list = ["ALL is finished, check your logs in {} !!!".format(father_dir),
                "Time consumption is: {}".format(time_consumption), "End time: {}".format(end_time)]
    return log_list


if __name__ == '__main__':
    print("hello")
    # 测试一下函数是否工作正常
    # end_time = datetime.fromtimestamp(time.time())
    # start_time = end_time - timedelta(seconds=60)
    #
    # query_and_write_csv(
    #     container_name="fiotest",
    #     nic_ID="eth0",
    #     start_time=start_time,
    #     end_time=end_time,
    #     output_path="./tmp.csv"
    # )
