# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

process = CrawlerProcess(get_project_settings())

# myspd1是爬虫名
# process.crawl('nihaowang')
process.crawl('world68')
# process.crawl('myspd3')

process.start()