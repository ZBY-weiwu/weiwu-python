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


import sys


class get_Cookie:

    url = "https://xueqiu.com/"
    headers  = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

    @classmethod
    def get_xueqie_cookie(cls):
        resp = requests.get(cls.url,headers = cls.headers)

        cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        cookies = cls.cookie_dict_str(cookie)
        return cookies

    @classmethod
    def cookie_dict_str(cls,cookie):
        str_cookie = json.dumps(cookie)
        str_cookie = str_cookie[1:]
        str_cookie = str_cookie[:-1]

        str_cookie_list = str_cookie.split(",")
        cookie_data = ""
        for cookies in str_cookie_list:
            cookie_data = cookie_data + cookies.replace(": ", "=") + ";"
        cookie_data = re.sub("\"", "", cookie_data)
        return cookie_data


if __name__ == '__main__':
    get_Cookie.get_xueqie_cookie()