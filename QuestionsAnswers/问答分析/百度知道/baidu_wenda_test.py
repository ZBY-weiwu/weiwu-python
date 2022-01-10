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
from fake_useragent import UserAgent
ua = UserAgent(path=r"../../useragent.json")
# headers = {"User-Agent": ua.chrome}
class Baiduwenda_requests:

    def __init__(self):
        self.session = HTMLSession()
        data = {"Host": "zhidao.baidu.com",
                "Connection": "keep-alive",
                "Cache-Control": "max-age=0",
                "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                "sec-ch-ua-mobile": "?0",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Accept-Language": "zh-CN,zh;q=0.9"}
        # , "Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"
        self.session.headers.update(data)

    def requests_get(self,url):
        self.session.cookies.update({"Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"})
        resp = self.session.get(url)
        resp.encoding="gbk"
        HTML_data= etree.HTML(resp.text)
        datas= HTML_data.xpath("//*[@id=\"j-question-list-pjax-container\"]/div/ul/li")
        # return resp.text
        print("body:",resp.text)
        for i in datas:
            title = i.xpath("./div[1]/div[@class=\"question-title\"]/a/text()")
            print("title:",title)

        print(requests.utils.dict_from_cookiejar(self.session.cookies))




if __name__ == '__main__':
    baiduwenda_requests = Baiduwenda_requests()
    url = "https://zhidao.baidu.com/list?category=%E5%A8%B1%E4%B9%90%E4%BC%91%E9%97%B2&rn=40&pn=0&ie=utf8&_pjax=%23j-question-list-pjax-container"
    baiduwenda_requests.requests_get(url)
