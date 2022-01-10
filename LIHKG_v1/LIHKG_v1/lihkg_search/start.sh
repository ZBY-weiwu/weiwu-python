#!/bin/bash
source ~/.bash_profile
cd /root/zby/oversea_Social_media/LIHKG_v1/lihkg_search 
taskid=$1
#taskid=${taskid##*/}
echo $1
scrapy crawl lihkg_spider -a cfg=$taskid

wait
exit 0
