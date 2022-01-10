# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/1

from requests_html import HTMLSession
from urllib.parse import urljoin
from urllib.parse import unquote
import requests
import re
from fake_useragent import UserAgent

from tenacity import retry, stop_after_attempt
import sys
import logging
import json
from requests import RequestException
logger = logging.getLogger(__name__)
class toutiao_user():

    def __init__(self, session=None, requests_kwargs=None):
        self.user_agent = {
            "User-Agent": "ozilla/5.0 (Windows NT 6.4; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2225.0 Safari/537.36"}
        if session:
            session = session
        else:
            session = HTMLSession()
            session.headers.update(self.user_agent)

        if requests_kwargs is None:
            requests_kwargs = {}

        self.session = session
        # self.session.proxies = proxies
        self.requests_kwargs = requests_kwargs
        self.toutiao_APi = "https://profile.zjurl.cn/user/profile/homepage/share/v7/?app_name=news_article&user_id={}&media_id={}&request_source=1&appId=1286&appType=mobile_detail_web&isAndroid=false&isIOS=false&isMobile=false&cookie_enabled=true&screen_width=1536&screen_height=824&browser_language=zh-CN&browser_platform=Win32&browser_name=firefox&browser_version=93.0.4577.82&browser_online=true&timezone_name=Asia%2FShanghai&_signature=_02B4Z6wo00f01BTMjmgAAIDAlM50KLxpZawUyIrAAGSFHoZKKujpC0nN2CvJioajdnJjCR0Qq8W-qWfjNNwUgG-htRbsoywTru7Ps0FKj8ueWniadPHTeIiSD3lyKWWLXzD8QXPWJgZnB5CXb3"
        url = "https://profile.zjurl.cn/user/profile/homepage/share/v7/?app_name=news_article&user_id=1816036351150420&media_id=1637142071418888&request_source=1&appId=1286&appType=mobile_detail_web&isAndroid=false&isIOS=false&isMobile=false&cookie_enabled=true&screen_width=1536&screen_height=824&browser_language=zh-CN&browser_platform=Win32&browser_name=firefox&browser_version=93.0.4577.82&browser_online=true&timezone_name=Asia%2FShanghai&_signature=_02B4Z6wo00f01BTMjmgAAIDAlM50KLxpZawUyIrAAGSFHoZKKujpC0nN2CvJioajdnJjCR0Qq8W-qWfjNNwUgG-htRbsoywTru7Ps0FKj8ueWniadPHTeIiSD3lyKWWLXzD8QXPWJgZnB5CXb3"
        self.get(url)

    def get(self, url, **kwargs):
        try:
            response = self.session.get(url=url, **self.requests_kwargs, **kwargs)
            response.raise_for_status()
            return response
        except RequestException as ex:
            logger.exception("Exception while requesting URL: %s\nException: %r", url, ex)
            raise

    def toutiao_user_parse(self,response, response2):
        try:
            json_data = response.json()
        except:
            json_data = {}
        print("json_data:", json_data)
        json_obj = response2.json()
        json_data2 = json_obj.get("data")

        json_data = json_data.get("data")

        share_data = json_data.get("share_data")
        wechat_moments = share_data.get("wechat_moments")

        fans = json_data2.get('fans', 0)
        if "万" in fans:
            fans = float(fans.replace("万", "")) * 10000
        elif "亿" in fans:
            fans = float(fans.replace("亿", "")) * 100000000
        fans = int(fans)
        like = json_data2.get('digg_count', 0)
        if "万" in like:
            like = float(like.replace("万", "")) * 10000
        elif "亿" in like:
            like = float(like.replace("亿", "")) * 100000000
        like = int(like)
        follow = json_data2.get('following', 0)
        if "万" in follow:
            follow = float(follow.replace("万", "")) * 10000
        follow = int(follow)
        # 发布
        releases_count = json_data.get('releases_count', 0)

        create_time = json_data.get('create_time', -1)

        uid = json_data.get("user_id", -1)
        user_name = json_data.get('name', "")
        area = json_data.get('area', "")
        desc = wechat_moments.get('desc', "")
        user_img = wechat_moments.get('icon_url', "")
        user_info = json_data.get('description', "")
        item = dict(
            code=response.status_code,
            fans_count=fans,
            like_count=like,
            follow_count=follow,
            releases_count=releases_count,

            uid=uid,
            user_name=user_name,
            area=area,
            desc=desc,
            create_time=create_time,

            user_info=user_info,
            user_img=user_img)
        return item

    def toutiao(self,selfurl):
        count = 0
        # https://profile.zjurl.cn/rogue/ugc/profile/?user_id=105220535018&media_id=1614254699279364&request_source=1
        "https://profile.zjurl.cn/rogue/ugc/profile/?user_id=102913547402&media_id=1619102771781646&request_source=1"
        regex = re.compile(r'user_id=(\d+)&media_id=(\d+)&request_source')
        news_ids = regex.finditer(selfurl)

        for i in news_ids:
            user_url = self.toutiao_APi.format(i.group(1),i.group(2))

            while True:
                if count >= 5:
                    return self.max_res
                count += 1
                resp = self.get(user_url)
                try:
                    resp.json()
                    break
                except:
                    continue
            url = "https://www.toutiao.com/api/pc/user/fans_stat"
            json_data = resp.json()
            json_data = json_data.get("data")
            try:
                url_data = unquote(json_data.get("verified_content_schema"))
            except:
                url_data=None
            if url_data:
                token = "".join(re.findall("crypto_uid=(.*?)&gd_ext_json",url_data))
            else:
                response = self.get("https://www.toutiao.com/c/user/{}/#".format(i.group(1)))
                print(response.url)
                token  ="".join(re.findall("https://www.toutiao.com/c/user/token/(.*?)/",response.url))
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = "token={}".format(token)
            print(data)
            resp2 = requests.post(url, data=data,headers=headers)
            print(resp2.status_code)
            return self.toutiao_user_parse(resp,resp2)

if __name__ == '__main__':
    url = "https://profile.zjurl.cn/rogue/ugc/profile/?user_id=105220535018&media_id=1614254699279&request_source=1"
    print(toutiao_user().toutiao("https://profile.zjurl.cn/rogue/ugc/profile/?user_id=5954781019&media_id=5954781019&request_source=1"))