# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/1


import requests
import chardet
from fake_useragent import UserAgent
from random import choice
import re
import os
dir_path = os.path.dirname
print("绝对路径：",dir_path)
ua = UserAgent(path=r"../../../../QuestionsAnswers/QuestionsAnswers_comment/Tools/useragent.json")


class CodeDistinguish:

    def __init__(self,call_proxy:int=0):
        self.call_proxy = call_proxy
        self.headers = {"User-Agent": ua.chrome}
        proxies_list = [{"http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'}]
        self.proxies = choice(proxies_list)

    def __repr__(self):
        return """说明：call_proxy=0是不使用代理，call_proxy=1时使用代理，支持get/post请求。支持自定义传入headers、dadta
        请求案例：  get_html(url,headers={"h":"333"},data={"a":111})
        """

    def get_html(self,url:str,**kwargs):
        if kwargs:
            if kwargs["headers"]:
                headers = kwargs["headers"]
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

    def post_html(self,url:str,**kwargs):
        if kwargs:
            if kwargs["headers"] and kwargs["data"]:
                data = kwargs["data"]
                headers = kwargs["headers"]
                # resp = requests.post(url=url, data=data,headers=self.headers,timeout=20)
                if self.call_proxy ==0:
                    resp = requests.post(url=url, data=data, headers=headers, timeout=20)
                else:
                    resp = requests.post(url=url, headers=headers,data=data, timeout=20,proxies=self.proxies)

            elif kwargs["headers"]:
                headers = kwargs["headers"]
                if self.call_proxy ==0:
                    resp = requests.post(url=url, headers=headers, timeout=20)
                else:
                    resp = requests.post(url=url, headers=headers, timeout=20,proies =self.proxies)

            elif kwargs["data"]:
                data = kwargs["data"]
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
    code_distinguish = CodeDistinguish(call_proxy=1)
    print(code_distinguish)
    # code_distinguish.UrlIndex("http://www.my-formosa.com/DOC_169337.htm")
    CD = code_distinguish.get_html("http://www.asaninst.org/contents/%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4-%EA%B8%B0%EA%B3%A0%EB%AC%B8-%EC%9C%A0%EC%97%94%EC%82%AC-%ED%95%B4%EC%B2%B4%EB%8A%94-%E6%A0%B8-%EA%B0%80%EC%A7%84-%E5%8C%97%EC%9D%B4-%EB%B0%94%EB%9D%BC%EB%8A%94/")
    # CD = code_distinguish.get_html("https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9751689401257465750%22%7D&n_type=0&p_from=1")
    print(CD)