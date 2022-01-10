# -*- coding:utf-8 -*-
# author: zby
# date: 2021/11/12

from user_spider.task_handle.synchro_db import synchro_wemedia_task
from user_spider.task_handle.synchro_db import synchro_weibo_task
import time

if __name__ == '__main__':
    while True:
        synchro_weibo_task.write_pg()
        print("sleep")
        time.sleep(259200)