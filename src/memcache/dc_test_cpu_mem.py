# --------------------------------------------------
# 文件名: dc_test_cpu_mem
# 创建时间: 2024/1/27 20:40
# 描述: ibench 测试
# 作者: WangYuanbo
# --------------------------------------------------
#  基本用法 python3 dc_test_cpu_mem.py && sleep 60 && python3 dc_test_cpu_mem.py --cpu
import argparse
import os
import sys
import threading
import time
from datetime import datetime, timedelta

import pytz

from collect_data import get_log_paths, log_start_time, run_process, log_end_time
from collect_data import query_and_write_csv_by_service, query_and_write_csv

parser = argparse.ArgumentParser()
parser.add_argument('--cpu', action='store_true', help='设置时表示测试cpu，否则测试内存')

try:
    # 解析参数
    args = parser.parse_args()
except argparse.ArgumentError as err:
    print("bug!")
    print(str(err))
    sys.exit(1)

service_name = "memcache"
trouble_name = "cpu" if args.cpu else "mem"

# 先解决日志的存放路径问题
tz = pytz.timezone('Asia/Shanghai')  # 指定时区为东八区，即上海时区
now_time = datetime.now(tz).strftime("%Y%m%d_%H%M")
father_dir = trouble_name + now_time
if not os.path.exists(father_dir):
    os.mkdir(father_dir)

src_name = sys.argv[0]
(service_log_path, service_data_path,
 trouble_log_path, trouble_data_path,
 src_log_path) = get_log_paths(
    father_dir=father_dir,
    service_name=service_name,
    trouble_name=trouble_name,
    src_name=src_name
)

# 测试脚本的记录输出
print_list = []

# 记录测试开始时间
start_time = datetime.fromtimestamp(time.time())
print_list.extend(log_start_time(
    start_time=start_time, src_name=src_name, father_dir=father_dir))

total_time = 120 * 55 if args.cpu else 18 * 120
time_interval = 1
rps = 45000
dc_client = (
    'docker exec -it dc-client timeout {} /bin/bash /entrypoint.sh --m="RPS" --S=28 --g=0.8 --c=200 --w=8 --T={} '
    '--r={}'.format(total_time, time_interval, rps))

dc_client_thread = threading.Thread(target=run_process, args=(dc_client, service_log_path))
dc_client_thread.start()

# time.sleep(60 * 3)

min_cpu = 1
cpu_step = 1
max_cpu = 55
time_spent = 120
cpu_cmd = ' cpu {} {} {} {}'.format(min_cpu, cpu_step, max_cpu, time_spent)

min_mem = 10
mem_step = 10
max_mem = 180
time_spent = 120
mem_cmd = ' memCap {} {} {} {}'.format(min_mem, mem_step, max_mem, time_spent)

ibench_cmd = 'ssh node16 docker exec ibench6 '
ibench_cmd += cpu_cmd if args.cpu else mem_cmd

ibench_thread = threading.Thread(target=run_process, args=(ibench_cmd, trouble_log_path))
ibench_thread.start()

# 等待测试完成
dc_client_thread.join()
ibench_thread.join()

# 测试完成记录结束时间
end_time = datetime.fromtimestamp(time.time())
print_list.extend(log_end_time(
    start_time=start_time,
    end_time=end_time,
    father_dir=father_dir
))

# 测试完成之后，在服务器端扒下所有的数据
# 设置服务器端的测试参数
service_name = "dc-server"
# swarm集群下网卡有变化
nic_ID = "eth1"
query_and_write_csv_by_service(
    service_name=service_name,
    nic_ID=nic_ID,
    start_time=start_time - timedelta(seconds=5),
    end_time=end_time + timedelta(seconds=5),
    output_path=service_data_path
)

# 扒下所有的cpu干扰的运行时数据
container_name = "ibench6"
query_and_write_csv(
    container_name=container_name,
    nic_ID="eth0",
    start_time=start_time - timedelta(seconds=5),
    end_time=end_time + timedelta(seconds=5),
    output_path=trouble_data_path
)

print_list.extend([
    "total_time = {}".format(total_time),
    "time_interval = {}".format(time_interval),
    "rps = {}".format(rps),
    "dc_client = {}".format(dc_client)
])
if args.cpu:
    print_list.extend([
        "min_cpu = {}".format(min_cpu),
        "cpu_step = {}".format(cpu_step),
        "max_cpu = {}".format(max_cpu),
        "time_spent = {}".format(time_spent),
    ])
else:
    print_list.extend([
        "min_mem = {}".format(min_mem),
        "mem_step = {}".format(mem_step),
        "max_mem = {}".format(max_mem),
        "time_spent = {}".format(time_spent)
    ])

print_list.append(ibench_cmd)
# 最后把控制台输出写到文件里面
with open(src_log_path, 'w') as f:
    for item in print_list:
        f.write(item + "\n")
