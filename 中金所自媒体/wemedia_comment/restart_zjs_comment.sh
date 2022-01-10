#!/bin/sh

while true
do
    sleep 3600
    pid=$(cat pid/pid.txt)
    echo "杀死:"+$pid
    kill -9 $pid
    sleep 3
    nohup python3 -u zjs_wemedia_comment_main.py > logs/wemedia_comment.log 2>&1 &
done
