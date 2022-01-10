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

ua = UserAgent(path=r'.\wemedia_comment\Tools\useragent.json')
# ua = UserAgent(path=r'.\useragent.json')



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
# "Cookie": "device_id=99e35e4a4e21f065553327c17e7a2107; s=dk12klit5a; __utma=1.1795507188.1632276874.1632276874.1632276874.1; __utmz=1.1632276874.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); acw_tc=2760827416381514041256149ea1a80b6aa8f3b8274d2af71027cbb2767d78; xq_a_token=ad254175b8f79f3ce1be51812b24adb083dc9851; xqat=ad254175b8f79f3ce1be51812b24adb083dc9851; xq_r_token=55944e6d0310d70bf0039e421a9a722032a84077; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYzOTc2NDY2MCwiY3RtIjoxNjM4MTUxMzQ5NDUyLCJjaWQiOiJkOWQwbjRBWnVwIn0.oREdu6olsLVSKLzLR228UH31QNlnWXSDI4CGcYkYTV_m5QrOO62xvaIQzxJDiNz0pVWsPM50POz9aPOT9X3TNyEaV4Ovg1UAOSTfd4qE6SQGPGgS2jNC_59Sfn97Y73tA0DdzeaKxREDH4lMws8w6B1gEW-nppJwb5tzRGRiuO3S1GZMex0oW0VVygAmoIGh3llpeKPbmPBVo-mVJQ5o9EVtYN9626amWWs31QAaeMZ6j2u00vMLlmjBg_RAFFH3rIpcK-wjs1y6eDubm80QtNeWUPynF9ImE_oKEtVv7Rrp74vS0Nx6-7IPM9s-Uol1Zju3_D69ZY1U3zy9LoCCTQ; u=191638151404134; Hm_lvt_1db88642e346389874251b5a1eded6e3=1637214832,1637293005,1637657086,1638151404; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1638151611",
if __name__ == '__main__':
    code_distinguish = Downloader_HTML(call_proxy=0)
    print(code_distinguish)
    url = "https://xueqiu.com/statuses/comments.json?id=204363189&count=20&page=2&reply=true&asc=false&type=status&split=true"
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Cookie":"u=371638155625041; xq_a_token=ad254175b8f79f3ce1be51812b24adb083dc9851; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTYzOTc2NDY2MCwiY3RtIjoxNjM4MTU1NjE2Mzg1LCJjaWQiOiJkOWQwbjRBWnVwIn0.gGpEI-hv5_lFD303YdRSBnHmzDJmrEAMmztLYmGmeWLxkleisaakuUGEs02bI5EE7o5eUfRTnnFedelEUj8C2B_npVUK-MqcORVJgtFj_F-Moo1deKVImNr5GgWmhKsFK9QUEAcV3uecDSMBJKMyewUvzceLp1JkddSLpjwveVS-HTKn6_AmMhDO6VUtB3lpMs7aIUk-n1oMucFgrC2OuKeHAxC2PO_PyIk7UQFRvVT1Ooks31JO_vqQ193JvUC0DNpjG-nu9aEfZN-EMGPlFtHOx9nHUnXXnAyb6w-XlaxVoFI5ZWSwsVYL1QTkyUczRHf5C2_PKu4LaX41x_Jp-w; xq_r_token=55944e6d0310d70bf0039e421a9a722032a84077; xqat=ad254175b8f79f3ce1be51812b24adb083dc9851; acw_tc=2760825f16381556249791935ec2e9cddf34920f69711d19f95da0e7a01a9a;",
           "Host": "xueqiu.com",
           "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
           "sec-ch-ua-mobile": "?0",
           "sec-ch-ua-platform": "\"Windows\"",
           "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none",
           "Sec-Fetch-User": "?1",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}
    data = "param=postid=1122391872&sort=1&sorttype=1&p=2&ps=30&path=reply/api/Reply/ArticleNewReplyList"
    CD = code_distinguish.post(url,headers=headers,data=data)
    print(CD)
