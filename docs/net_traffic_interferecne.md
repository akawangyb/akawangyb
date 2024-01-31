# 利用iperf3测试 
iperf3 官方网址 https://github.com/esnet/iperf

iperf3 用户手册
https://software.es.net/iperf/invoking.html#iperf3-manual-page

有一个已经打包到容器的版本
https://github.com/nerdalert/iperf3

修改entrypoint，cmd tail dev/null 使其可以后台运行


## iperf服务器
启动服务器端
```shell
docker run -d --name=iperf-server -p 5201:5201 iperf:2
```
加入交互式环境，启动iperf服务器
```shell
docker exec -it iperf-server bash
iperf3 -s
```

## iperf客户端
启动
```shell
docker run -d --name=iperf-client iperf:2
```
进入交互式环境，并进行连接测试，这里只能用ip连接，不能用主机名
```shell
docker exec -it iperf-client bash
iperf3 -c 11.11.11.16
```
## 基本用法
测试上行带宽
```shell
iperf3 -c 11.11.11.16
```
测试下行带宽
```shell
iperf3 -c 11.11.11.16 -R
```
-b 表示bitrate -t 表示测试时间 -i 表示输出间隔， --timestamp表示时间戳
```shell
iperf3 -c 11.11.11.16 -b 200000000 -t 10 -i 2 --timestamp=%s
```

测试脚本用法
```shell
./iperf_test.sh 11.11.11.16 5 100 100 1200
./iperf_test.sh 11.11.11.16 5 100 100 500 -R
./iperf_test.sh <server_ip> <time_spent_each_test> <min_bit_rate> <step> <max_bit_rate> [option -R]
```

测试功能基本差不多，所以可以在一个代码里面实现
```shell
 python3 dc_test_net.py --Reverse  && sleep 60 &&  python3 dc_test_net.py 
```


- list content1
- list content2
- list content3

1. list content1
2. list content2
3. list content3



*斜体字*

**粗体字**

_斜体字_

**粗体字**

- code:
    - ``print("hello world!")``