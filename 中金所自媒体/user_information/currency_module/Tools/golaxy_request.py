# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/1
import requests
import chardet
from fake_useragent import UserAgent
import re
ua = UserAgent(path='./fake_useragent.json')


class GolaxyRequests:

    headers = {"User-Agent": ua.chrome}

    @classmethod
    def GetResponse(cls,resp):
        headers_item = {}
        headers_item["Content_Type"] = resp.headers["Content-Type"]
        headers_item["body"] = resp.text
        headers_item["body_content"] = resp.content
        page_code = cls.GetHtmlCode(headers_item)
        resp.encoding = page_code["code"]
        return resp

    @classmethod
    def get(cls,url:str,**kwargs):
        if kwargs:
            resp = requests.get(url=url,**kwargs)
        else:
            resp = requests.get(url=url, headers=cls.headers, timeout=10)
        return cls.GetResponse(resp)

    @classmethod
    def post(cls,url:str,**kwargs):
        if kwargs:
            resp = requests.post(url=url, **kwargs)
        else:
            resp = requests.post(url=url, headers=cls.headers,timeout=20)
        return cls.GetResponse(resp)

    " \
    *可增加扩展编码格式*,后期更新自动扩展编码 \
    "
    @classmethod
    def GetHtmlCode(cls,headers_item):
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
                code = "".join(re.findall("charset=(.*?)",headers["Content-Type"]))
                item["code"] = code.lower()

        elif  "text/html" in headers["Content-Type"]:
            Code = "".join(re.findall("charset=(.*?)\">",body))
            if len(Code)!=0:
                item["code"] = Code

            # 获取网站首页代码
            """
            else:
                index_url = cls.domain_name(url)
                print(index_url)
                index_resp = requests.get(url=index_url, headers=cls.headers)
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
    @classmethod
    def domain_name(cls,url):
        from urllib.parse import urlparse
        home_page = "https://" + urlparse(url).netloc
        return home_page

if __name__ == '__main__':
    # code_distinguish.UrlIndex("http://www.my-formosa.com/DOC_169337.htm")
    resp = GolaxyRequests.get("http://www.asaninst.org/contents/%EC%A1%B0%EC%84%A0%EC%9D%BC%EB%B3%B4-%EA%B8%B0%EA%B3%A0%EB%AC%B8-%EC%9C%A0%EC%97%94%EC%82%AC-%ED%95%B4%EC%B2%B4%EB%8A%94-%E6%A0%B8-%EA%B0%80%EC%A7%84-%E5%8C%97%EC%9D%B4-%EB%B0%94%EB%9D%BC%EB%8A%94/")
    # CD = code_distinguish.get_html("https://mbd.baidu.com/newspage/data/landingsuper?context=%7B%22nid%22%3A%22news_9751689401257465750%22%7D&n_type=0&p_from=1")
    print(resp.text)