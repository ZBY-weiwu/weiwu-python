#!/usr/bin/python
# -*- coding:utf8 -*-

import requests
import re
from lxml import etree


"\
   查询公网IP \
\
"
def GetProxy():
    proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
    resp = requests.get("http://txt.go.sohu.com/ip/soip",proxies=proxies)
    text = resp.text
    IP = "".join(re.findall(r'\d+.\d+.\d+.\d+',text))
    return IP
    # if re.findall("1\.170\.13\.58",IP):
    #     print(True)

def GetIP_address(proxies):


    headers = {"Host": "www.ez2o.com",
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
     "Accept-Language": "zh-CN,zh;q=0.9",
     "Cookie": "__RequestVerificationToken=NSLqMwaAPRWVKy2wJ96m8cvGZw4dK37kFhQFhx8J28CYK1HQoqJ5dV-HGxa2q7li-iS_UlK0xMwXifAbHEhgXulJeyTL3uB8tkCqlYYQsIQ1; __gads=ID=57085a243cf42497-2267bf0a51ca0094"}

    resp = requests.get("https://www.ez2o.com/App/Net/IP",headers=headers,proxies=proxies)
    text = resp.text
    # print(text)
    html_data = etree.HTML(text)
    country = html_data.xpath("/html/body/div[1]/div/div[1]/div[4]/div[2]/table/tbody/tr[2]/td[2]/span/text()")[0]
    item={}
    item["country"] = country

    print(item)
    return country


def Get_Usr():
    pass


if __name__ == '__main__':
    proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
    GetIP_address(proxies)