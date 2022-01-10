# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28


import requests
from lxml import etree
from fake_useragent import UserAgent
ua = UserAgent(path=r"../../useragent.json")
# headers = {"User-Agent": ua.chrome}
# class baiduwenda_requests:
#
#     def __init__(self):
#         self.session = HTMLSession()

url = "https://zhidao.baidu.com/list?category=%E5%A8%B1%E4%B9%90%E4%BC%91%E9%97%B2&rn=40&pn=0&ie=utf8&_pjax=%23j-question-list-pjax-container"

# headers = {"User-Agent": ua.chrome,"Referer": "https://zhidao.baidu.com"}
headers = {"Host": "zhidao.baidu.com",
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
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9",}
# "Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"}
cookie_data = {"BAIDUID":"DC004BE9E557DCA2CE1FD6542FAD4207:FG=1;"}
cookie_data = {"Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"}
resp = requests.get(url,headers=headers,cookies = cookie_data)
resp.encoding="gbk"
print(resp.text)
HTML = etree.HTML(resp.text)
datas = HTML.xpath("//*[@id=\"j-question-list-pjax-container\"]/div/ul/li")
print(datas)
for data in datas:
    titile = data.xpath("./div[1]/div[@class=\"question-title\"]/a/text()")
    print(titile)
