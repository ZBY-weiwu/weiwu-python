# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random

import base64
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin

import xml.etree.ElementTree

from xml.etree.ElementTree import parse

xml = parse('./seed.xml')
root = xml.getroot()
board_list = root.findall("board")
item_list = []
for board in board_list:
    item = dict(board_id = (board.find("board_id").text),
    site_name = (board.find("site_name").text),
    site_id = (board.find("site_id").text),
    board_name = (board.find("board_name").text),
    entry_url = (board.find("entry_url").text),
    docurl_regex_yes = (board.find("docurl_regex_yes").text),
    accurate_extraction =  base64.b64decode((board.find("accurate_extraction").text)).decode())
    print(item)
    item_list.append(item)

# print(item_list)




