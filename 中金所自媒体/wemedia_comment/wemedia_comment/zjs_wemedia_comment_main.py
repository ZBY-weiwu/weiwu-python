# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import time
import os
import logging
from scrapy.utils.project import get_project_settings
import eventlet

# 在控制台打印日志
configure_logging()
# CrawlerRunner获取settings.py里的设置信息
runner = CrawlerRunner(get_project_settings())


@defer.inlineCallbacks
def crawl():
    pid = os.getpid() 
    with open("pid/pid.txt","w") as f:
        f.write(str(pid))
    eventlet.monkey_patch(time=True)
    while True:
        with eventlet.Timeout(300, False):
            logging.info("new cycle starting")
            yield runner.crawl("wemedia_comment")
            # 3s跑一次
            time.sleep(3)
    reactor.stop()


crawl()
reactor.run()
