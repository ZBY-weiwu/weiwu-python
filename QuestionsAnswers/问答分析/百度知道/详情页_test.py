# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28


import requests
import re
from lxml import etree
from fake_useragent import UserAgent
ua = UserAgent(path=r"../../useragent.json")
# headers = {"User-Agent": ua.chrome}
# class baiduwenda_requests:
#
#     def __init__(self):
#         self.session = HTMLSession()

url = "https://zhidao.baidu.com/question/2082535640334635788.html?fr=qlquick&is_force_answer=0&entry=list_highScore_level1"
url = "https://zhidao.baidu.com/question/463883888473524845.html?fr=qlquick&is_force_answer=0"
url2 = "https://zhidao.baidu.com/question/689373095657480732.html?fr=qlquick&is_force_answer=0&entry=list_highScore_all"
# headers = {"User-Agent": ua.chrome,"Referer": "https://zhidao.baidu.com"}
headers = {"Host": "zhidao.baidu.com",
           "Connection": "keep-alive",
           "Cache-Control": "max-age=0",
           "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
           "sec-ch-ua-mobile": "?0",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "navigate",
           "Sec-Fetch-User": "?1",
           "Sec-Fetch-Dest": "document",
           "Referer": "https://zhidao.baidu.com",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9"}


# "Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"}
cookie_data = {"Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"}

resp = requests.get(url2,headers=headers,cookies = cookie_data)
resp.encoding="gbk"
print(resp.text)
HTML = etree.HTML(resp.text)

# datas  =
datas  = HTML.xpath("//*[@id=\"wgt-best\"]/div")+HTML.xpath("//*[@id=\"wgt-answers\"]/div/div")
print("datas:",datas)

for data in datas:
    author_url = "".join(data.xpath("./div[@class=\"wgt-replyer-all\"]/a[1]/@href"))

    if len(author_url)==0:
        continue
    print("author_url", author_url)
    author_img = "".join(data.xpath(".//div[@class=\"wgt-replyer-all-avatar\"]/@style"))
    author_img = re.sub("background-image: url\(", "", author_img)
    author_img = re.sub("\)", "", author_img)
    print("author_img:",author_img)
    author = "".join(data.xpath(".//div[@class=\"wgt-replyer-all\"]/a[2]//text()")).strip()
    print("author:",author)
