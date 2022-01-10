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
import sys

def wenda_renminwang():
    url = "http://liuyan.people.com.cn/threads/queryThreadsList"
    data= "fid=0&state=1&lastItem=0"
    headers ={"Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
              "Referer": "http://liuyan.people.com.cn",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

    resp = requests.post(url,data=data,headers=headers)
    print(resp.text)

def wenda_wuhancity():
    url = "http://api1.liuyan.cjn.cn/messageboard/internetUserInterface/selectThreadsByGroup"
    data= "pageSize=5&pageNum=3&fid=6&handleState=&threadState=&"
    headers = {"Content-Type": "application/x-www-form-urlencoded",
               "Referer": "http://liuyan.cjn.cn",
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
    resp = requests.post(url, data=data, headers=headers)
    print(resp.text)

if __name__ == '__main__':
    wenda_wuhancity()