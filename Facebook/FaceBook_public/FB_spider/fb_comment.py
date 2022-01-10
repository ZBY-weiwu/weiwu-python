# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/15

import re
import random
import time
import requests
import json
from FaceBook_Private.FB_spider.un_name import username,password
from urllib import parse
from lxml import etree
from requests_html import HTMLSession
from FaceBook_Private.util.FaceBookLogin import Facebook_Login
from FaceBook_Private.util.index_url import PC_index_url, mbasic_url
from urllib.parse import urljoin

# https://mbasic.facebook.com/profile.php?id=100001937939190
fb_login = Facebook_Login()

# class FacebookPrivate_user:
class FacebookPrivate_user:

    def __init__(self,user_data,**kwargs):


        self.session = HTMLSession()

        login_data = self.Fb_login_data()

        # self.seed_data = seed_task
        self.list_item = {}

        self.session.headers.update(login_data["headers"])
        self.session.cookies.update(login_data["cookie"])
        self.proxies = {'http': 'http://127.0.0.1:1081', 'https': 'https://127.0.0.1:1081'}
        self.session.proxies = self.proxies
        # requests.get("https://mbasic.facebook.com/profile.php?id=100001937939190", proxies=proxies)


    def Fb_comment(self,seed_list):

        url  =seed_list["url"]
        message_id = seed_list["message_id"]
        url = re.sub('https://www',"https://mbasic",url)
        url = re.sub('https://m\.',"https://mbasic.",url)
        resp = self.session.get(url)
        body = (resp.content)
        Fb_HTML = etree.HTML(body)
        xml_datas = Fb_HTML.xpath("//*[@id=\"ufi_{}\"]/div/div[5]/div".format(message_id))
        for xml_data in xml_datas:
            item = {}
            # 评论人的人物链接
            comment_u_url  = "".join(xml_data.xpath("./div/h3/a/@href"))
            comment_u_url = urljoin(PC_index_url, comment_u_url.split("?")[0])
            comment_uname = "".join(xml_data.xpath("./div/h3/a/text()"))
            item["comment_uname_url"] = comment_u_url
            item["comment_uname"] = comment_uname
            comment_cont = "".join(xml_data.xpath("./div/div[1]//text()"))
            item["comment_cont"] = comment_cont
            comment_like = "".join(xml_data.xpath("./div/div[3]/span/span/text()"))
            item["comment_like"] = comment_like
            print(item)

    def Fb_login_data(self):
        get_login_data = fb_login.login(username,password)
        item={}
        item["headers"] = get_login_data.headers
        item["cookie"] = get_login_data.cookies
        print("headers:",item["headers"])
        print("cookie:",item["cookie"])
        print("cookie_type:", type(item["cookie"]))
        return item



if __name__ == '__main__':

    seed_data = {"message_id": "2569127879789420","url": "https://www.facebook.com/story.php?story_fbid=2569127879789420&id=185848024784096"}
    facebookfrivate_user =  FacebookPrivate_user()
    facebookfrivate_user.Fb_comment(seed_data)

