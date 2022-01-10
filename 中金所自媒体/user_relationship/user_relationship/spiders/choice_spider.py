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

    def getFactory(self, site_id):

        if site_id == 7010:
            from .guba_relationship import DongfangcaifugubaRelationship
            return DongfangcaifugubaRelationship()
        # if comment_id == 8:
        #     from .toutiao_relationship import JinritoutiaoCommentSpider
        #     return JinritoutiaoCommentSpider()
        elif site_id == 25953:
            from .xueqiu_relationship import XueqiuRelationship
            return XueqiuRelationship()


