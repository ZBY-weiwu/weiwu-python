# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/15

import re
from FB_spider.un_name import username,password
from requests_html import HTMLSession
from FaceBookLogin import Facebook_Login
from urllib.parse import urljoin

fb_login = Facebook_Login()

class FacebookPrivate_Posts:


    next_headers ={"Host": "m.facebook.com",
                   "Connection": "keep-alive",
                   "Content-Length": "392",
                   "X-FB-LSD": "SMcnDo27shZQMysV3xz0BV",
                   "Content-Type": "application/x-www-form-urlencoded",
                   "X-Requested-With": "XMLHttpRequest",
                   "sec-ch-ua-mobile": "?0",
                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                   "X-Response-Format": "JSONStream",
                   "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                   "Accept": "*/*",
                   "Origin": "https",
                   "Sec-Fetch-Site": "same-origin",
                   "Sec-Fetch-Mode": "cors",
                   "Sec-Fetch-Dest": "empty",
                   "Referer": "https://m.facebook.com/preaudience/friends",
                   "Accept-Language": "zh-CN,zh;q=0.9"}


    def __init__(self,**kwargs):

        self.PC_index_url ="https://www.facebook.com/"
        self.m_index_url = "https://m.facebook.com/"
        self.session = HTMLSession()

        login_data = self.Fb_login_data()
        self.session.headers.update(login_data["headers"])
        self.session.cookies.update(login_data["cookie"])
        self.session.proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}


    def next_cookie_data(self):
        return self.next_cookie_data

    def get_url(self,url:str,**kwargs):
        data = {"fb_dtsg": "",
                "jazoest": "",
                "lsd": "",
                "__dyn": "",
                "__csr": "",
                "__req": "60",
                "__a": "",
                "__user": "100052975728068"}
        resp = self.session.get(url)
        body = resp.text
        next_link = urljoin(self.m_index_url,"".join(re.findall("/profile/timeline/stream/\?cursor.*?\",proximity_pages",body)))
        print(next_link)
        next_page = self.session.post(next_link,data=data)
        print(next_page.text)





    def main(self,url):

        self.get_url(url)



    def Fb_login_data(self):
        get_login_data = fb_login.login(username,password)
        item={}
        item["headers"] = get_login_data.headers
        item["cookie"] = get_login_data.cookies
        return item


if __name__ == '__main__':
    # get_url()
    url = "https://m.facebook.com/chungchunwong"
    Private_Posts = FacebookPrivate_Posts()
    Private_Posts.main(url)