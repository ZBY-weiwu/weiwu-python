# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/1


import requests
import chardet
from fake_useragent import UserAgent
from random import choice
import re

from lxml import etree

ua = UserAgent(path=r'.\user_relationship\Tools\useragent.json')



class Downloader_HTML:

    def __init__(self,call_proxy:int=0):
        self.call_proxy = call_proxy
        self.headers = {"User-Agent": ua.chrome}
        proxies_list = [{"http": "http://127.0.0.1:1081", "https": "https://127.0.0.1:1081"}]
        self.proxies = choice(proxies_list)

    def __repr__(self):
        return """说明：call_proxy=0是不使用代理，call_proxy=1时使用代理，支持get/post请求。支持自定义传入headers、dadta
        请求案例：  get_html(url,headers={"h":"333"},data={"a":111})
        """

    def get(self,url:str,**kwargs):
        if kwargs:
            if kwargs["headers"]:
                headers = kwargs.get("headers")
                if self.call_proxy ==0:
                    resp = requests.get(url=url, headers=headers, timeout=20)
                else:
                    resp = requests.get(url=url, headers=headers, timeout=20,proxies=self.proxies)
            else:
                if self.call_proxy == 0:
                    resp = requests.get(url=url, headers=self.headers, timeout=20)
                else:
                    resp = requests.get(url=url, headers=self.headers, timeout=20, proxies=self.proxies)

        else:
            if self.call_proxy == 0:
                resp = requests.get(url=url, headers=self.headers, timeout=20)
            else:
                resp = requests.get(url=url, headers=self.headers, timeout=20, proxies=self.proxies)

        if resp.status_code != 200:
            return
        else:
            headers_item = {}
            headers_item["Content_Type"] = resp.headers["Content-Type"]
            headers_item["body"] = resp.text
            headers_item["body_content"] = resp.content

            page_code  = self.HtmlCode(headers_item)
            resp.encoding=page_code["code"]

            return resp.text

    def post(self,url:str,**kwargs):
        if kwargs:
            if kwargs.get("headers") and kwargs.get("data"):
                data = kwargs.get("data")
                headers = kwargs.get("headers")
                # resp = requests.post(url=url, data=data,headers=self.headers,timeout=20)
                if self.call_proxy ==0:
                    resp = requests.post(url=url, data=data, headers=headers, timeout=20)
                else:
                    resp = requests.post(url=url, headers=headers,data=data, timeout=20,proxies=self.proxies)

            elif kwargs.get("headers") :
                headers = kwargs["headers"]
                if self.call_proxy ==0:
                    resp = requests.post(url=url, headers=headers, timeout=20)
                else:
                    resp = requests.post(url=url, headers=headers, timeout=20,proies =self.proxies)

            elif kwargs["data"]:
                data = kwargs.get("data")
                if self.call_proxy == 0:
                    resp = requests.post(url=url, headers=self.headers, data=data,timeout=20)
                else:
                    resp = requests.post(url=url, headers=self.headers, data=data,imeout=20,proies =self.proxies)

            else:
                if self.call_proxy == 0:
                    resp = requests.post(url=url, headers=self.headers,timeout=20)
                else:
                    resp = requests.post(url=url, headers=self.headers, timeout=20,proies =self.proxies)

        else:
            if self.call_proxy == 0:
                resp = requests.post(url=url, headers=self.headers)
            else:
                resp = requests.post(url=url, headers=self.headers,proies =self.proxies)

        if resp.status_code!=200:
            print("Error!")
            return

        else:
            headers_item = {}
            headers_item["Content_Type"] = resp.headers["Content-Type"]
            headers_item["body"] = resp.text
            headers_item["body_content"] = resp.content

            page_code  = self.HtmlCode(headers_item)
            resp.encoding=page_code["code"]
            return resp.text

    " \
    *可增加扩展编码格式*,后期更新自动扩展编码 \
    "
    def HtmlCode(self,headers_item):
        Content_Type = headers_item["Content_Type"]
        body = headers_item["body"]
        body_content = headers_item["body_content"]
        headers = {}
        headers["Content-Type"]=Content_Type

        item = {}
        item["body"] = body

        if "charset" in headers["Content-Type"]:
            charset_types = ["utf-8","gbk","gb2312","big5"]
            if  re.compile("UTF-8", re.I).search(headers["Content-Type"]):
                item["code"]="utf-8"
            elif re.compile("GBK", re.I).search(headers["Content-Type"]):
                item["code"]="gbk"
            elif re.compile("GB2312", re.I).search(headers["Content-Type"]):
                item["code"]="gb2312"
            elif re.compile("BIG5", re.I).search(headers["Content-Type"]):
                item["code"]="big5"
            elif re.compile("ISO-8859-1", re.I).search(headers["Content-Type"]):
                item["code"]="ISO-8859-1"
            elif re.compile("UTF-16 ", re.I).search(headers["Content-Type"]):
                item["code"]="UTF-16"
            else:
                code = re.findall("charset=(.*?)",headers["Content-Type"])
                item["code"] = code.lower()

        elif  "text/html" in headers["Content-Type"]:
            Code = "".join(re.findall("charset=(.*?)\">",body))

            if len(Code)!=0:
                item["code"] = Code

            """
            else:
                index_url = self.domain_name(url)
                print(index_url)
                index_resp = requests.get(url=index_url, headers=self.headers, proxies=self.proxies)
                index_body = index_resp.text
                if  "text/html" in index_resp.headers["Content-Type"]:
                    index_Code = "".join(re.findall("charset=(.*?)\">", index_body))
                    if len(index_Code) != 0:
                        item["code"] =index_Code
            """

        elif "json" in headers["Content-Type"]:
            item["code"] = "utf-8"

        else:
            item["code"] = chardet.detect(body_content)['encoding']

        return item

    "\
    *获取网站首页url的编码,不推荐* \
    "
    def domain_name(self,url):
        from urllib.parse import urlparse
        res = "https://" + urlparse(url).netloc
        return res

if __name__ == '__main__':
    code_distinguish = by_requests(call_proxy=0)
    print(code_distinguish)
    url = "http://mguba.eastmoney.com/mguba2020/interface/GetData.aspx?param=postid%3D1089887534%26type%3D0%26ps%3D5%26p%3D1%26sort%3D1%26sorttype%3D1&plat=wap&version=200&path=reply%2Fapi%2FReply%2FArticleNewReplyList&env=1&origin=&ctoken=&utoken="
    headers = {"Accept-Language": "zh-CN,zh;q=0.9",
               "Connection": "keep-alive",
               "Content-Length": "124",
               "Content-Type": "application/x-www-form-urlencoded",
               "Cookie": "qgqp_b_id=d264c381ed1039f937a3b4db2d69ef50; HAList=a-sz-000858-%u4E94%20%u7CAE%20%u6DB2; em_hq_fls=js; em-quote-version=topspeed; show_app_box_time=1632725306995; st_si=67135545968649; st_asi=delete; st_pvi=64008435560471; st_sp=2021-09-13%2011%3A31%3A31; st_inirUrl=https%3A%2F%2Fwww.baidu.com%2Flink; st_sn=36; st_psi=20210928135510872-113200301201-5478573055",
               "Host": "mguba.eastmoney.com",
               "Origin": "http", "Referer": "http",
               "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"}
    data = "param=postid=1089887534&sort=1&sorttype=1&p=1&ps=30&path=reply/api/Reply/ArticleNewReplyList"
    CD = code_distinguish.post(url,headers=headers,data=data)
    print(CD)
