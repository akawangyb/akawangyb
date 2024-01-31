# 资源占用量查询命令


- cpu_numbers
  - ``sum(irate(container_cpu_usage_seconds_total{name="dc-server"}[120s]))``
- mem
  - ``container_memory_usage_bytes{name="dc-server"}``
- net_in
  - ``irate(container_network_receive_bytes_total{name="dc-server", interface="ens12f1"}[120s])``
- net_out
  - ``irate(container_network_transmit_bytes_total{name="dc-server", interface="ens12f1"}[60s])``
- disk_in
  - ``irate(container_fs_writes_bytes_total{name="dc-server"}[120s])``
- disk_out
  - ``irate(container_fs_reads_bytes_total{name="dc-server"}[120s])``

