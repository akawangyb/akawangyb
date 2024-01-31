# fio 读写性能测试

## 打包镜像
fio文件已经提供了源码

## 测试
首先要挂载一个文件用作测试
```shell
docker run \
--detach \
--name=fiotest \
--volume=/home/wangyuanbo/data:/data \
fio:2
```
测试命令，测试随机读性能。

选择随机读写的进行干扰注入的原因： 
1. 随机读写对磁盘的访问更分散，需要的磁盘寻道次数更多，这往往会带来较大的I/O延迟和CPU使用率，从而更大概率上干扰到其他程序的运行。
2. 随机读写更符合真实环境
```shell
fio --direct=1 \
--iodepth=32 \
--rw=randread \
--ioengine=libaio \
--bs=4k \
--numjobs=4 \
--time_based=1 \
--runtime=30 \
--rate=20m \
--group_reporting \
--filename=/data/stubook.pdf \
--name=test  
```


| 参数                           | 含义                                                          |
|------------------------------|-------------------------------------------------------------|
| --direct=1                   | 设置为直接I/O模式，绕过操作系统的缓存，直接和磁盘交互。                               |
| --iodepth=32                 | 设置I/O深度为32，即每个线程可以同时处理的I/O操作数目。这个参数可以用来模拟不同的并发数。            |
| --rw=randread                | 设置I/O为随机读。还可以选择其他的模式，如randwrite（随机写）、read（顺序读）、write（顺序写）等。 |
| --ioengine=libaio            | 选择I/O引擎为libaio。libaio是Linux平台的异步I/O库                        |
| --bs=4k                      | 设置块大小为4KB。这是每次读写操作的数据大小。                                    |
| --numjobs=4                  | 设置4个并发的I/O操作。                                               |
| --time_based=1               | 设置基于时间的测试，即在指定的时间内一直进行读写操作，不受待测试文件大小的限制。                    |
| --runtime=30                 | 设置测试时间为30秒。                                                 |
| --rate=20m                   | 设置I/O带宽。这里表示读取速率是20MB/s                                     |
| --group_reporting            | 一次性报告所有job的统计信息，而不是对每个job单独报告。                              |
| --filename=/data/stubook.pdf | 设置待测试的文件路径。                                                 |
| --name=test                  | 设置任务名称为test，便于在结果中识别。                                       |

## 测试方法

参数含义 `<time_spent_each_test> <rw_mode> <min_bw> <step> <max_step>`

```shell
docker exec -it fiotest ./fio_test.sh 10 randread 10 2 10
```
进行测试的时候，直接一个搞完，弄另一个，中间休息60秒
```shell
python3 dc_test_disk.py --type=diskIn && \
sleep 60 && \
python3 dc_test_disk.py --type=diskOut
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