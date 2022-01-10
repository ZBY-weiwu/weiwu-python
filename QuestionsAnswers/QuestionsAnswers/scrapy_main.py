# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin
"scrapy crawl QuestionsAnswersspider  -a cfg=baidu"

from scrapy.cmdline import execute

if __name__ == '__main__':
    execute(["scrapy", "crawl", "QuestionsAnswersspider", "-a", "cfg=baidu"])
    # execute(["scrapy", "crawl", "QuestionsAnswersspider", "-a", "cfg=360"])
    # execute(["scrapy", "crawl", "QuestionsAnswersspider", "-a", "cfg=sougou"])
    # execute(["scrapy", "crawl", "QuestionsAnswersspider", "-a", "cfg=wukong"])