# 性能测试工具

性能测试，类似loadrunner、jmeter。 实时显示测试结果，生成测试报告。

## 注
* 查看当前的各种用户进程限制 ulimit -a
* 设置用户的最大进程数
    1. ulimit -u 4096
    2. cat /etc/security/limits.d/90-nproc.conf

* 杀掉所有python 进程
kill -9 $(pidof python)

* 修改timewait等待时间
    1. net.ipv4.tcp_fin_timeout = 30
    2. /sbin/sysctl -p

* 查看链接是否断开
netstat -nat | grep 9101