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

url = "http://liuyan.people.com.cn/threads/queryThreadsList"
headers={"Accept": "application/json, text/javascript, */*; q=0.01", "Accept-Encoding": "gzip, deflate", "Accept-Language": "zh-CN,zh;q=0.9", "Connection": "keep-alive", "Content-Length": "27", "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8", "Cookie": "wdcid=1c595f945f212751; __jsluid_h=f4b90cf1996dd3d0b690fce71f21f0a4; sso_c=0; sfr=1; _ma_tk=2wjftugrdryzql4zlfvw7y4amvtyracb; 4de1d0bdb25d4625be2481a1b9e1350f=WyIyNzA4MzA1Mzg2Il0; wdses=69e49df924a1c934; wdlast=1636336354; JSESSIONID=7EEDB6EBAACACDDD3FD1EC2BDB562AE5", "Host": "liuyan.people.com.cn", "Origin": "http", "Referer": "http", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36", "X-Requested-With": "XMLHttpRequest"}

resp = requests.post(url=url,headers=headers)
resp.text