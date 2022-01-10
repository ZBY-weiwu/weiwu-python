# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28


import requests
import json
from user_spider.user_behavior.weibo import WeiboBehavior
from user_spider.pipelines import UserBehavior
from tools.golaxy_package import Get_md5

' 测试url\
toutiao_url = "https://m.toutiao.com/i7023577678095696397" \
guba_url = "https://guba.eastmoney.com/news,gssz,1095663931.html" \
xueqiu_url = "https://xueqiu.com/7750449163/201386832" \
'


class UserBehaviorSpider:

    headers = {"accept": "application/json","Content-Type": "application/x-www-form-urlencoded"}
    index_url = "http://10.20.18.10:30086/golaxy/wde/dataservice/v1/appnews/baseinfo"

    @classmethod
    def get_wemedia_BoBehavior(cls,url:str):
        data = {"url": url}
        resp = requests.post(cls.index_url, headers=cls.headers, data=data)
        return resp.text

    @classmethod
    def get_weibo_BoBehavior(cls,url:str):
        return WeiboBehavior(url=url).run()

    @classmethod
    def parse(cls,url:str):
        print("url:",url)
        if "http" in url:
            user_data = json.loads(cls.get_wemedia_BoBehavior(url))
            if "toutiao" in url:
                user_data["media_id"] = 33798
                user_data["media_name"] = "头条号"
            elif "xueqiu" in url:
                user_data["media_id"] = 25953
                user_data["media_name"] = "雪球号"
            elif "eastmoney" in url:
                user_data["media_id"] = 7010
                user_data["media_name"] = "东方财富APP"

            return user_data
        else:
            user_data = cls.get_weibo_BoBehavior(url)
            user_data["media_id"] = 55130
            user_data["media_name"] = "微博"
            return user_data

    @classmethod
    def format_item(cls,url:str,user_data:dict,user_obj=None):
        item={}
        item["media_name"] = user_obj["media_name"]

        if item["media_name"]=="微博":
            item["_key"] = user_data.get("id")
            item["_ch"] = 5
            item["_spec"] = "M-WB03-AI"
        else:
            item["_key"] = Get_md5(url)
            item["_spec"] = "M-APP06-AI"
            item["_ch"] = 11
        item["_dcm"] = "监控采集"
        item["_adp"] = "中科天机"
        item["id"] = str(item["_ch"]) + item["_key"]
        item["media_id"] = str(user_obj["media_id"])
        item["comments_count"] = user_data.get("comment")
        item["likes_count"] = user_data.get("like")
        item["dislikes_count"] = user_data.get("dislike")
        item["share_count"] = user_data.get("share")
        item["reposts_count"] = user_data.get("forward")
        item["views_count"] = user_data.get("read")
        item["attitudes_count"] = user_data.get("join")
        return item

    @classmethod
    def item(cls,url:str):
        user_obj = cls.parse(url)
        user_info = user_obj.get("datas") or user_obj.get("data")
        list_item=[]

        if isinstance(user_info,list):
            for user_data in user_info:
                item = cls.format_item(url,user_data,user_obj)
                list_item.append(item)

        elif isinstance(user_info,dict):
            user_data = user_info
            item = cls.format_item(url,user_data,user_obj)
            list_item.append(item)
        return list_item

    @classmethod
    def Engine(cls,url):
        items = cls.item(url)
        for item in items:

            UserBehavior.process_item(item)
    @classmethod
    def run_Engine(cls,url):
        return cls.Engine(url)

if __name__ == '__main__':
    url = "https://profile.zjurl.cn/rogue/ugc/profile/?user_id=105220535018&media_id=1614254699279364&request_source=1"
    # url = "5167198527,6529876887"
    resp =UserBehaviorSpider.run_Engine(url)
    print(resp)