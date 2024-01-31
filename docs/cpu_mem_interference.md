# cpu干扰注入方法
使用iBench进行干扰注入
https://github.com/stanford-mast/iBench/blob/master/README.md

这个项目可以直接编译打包成docker，但是最大的问题是在测试的时候需要后台运行。

要确保容器一直能在后台运行，只需要在Dockerfile的最后一行加上
``
CMD tail -f /dev/null
``

注入CPU干扰的代码解读
```cpp
#define NS_PER_S (1000000000L)

#获得系统时间，单位是纳秒
uint64_t getNs() {
	struct timespec ts;
	clock_gettime(CLOCK_REALTIME, &ts);
	return ts.tv_sec*NS_PER_S + ts.tv_nsec;
}

int main(int argc, const char** argv) {
    //获得系统的最大处理器数量，这里是虚拟cpu
	uint32_t maxThreads = omp_get_num_procs();
	//Usage: "./cpu <duration in sec>"
	if (argc < 2) { 
		printf("Usage: ./cpu <duration in sec>\n"); 
		exit(0);
	}
	//这里是计算每个循环运行的时间，用总的执行时间除以cpu数量
	uint64_t nsPerRun = NS_PER_S*atoi(argv[1])/maxThreads;  // ns

	for (uint32_t threads = 1; threads <= maxThreads; threads++) {
		printf("Running with %d threads\n", threads);
		//设置当前的循环使用的cpu数量
		omp_set_num_threads(threads);
		//计算这个循环的截止时间;
		uint64_t endNs = getNs() + nsPerRun;
		//空循环占用cpu
#pragma omp parallel
		while (getNs() < endNs);
	}
	return 0;
}
```
使用方法,560表示一个循环执行10秒
```shell
./cpu 560
```

```cpp
//获得系统时间，单位纳秒
unsigned long int getNs() {
	struct timespec ts;
	clock_gettime(CLOCK_REALTIME, &ts);
	return ts.tv_sec*NS_PER_S + ts.tv_nsec;
}

//从字符串str里面删除所有的字母c
void remove_all_chars(char* str, char c) {
	char *pr = str, *pw = str;
	while (*pr) {
		*pw = *pr++;
		pw += (*pw != c);
	}
	*pw = '\0';
}

//返回系统可用的全部内存
long long int memory_size_kb(void) {
	char line[512], buffer[32];
	long long int column;
	FILE *meminfo;


	if (!(meminfo = fopen("/proc/meminfo", "r"))) {
		perror("/proc/meminfo: fopen");
		return -1;
	}


	while (fgets(line, sizeof(line), meminfo)) {
		if (strstr(line, "MemTotal")) {
			char* colStr;
			colStr = strstr(line, ":");
			remove_all_chars(colStr, ':'); 
			remove_all_chars(colStr, 'k'); 
			remove_all_chars(colStr, 'B');
			remove_all_chars(colStr, ' ');
			column = atoi(colStr);
		        column = 1000*column;	
			fclose(meminfo);
			return column; 
		}
	}
	fclose(meminfo);
	return -1;
}
// 先申请一个和全部内存一样大的私有内存空间，然后在指定时间之内，反复拷贝这个内存内容
int main(int argc, char **argv) {
	timespec sleepValue = {0};

	char* volatile block;
	long long int MEMORY_SIZE = memory_size_kb(); 
	printf("Total Memory Size: %llu\n", MEMORY_SIZE);

	/*Usage: ./memCap <duration in sec>*/
	if (argc < 2) { 
		printf("Usage: ./cap_mem <duration in sec>\n"); 
		exit(0); 
	}	
	block = (char*)mmap(NULL, MEMORY_SIZE, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, 0, 0);

	int usr_timer = atoi(argv[1]);
	double time_spent = 0.0; 
  	clock_t begin, end;


	while (time_spent < usr_timer) {
  		begin = clock();
		memcpy(block, block+MEMORY_SIZE/2, MEMORY_SIZE/2);
		
		end = clock();
  		time_spent += (double)(end - begin) / CLOCKS_PER_SEC;
	}
	return 0;
}
```

我修改了这个代码，使其能够以一个循环的方式，逐步时间内存干扰

使用方法,第一个参数：每步干扰的最大施加时间，第二个参数：最大内存空间申请量。
```shell
memCap 15 100000000000
```

这个里面存在一个问题，就是申请了内存之后，操作系统不会立即分配

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