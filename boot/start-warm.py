import argparse
import subprocess

# 创建一个解析器对象
parser = argparse.ArgumentParser(description='这是一个示例程序')

# 添加需要的参数
parser.add_argument('--dc', type=bool, help='True or False 是否启动dc-client预热')
parser.add_argument('--nosql', type=bool, help='True or False 是否启动cassandra-client预热')
parser.add_argument('--sql', type=bool, help='True or False 是否启动postgresql-client预热')

# 解析参数
args = parser.parse_args()

if args.dc is None and args.nosql is None and args.sql is None:
    parser.error('至少需要提供一个参数')
    parser.print_help()

dc_warm = "docker exec -it dc-client /bin/bash /entrypoint.sh --m=\"W\" --S=28 --D=10240 --w=8 --T=1"
nosql_warm = "docker exec -it cassandra-client /bin/bash ./warmup.sh node1 10000 4"
sql_warm = "docker exec -it postgresql-client /bin/bash -c \"python3 ./root/template/tpcc.py --warm\""

if args.dc:
    subprocess.run(dc_warm, shell=True)
if args.nosql:
    subprocess.run(nosql_warm, shell=True)
if args.sql:
    subprocess.run(sql_warm, shell=True)
