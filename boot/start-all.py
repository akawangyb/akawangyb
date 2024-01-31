import subprocess
import os

os.chdir("/home/ecs-user/opt/prometheus-2.45.2.linux-amd64")

start_cadvisor = "docker start cadvisor"
subprocess.run(start_cadvisor, shell=True)
print("cadvisor started successfully!!!")
start_prometheus = "./prometheus --config.file=prometheus.yml"
subprocess.run(start_prometheus, shell=True)
