# -*- coding:UTF-8 -*-
import chardet
import urllib3
import requests
#from langconv import *
from requests_html import HTMLSession
from fake_useragent import UserAgent
import sys
ua = UserAgent()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#def Traditional2Simplified(sentence):
#
#    sentence = Converter('zh-hans').convert(sentence)
#    return sentence
session = HTMLSession()
class LD:
    def __init__(self):
        start_urllist = ["https://lihkg.com/category?cat_id=%s&page=1&count=60",]
        self.headers = {"User-Agent": ua.chrome,
                        "referer":"https://lihkg.com"}
        self.proxies = {'http': 'socks5://192.168.1.50:1080', 'https': 'socks5://192.168.1.50:1080'}
    def liandeng_index(self):
        index_url = "https://lihkg.com/api_v2/thread/category?cat_id=5&page=1&count=60&type=now"#时事
        req=session.get(url=index_url, headers=self.headers, timeout=10, verify=False,proxies=self.proxies)

        print(req.status_code)
        print(req.text)
        # print(chardet.detect(req.content)['encoding'])
        #req.encoding = chardet.detect(req.content)['encoding']

if __name__ == '__main__':

    liandeng = LD()
    liandeng.liandeng_index()

