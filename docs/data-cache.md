#  数据缓存测试笔记

### 首先以服务的形式运行dc-server
docker run --name dc-server 
--net host 
-d cloudsuite/data-caching:server 
-t 4 -m 10240 -n 550
首先创建一个overlay网络
```shell
docker network create --driver overlay data-cache
```
创建服务器端
```shell
docker service create \
--name=dc-server \
--network=data-cache \
--constraint=node.hostname==node16 \
--publish=11211:11211 \
--detach \
cloudsuite/data-caching:server \
-t 4 -m 10240 -n 550
```
客户端进行预热
```shell
docker exec -it dc-client /bin/bash /entrypoint.sh --m="W" --S=28 --D=10240 --w=8 --T=1
```
客户端测试
```shell
docker exec -it dc-client /bin/bash /entrypoint.sh --m="RPS" --S=28 --g=0.8 --c=200 --w=8 --T=1 --r=10000
```
对于memcached容器要进行单独性能测试，干扰注入性能测试。
假设可以先单独测试，然后分别施加cpu，mem，ni，no，di，do

因此我可以先创建一个memcache文件夹，然后创建solo，cpu，mem，ni，no，di，do文件夹
存放数据,相应的使用dc_test_solo.py,dc_test_cpu.py,dc_test_mem.py 表示无干扰，cpu干扰...时候的测试
```shell
python3 dc_test_solo.py
python3 dc_test_cpu.py
```



- list content1
- list content2
- list content3

1. list content1
2. list content2
3. list content3

[这是一个链接](https://example.com)

![interference of container](../logs/log1/myplot.svg)

*斜体字*

**粗体字**

_斜体字_

**粗体字**

- code:
    - ``print("hello world!")``