# 测试文件的命名规则

## 5个服务名 service_name

1. memcache
2. cassandra
3. postgresql
4. xxx
5. xxx

## 6个干扰名字 trouble_name

1. cpu
2. mem
3. ni (net_in)
4. no (net_out)
5. write (disk_in)
6. read (disk_out)
7. solo (无干扰,单独运行)

## 文件结构

- 服务名
    - 干扰名+时间戳
        - 下面有5个文件
        - 服务的日志,命名为 service_name + ".log"
        - 服务的资源数据,命名为 service_name + ".data.csv"
        - 干扰的日志,命名为 trouble_name + ".log"
        - 干扰的资源数据,命名为 trouble_name + ".data.csv"
        - 测试脚本的参数,命名为 src_name + ".log"
    - 处理后的数据文件 processed_file
        - 共3个文件
        - 服务延迟数据, 命名为 service_name+'.log.csv'
        - 合并后的原始数据, 命名为 service_name+'.'+trouble_name+'.merged.data.csv'
        - 直接可用数据集, 命名为 service_name+'.'+trouble_name+'.dataset.csv'
        - ????这里的数据集还需要进一步清洗,优化?

| 列标题1 | 列标题2 | 列标题3 |
|------|------|------|
| 单元格1 | 单元格2 | 单元格3 |
| 单元格4 | 单元格5 | 单元格6 |

- list content1
- list content2
- list content3

1. list content1
2. list content2
3. list content3

[这是一个链接](https://example.com)


*斜体字*

**粗体字**

_斜体字_

**粗体字**

- code:
    - ``print("hello world!")``