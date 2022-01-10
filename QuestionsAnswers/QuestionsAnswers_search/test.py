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
from Tools.wenda_package import timeStamp_data,str_to_timestamp

# print(str_to_timestamp("2021.08.04 10:14"))

import csv
headers = ['site_url', 'country', 'site_name']
f = open("./oversea_site.csv", "a+", encoding="utf-8",newline='')
f_csv = csv.DictWriter(f, headers)
f_csv.writeheader()
item = {'country': '牙买加',
 'site_name': '英属维尔京群岛副总督府',
 'site_url': 'http://www.dgo.gov.vg/'}
item2 = {'country': '牙买加2',
 'site_name': '英属维尔京群岛副总督府2',
 'site_url': 'http://www.dgo.gov.vg/2'}
item_list = []
item_list.append(item)
item_list.append(item2)
f_csv.writerows(item_list)