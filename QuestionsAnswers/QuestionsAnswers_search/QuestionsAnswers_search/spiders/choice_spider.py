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


class abstractFactory():
    def __init__(self):
        pass

    def getFactory(self, wenda_id):
        if wenda_id == 1:
            from .baiduzhidao_search_spider import Baiduzhidao_search_Spider
            return Baiduzhidao_search_Spider()
        elif wenda_id == 2:
            from ._360wenda_search_spider import _360wenda_search_Spider
            return _360wenda_search_Spider()
        elif wenda_id == 3:
            from .sougouwenda_search_spider import sougouwenda_search_Spider
            return sougouwenda_search_Spider()

        elif wenda_id==4:
            from .wukongwenda_search_spider import wukongwenda_search_Spider
            return wukongwenda_search_Spider()


