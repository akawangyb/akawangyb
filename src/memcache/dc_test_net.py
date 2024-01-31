# --------------------------------------------------
# 文件名: dc_test_net
# 创建时间: 2024/1/26 9:12
# 描述: 逐渐施加流入带宽干扰，观察容器的性能变化
# 作者: WangYuanbo
# --------------------------------------------------
# 使用方法 python3 dc_test_net.py && sleep 60 && python3 dc_test_net.py --Reverse


# 这个测试需要三个节点，在我的实验中node16作为dc服务器和iperf服务器
# 另外有两个节点，分别作为dc客户端（node5）和iperf客户端（node1）
import argparse
import os
import sys
import threading
import time
from datetime import datetime, timedelta

import pytz

from collect_data import get_log_paths, log_start_time, log_end_time
from collect_data import query_and_write_csv_by_service, query_and_write_csv, run_process

parser = argparse.ArgumentParser()
parser.add_argument('--Reverse', action='store_true', help='设置时表示测试下行带宽，否则测试上行带宽')

try:
    # 解析参数
    args = parser.parse_args()
except argparse.ArgumentError as err:
    print(str(err))
    sys.exit(1)

service_name = "memcache"
trouble_name = 'no' if args.Reverse else 'ni'

# 先解决日志的存放路径问题
tz = pytz.timezone('Asia/Shanghai')  # 指定时区为东八区，即上海时区
now_time = datetime.now(tz).strftime("%Y%m%d_%H%M")
father_dir = trouble_name + now_time
if not os.path.exists(father_dir):
    os.mkdir(father_dir)

# 测试脚本的记录输出
# 获得当前脚本名称
print_list = []
src_name = sys.argv[0]
# 输出日志的存放路径
(
    service_log_path,
    service_data_path,
    trouble_log_path,
    trouble_data_path,
    src_log_path
) = get_log_paths(father_dir=father_dir, service_name=service_name, trouble_name=trouble_name, src_name=src_name)

# 记录测试开始时间
start_time = datetime.fromtimestamp(time.time())
print_list.extend(log_start_time(
    start_time=start_time, src_name=src_name, father_dir=father_dir))

# 开始进入测试脚本
# 设置客户端测试参数
# data_path记录运行时资源数据
# log_path记录终端输出
total_time = 20 * 180 + 5 * 60
time_interval = 1
rps = 45000
dc_client = (
    'docker exec -it dc-client timeout {} /bin/bash /entrypoint.sh --m="RPS" --S=28 --g=0.8 --c=200 --w=8 --T={} '
    '--r={}'.format(total_time, time_interval, rps))

dc_client_thread = threading.Thread(target=run_process, args=(dc_client, service_log_path))
dc_client_thread.start()

time.sleep(60 * 3)
# 每一步带宽档运行15s，
# 表示上传带宽200Mb/s
# 写一个shell脚本使之能够实现逐步增加带宽，
# ssh node1 docker exec  iperf-client ./iperf_test.sh 11.11.11.16 5 100 100 1200
# bit_rate = 200000000
server_ip = "11.11.11.16"
init_bit_rate = 50
step = 50
max_bit_rate = 1000
time_spent = 180
iperf_cmd = 'ssh node1 docker exec  iperf-client ./iperf_test.sh {} {} {} {} {}'.format(
    server_ip,
    time_spent,
    init_bit_rate,
    step,
    max_bit_rate
)
if args.Reverse:
    iperf_cmd = iperf_cmd + ' -R'

iperf_thread = threading.Thread(target=run_process, args=(iperf_cmd, trouble_log_path))
iperf_thread.start()

dc_client_thread.join()
iperf_thread.join()

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
container_name = "iperf-server"
query_and_write_csv(
    container_name=container_name,
    nic_ID="eth0",
    start_time=start_time - timedelta(seconds=5),
    end_time=end_time + timedelta(seconds=5),
    output_path=trouble_data_path
)

# 要记录本次测试的各项参数
print_list.append("total_time: {}".format(total_time))
print_list.append("time_interval: {}".format(time_interval))
print_list.append("rps: {}".format(rps))
print_list.append("dc_client_cmd: {}".format(dc_client))

print_list.append("server_ip: {}".format(server_ip))
print_list.append("time_spent: {}".format(time_spent))
print_list.append("init_bit_rate: {}".format(init_bit_rate))
print_list.append("step: {}".format(step))
print_list.append("max_bit_rate: {}".format(max_bit_rate))
print_list.append("iperf_cmd: {}".format(iperf_cmd))

# 最后把控制台输出写到文件里面
with open(src_log_path, 'w') as f:
    for item in print_list:
        f.write(item + "\n")
