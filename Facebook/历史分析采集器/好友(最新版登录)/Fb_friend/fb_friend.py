# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/9

import re
import json

import requests
from requests_html import HTMLSession
from FaceBookLogin import Facebook_Login
from urllib.parse import urljoin


from cookie_parse import get_dict_cookie


fb_login = Facebook_Login()

class FacebookFriendSpider:
    headers ={"Host": "m.facebook.com",
              "Connection": "keep-alive",
              "Cache-Control": "max-age=0",
              "sec-ch-ua": "\" Not;A Brand\";v=\"99\","
                           " \"Google Chrome\";v=\"91\", "
                           "\"Chromium\";v=\"91\"",
              "sec-ch-ua-mobile": "?0",
              "Upgrade-Insecure-Requests": "1",
              "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
              "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
              "Sec-Fetch-Site": "same-origin",
              "Sec-Fetch-Mode": "navigate",
              "Sec-Fetch-User": "?1",
              "Sec-Fetch-Dest": "document",
              "Accept-Language": "zh-CN,zh;q=0.9"}

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
        self.session = HTMLSession()
        if not kwargs:
            pass
        elif kwargs['headers']:
            self.session.headers.update(kwargs['headers'])
        else:
            self.session.headers.update(self.headers)
        self.session.proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
        self.self_cookie = self.Fb_login_cookie()

    def next_cookie_data(self):
        return self.next_cookie_data

    def page_num(selfs,fb_num):
        return fb_num

    def get_url(self,url:str,**kwargs):

        if "unit_cursor" not in url:

            self.session.cookies = self.self_cookie
            resp = self.session.get(url)
            self.next_cookie_data = self.session.cookies
            # print(resp.text
            return self.get_next_url(resp.text)

        elif "unit_cursor" in url:
            if self.next_headers:
                print("unit_cursor")
                self.session.headers.update(self.next_headers)
                # self.session.cookies.update(self.next_cookie_data)
                print("next_cookie:",(requests.utils.dict_from_cookiejar(self.next_cookie_data)))
                resp = self.session.post(url)

                print("unit_cursor:",resp.text)
            else:
                print("xxxxxxxxxxxxxx")


    def get_next_url(self,body):
        resp_daata = """{id:"m_more_friends",href:"/preaudience/friends?unit_cursor=AQHRUdWtvt2zezuKtT3lnR4JNheOBd7PsRWYbkA4FBjM9PMXgWEC8F_ndosa4LV_7RA7efeULShGaaNFrENkCha8bQ&lst=100052975728068%3A1353352331%3A1625807964",proximity_pages:5,persist_on_reload:false,logger_name:"unnamed"""
        # url = response.url
        url = "https://m.facebook.com/preaudience/friends"
        # print("url")
        if re.findall("https://\w+\.facebook\.com/\w+/friends",url)[0]:
            next_page_data = re.findall("\{id:\"m_more_friends\"(.*?),persist_on_reload",resp_daata)
            if not next_page_data:
                return

            next_page_data = "".join(next_page_data)
            print(next_page_data)
            try:
                next_page_num = int(re.findall("proximity_pages:(\d+)",next_page_data)[0])
                print(next_page_num)
                self.page_num(next_page_num)
                next_page_link = urljoin(url,re.findall(",href:\"(.*?)\",proximity_pages", next_page_data)[0])
                return next_page_link
            except:
                next_page_num = 0


        elif "unit_cursor" in url:
            pass


    def main(self,url):
        next_page_link = self.get_url(url)
        print("next_page_link:",next_page_link)
        self.get_url(next_page_link)



    def Fb_login_cookie(self):
        get_cookie = fb_login.login("by951118@163.com","qq1161081779")
        return get_cookie


if __name__ == '__main__':
    # get_url()
    url = "https://m.facebook.com/preaudience/friends"
    fb_friend = FacebookFriendSpider()
    fb_friend.main(url)