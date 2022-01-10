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

ua = UserAgent(path='fake_useragent.json')



class by_requests:

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
    url = "https://weather.cma.cn/web/weather/58238.html"
    CD = code_distinguish.get(url)
    html =etree.HTML(CD)
    city_html_list = html.xpath("//*[@id=\"cityPosition\"]/div[3]/ul/li")
    for city_data in city_html_list:
        city_name = dict(
            city_valu=city_data.xpath("./@data-value"),
            city_name=city_data.xpath("./text()"),
        )

        print(city_name)
