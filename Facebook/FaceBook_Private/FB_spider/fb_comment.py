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

    def __init__(self,seed_task,**kwargs):


        self.session = HTMLSession()
        url = re.sub('https://www',"https://mbasic",seed_task["url"])
        url = re.sub('https://m\.',"https://mbasic.",url)
        seed_task["url"] = url
        login_data = self.Fb_login_data()
        self.seed_data = seed_task
        self.list_item = {}
        self.session.headers.update(login_data["headers"])
        self.session.cookies.update(login_data["cookie"])
        self.proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
        self.session.proxies = self.proxies
        # requests.get("https://mbasic.facebook.com/profile.php?id=100001937939190", proxies=proxies)

    """
    /profile.php?id=100001937939190&v=timeline&lst=100052975728068%3A100001937939190%3A1626404627&refid=17
    /profile.php?id=100001937939190&v=friends&lst=100052975728068%3A100001937939190%3A1626404627&refid=17
    /profile.php?id=100001937939190&v=photos&lst=100052975728068%3A100001937939190%3A1626404627&refid=17
    /profile.php?id=100001937939190&v=likes&lst=100052975728068%3A100001937939190%3A1626404627&refid=17
    """


    def Fb_spider(self):

        resp = self.session.get(self.seed_data["url"])
        body = (resp.content)
        Fb_HTML = etree.HTML(body)
        FB_url_all = Fb_HTML.xpath("//*[@id=\"root\"]/div[1]/div[1]/div[4]/a/@href")
        url_data = "".join(Fb_HTML.xpath("//*[@id=\"root\"]/div[1]/div[1]/div[4]/a[1]/@href"))
        url_data = parse.unquote(url_data)
        uid = "".join(re.findall("lst=\d+:(\d+):\d+",url_data))
        for link in FB_url_all:
            link = urljoin(mbasic_url,link)
            if "friends" in link:
                self.friends_spider(uid,link)
            elif "timeline" in link:
                pass
            else:
                pass


    def timeline_spider(self,url):
        spider_resp = self.session.get(url=url)
        body = spider_resp.content
        Fb_HTML = etree.HTML(body)

        next_data = "".join(Fb_HTML.xpath("//*[@id=\"m_more_friends\"]/a/@href"))
        next_url = urljoin(mbasic_url, next_data)
        HTML_datas = Fb_HTML.xpath("//*[@id=\"root\"]/div[1]/div[2]/div")
        for HTML_data in HTML_datas:
            item = {}

    def friends_spider(self,uid,friends_link):

        spider_resp = self.session.get(url=friends_link)
        body = spider_resp.content
        Fb_HTML = etree.HTML(body)

        next_data = "".join(Fb_HTML.xpath("//*[@id=\"m_more_friends\"]/a/@href"))
        next_url = urljoin(mbasic_url, next_data)
        HTML_datas = Fb_HTML.xpath("//*[@id=\"root\"]/div[1]/div[2]/div")
        for HTML_data in HTML_datas:
            item={}

            "//*[@id=\"root\"]/div[1]/div[2]/div[1]/table/tbody/tr/td[1]/img"
            item["name"] = self.seed_data["name"]
            item["url"] = re.sub("mbasic","www",self.seed_data["url"])
            item ["uid"] = uid
            self.list_item["name"] = item["name"]
            self.list_item["url"] = item["url"]
            self.list_item["uid"] = item["uid"]

            item["friend_iurl"] = "".join(HTML_data.xpath("./table/tbody/tr/td[1]/img/@src"))
            friend_uname = "".join(HTML_data.xpath("./table/tbody/tr/td[1]/img/@alt"))
            friend_uname = re.sub(", profile picture","",friend_uname)
            item["friend_uname"] = friend_uname
            friend_url = urljoin(PC_index_url,"".join(HTML_data.xpath("./table/tbody/tr/td[2]/a/@href")))
            try:
                friend_url = friend_url.split("&")[0]
            except:
                pass
            item["friend_url"] = friend_url

            friend_uid = "".join(re.findall("php\?id=(\d+)",friend_url))
            if len(friend_uid)<1:
                friend_url1 = re.sub("www","mbasic",friend_url)
                friend_uid = self.get_friend_id(friend_url1)

            item["friend_uid"] = friend_uid
            print(json.dumps(item,ensure_ascii=False))

        if len(next_data) > 0:
            self.friends_next_page(next_url)

    def friends_next_page(self,url,cookies=None):
        a = int(random.uniform(12, 20))
        time.sleep(a)
        headers ={"Host": "mbasic.facebook.com",
           "Connection": "keep-alive",
           "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
           "sec-ch-ua-mobile": "?0",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
           "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "navigate",
           "Sec-Fetch-User": "?1",
           "Sec-Fetch-Dest": "document",
           "Referer": "https",
           "Accept-Language": "zh-CN,zh;q=0.9"}

        # session = HTMLSession()
        if cookies:
            session.cookies.update(cookies)

        spider_resp = self.session.get(url=url,headers=headers)
        # proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
        # spider_resp = session.get(url, headers=headers, proxies=proxies)
        print("此时cookies:",requests.utils.dict_from_cookiejar(self.session.cookies))
        body = spider_resp.content
        Fb_HTML = etree.HTML(body)
        HTML_datas = Fb_HTML.xpath("//*[@id=\"root\"]/div[1]/div[1]/div")
        next_data = "".join(Fb_HTML.xpath("//*[@id=\"m_more_friends\"]/a/@href"))
        next_url = urljoin(mbasic_url,next_data)
        print("下一页")
        print("next_data:",next_data)
        print("next_url:", next_url)
        for HTML_data in HTML_datas:
            item={}

            item["name"] = self.list_item["name"]
            item["url"] = self.list_item["url"]
            item["uid"] = self.list_item["uid"]
            item["friend_iurl"] = "".join(HTML_data.xpath("./table/tbody/tr/td[1]/img/@src"))
            friend_uname = "".join(HTML_data.xpath("./table/tbody/tr/td[1]/img/@alt"))
            friend_uname = re.sub(", profile picture","",friend_uname)
            item["friend_uname"] = friend_uname
            friend_url = urljoin(PC_index_url, "".join(HTML_data.xpath("./table/tbody/tr/td[2]/a/@href")))
            try:
                friend_url = friend_url.split("&")[0]
            except:
                pass
            item["friend_url"] = friend_url

            friend_uid = "".join(re.findall("php\?id=(\d+)",friend_url))
            if len(friend_uid)<1:
                friend_url1 = re.sub("www","mbasic",friend_url)
                friend_uid = self.get_friend_id(friend_url1)

            item["friend_uid"] = friend_uid
            try:
                item_data = json.dumps(item, ensure_ascii=False)
            except:
                pass



        if len(next_data)>0:
            cookies = {'sb': 'OMm-YJvgaMRoH0q_lUahyZGd', ' datr': 'Rcm-YHBQSPzUAvapJ15QHjlO', ' _fbp': 'fb.1.1626401133852.372614239', ' dpr': '1.375', ' locale': 'zh_CN', ' wd': '1396x656', ' c_user': '100070834266702', ' spin': 'r.1004156026_b.trunk_t.1627286809_s.1_v.2_', ' xs': '4%3AZ8wEmWWDbDI2Bw%3A2%3A1627286804%3A-1%3A15002%3A%3AAcVVzVTIENY1J5KCy0dX-lAToVMyBRChhLcuV2sbTQ', ' fr': '1kCodm0jPsRvAssas.AWVMXyu_3xgV3EjSgVDlijnP_lo.Bg_n26.RY.AAA.0.0.Bg_n26.AWXYxx8fJyM'}
            # self.session.cookies.update(cookies)
            self.friends_next_page(next_url)
        else:
            print(spider_resp.text)

    def get_friend_id(self,url):
        resp = self.session.get(url)
        body = (resp.content)
        Fb_HTML = etree.HTML(body)
        url_data = "".join(Fb_HTML.xpath("//*[@id=\"root\"]/div[1]/div[1]/div[4]/a[1]/@href"))
        url_data = parse.unquote(url_data)
        uid = "".join(re.findall("v=timeline&lst=\d+:(\d+):\d+",url_data))
        return uid


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
    seed_task = {"name":"Nguyễn Thanh","url":"https://www.facebook.com/profile.php?id=100070447793677"}
    url = "https://mbasic.facebook.com/profile.php?id=100001937939190"

    facebookfrivate_user =  FacebookPrivate_user(seed_task)
    facebookfrivate_user.Fb_spider()

