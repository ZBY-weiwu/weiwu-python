# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/10/22
from scrapy.cmdline import execute
from Schedulingredis import SchedulingRedis

def scrapy_main():
    execute(["scrapy", "crawl", "WemediaUserRelationship"])

if __name__ == '__main__':
    scrapy_main()
    # execute(["scrapy", "crawl", "wemedia_comment"])