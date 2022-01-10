# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/8/28

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
process = CrawlerProcess(get_project_settings())


# process.crawl('toutiao_baike')
# process.crawl('baidu_baike')
process.crawl('360_baike')
# process.crawl('sougou_baike')

process.start()