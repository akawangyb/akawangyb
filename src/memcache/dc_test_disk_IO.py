# --------------------------------------------------
# 文件名: dc_test_disk_IO
# 创建时间: 2024/1/26 22:14
# 描述: 用于逐步增加磁盘IO干扰测试容器性能
# 作者: WangYuanbo
# --------------------------------------------------
import argparse
import os
import sys
import threading
import time
from datetime import datetime, timedelta

from collect_data import query_and_write_csv_by_service, query_and_write_csv
from collect_data import run_process, get_log_paths, log_start_time, log_end_time

parser = argparse.ArgumentParser()
parser.add_argument('--type', type=str, help='干扰类型', required=True)
# parser.add_argument('--arg2', type=str, help='这是参数2')

try:
    # 解析参数
    args = parser.parse_args()
except argparse.ArgumentError as err:
    print(str(err))
    sys.exit(1)

trouble_name = args.type
service_name = "memcache"

# 先解决输出路径的问题
# 输出日志的存放路径
father_dir = './' + trouble_name
if not os.path.exists(father_dir):
    os.makedirs(father_dir)

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

# 开始进入测试脚本
# 设置客户端测试参数
# data_path记录运行时资源数据
# log_path记录终端输出
total_time = 50 * 60
time_interval = 1
rps = 45000
dc_client = (
    'docker exec -it dc-client timeout {} /bin/bash /entrypoint.sh --m="RPS" --S=28 --g=0.8 --c=200 --w=8 --T={} '
    '--r={}'.format(total_time, time_interval, rps))

dc_client_thread = threading.Thread(target=run_process, args=(dc_client, service_log_path))
dc_client_thread.start()

# 休息30秒然后注入干扰
time.sleep(60)

time_spent = 120
rw_mode = "randread" if args.type == "diskOut" else "randwrite"
min_BW = 2
step = 2
max_BW = 50
fio_cmd = 'ssh node16 docker exec fiotest ./fio_test.sh {} {} {} {} {}'.format(time_spent, rw_mode, min_BW, step,
                                                                               max_BW)

fio_thread = threading.Thread(target=run_process, args=(fio_cmd, trouble_log_path))
fio_thread.start()
dc_client_thread.join()
fio_thread.join()

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
    output_path=service_data_path)

# 扒下所有的干扰的运行时数据
container_name = "fiotest"
query_and_write_csv(
    container_name=container_name,
    nic_ID="eth0",
    start_time=start_time - timedelta(seconds=5),
    end_time=end_time + timedelta(seconds=5),
    output_path=trouble_data_path
)

# 最后把控制台输出写到文件里面
with open(src_log_path, 'w') as f:
    for item in print_list:
        f.write(item + "\n")
