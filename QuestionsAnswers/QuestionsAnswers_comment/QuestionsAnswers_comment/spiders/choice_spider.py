# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/8/4

import re
import random
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin


class abstractFactory(object):
    def __init__(self):
        pass

    def getFactory(self, wenda_comment_id):
        if wenda_comment_id == 1:
            from .baiduwenda_comment_spider import Baiduzhidao_comment_Spider
            return Baiduzhidao_comment_Spider()
        elif wenda_comment_id == 2:
            from ._360wenda_comment_spider import  _360wenda_comment_Spider
            return _360wenda_comment_Spider()

        elif wenda_comment_id == 3:
            from .sougouwenda_comment_spider import  sougouwenda_comment_Spider
            return sougouwenda_comment_Spider()

        elif wenda_comment_id == 4:  #暂时不采集评论
            return
            from .wukongwenda_comment_spider import  wukongwenda_comment_Spider
            return wukongwenda_comment_Spider()


