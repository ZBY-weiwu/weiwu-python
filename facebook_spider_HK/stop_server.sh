#/bin/bash
##echo "kill process provider"
PID=$(ps -ef|grep fb_hk_server |grep -v grep|awk '{print $2}')
if [ -z $PID ]; then
	echo "进程提供程序不存在"
	exit
else
	echo "process id: $PID"
	kill -9 ${PID}
	echo "进程提供程序已终止"
fi
