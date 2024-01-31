# --------------------------------------------------
# 文件名: dc_test_solo
# 创建时间: 2024/1/25 10:43
# 描述: 测试单独运行的dc-server性能
# 作者: WangYuanbo
# --------------------------------------------------
# 用法 python dc_test_solo.py
import os
import sys
import threading
import time
from datetime import datetime, timedelta

import pytz

from collect_data import query_and_write_csv_by_service, log_start_time, log_end_time
from collect_data import run_process

service_name = "memcache"
trouble_name = "solo"
# 先解决日志的存放路径问题
tz = pytz.timezone('Asia/Shanghai')  # 指定时区为东八区，即上海时区
now_time = datetime.now(tz).strftime("%Y%m%d_%H%M")
father_dir = trouble_name + now_time
if not os.path.exists(father_dir):
    os.mkdir(father_dir)

# 获得当前脚本名称
src_name = sys.argv[0]
# 有三个输出文件，一个是测试客户端的终端输出，一个是测试服务器端的运行时数据。
client_log_path = os.path.join(father_dir, service_name + ".log")
server_log_path = os.path.join(father_dir, service_name + ".data.csv")
src_log_path = os.path.join(father_dir, src_name + ".log")

# 测试脚本的记录输出
print_list = []
# 记录测试开始时间
start_time = datetime.fromtimestamp(time.time())
print_list.extend(log_start_time(
    start_time=start_time, src_name=src_name, father_dir=father_dir))

# 开始进入测试脚本
# 设置客户端测试参数
total_time = 30 * 60
time_interval = 1
rps = 45000
dc_client = (
    'docker exec -it dc-client timeout {} /bin/bash /entrypoint.sh --m="RPS" --S=28 --g=0.8 --c=200 --w=8 --T={} '
    '--r={}'.format(total_time, time_interval, rps))
dc_client_thread = threading.Thread(target=run_process, args=(dc_client, client_log_path))
dc_client_thread.start()
# 等待测试完成
dc_client_thread.join()

# 记录测试完成时间
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
    output_path=server_log_path)

# 服务端参数
print_list.extend([
    "total_time = {}".format(total_time),
    "time_interval = {}".format(time_interval),
    "rps = {}".format(rps),
    "dc_client = {}".format(dc_client)
])

# 最后把控制台输出写到文件里面
with open(src_log_path, 'w') as f:
    for item in print_list:
        f.write(item + "\n")
