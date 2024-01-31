# 测试hadoop-mahout容器性能


### 创建共享卷，解决数据集的问题
```shell
docker volume create wiki-dataset
docker volume ls
```
创建一个临时容器，修改卷的内容
```shell
docker run -it --rm \
  --volume wiki-dataset:/data \
  cloudsuite/base-os:ubuntu
```
定义变量，先安装相关工具包，和数据集

在本机上把数据集解压之后，拷贝到容器里面。在这个容器里面修改data的内容将会保留到卷里面
```shell
BUILD_DEPS="curl bzip2 ca-certificates"
DATASET_FILENAME="enwiki-latest-pages-articles1.xml-p1p41242.bz2"
apt-get update -y && apt-get install -y --no-install-recommends ${BUILD_DEPS}
```

### 创建master节点,以overlay模式运行
```shell
docker service create \
    --network hadoop-net \
    --name hadoop-node1 \
    --hostname=hadoop-node1 \
    --detach \
    --mount type=volume,source=wiki-dataset,target=/data \
    --constraint node.hostname==node1  \
    mahout:jdk.8.hadoop.2.10  --master
```

### 在node16上创建一个slave节点：
```shell
    docker service create \
    --network hadoop-net \
    --name hadoop-node16 \
    --hostname=hadoop-node16 \
    --detach \
    --constraint node.hostname==node16  \
    mahout:jdk.8.hadoop.2.10 --slave --master-ip=hadoop-node1
```


## grep
```shell
./prepare_grep.sh
./run_grep.sh
```

## bayes

```shell
./prepare_bayes.sh
./run_bayes.sh
```