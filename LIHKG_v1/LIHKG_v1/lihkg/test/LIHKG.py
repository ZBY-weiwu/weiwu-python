# -*- coding:UTF-8 -*-
import chardet
import urllib3
import requests
#from langconv import *
from requests_html import HTMLSession
from fake_useragent import UserAgent
import sys
ua = UserAgent()


#def Traditional2Simplified(sentence):
#
#    sentence = Converter('zh-hans').convert(sentence)
#    return sentence
session = HTMLSession()
class LD:
    def __init__(self):
        start_urllist = ["https://lihkg.com/category?cat_id=%s&page=1&count=60",]
        self.headers = {"Host": "lihkg.com",
                        "Connection": "keep-alive",
                        "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"", "sec-ch-ua-mobile": "?0",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                        "Accept": "application/json, text/plain, */*",
                        "X-LI-LOAD-TIME": "5.2676917",
                        "X-LI-DEVICE-TYPE": "browser",
                        "X-LI-DEVICE": "ed25fc9fae735203870bfb9d763fad0a5f52d142",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "cors",
                        "Sec-Fetch-Dest": "empty",
                        "Referer": "https://lihkg.com/category/1",
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": "_ga=GA1.1.1212655718.1637570941; _gid=GA1.1.422717220.1637570941; __gads=ID=a2609314b08ac038-22358a853acf009d"}


        # self.proxies = {'http': 'socks5://127.0.0.1:10809', 'https': 'socks5://127.0.0.1:10809'}
        self.proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
    def liandeng_index(self):
        index_url = "https://lihkg.com/api_v2/thread/category?cat_id=5&page=1&count=60&type=now&order=now"#时事

        index_url = "https://lihkg.com/api_v2/thread/category?cat_id=33&page=1&count=60&type=now"
        # req=requests.get(url=index_url, headers=self.headers, timeout=10, proxies=self.proxies)
        req = requests.get(url=index_url, headers=self.headers, timeout=10, proxies=self.proxies)

        print(req.status_code)
        print(req.text)
        # print(chardet.detect(req.content)['encoding'])
        #req.encoding = chardet.detect(req.content)['encoding']

if __name__ == '__main__':

    liandeng = LD()
    liandeng.liandeng_index()

