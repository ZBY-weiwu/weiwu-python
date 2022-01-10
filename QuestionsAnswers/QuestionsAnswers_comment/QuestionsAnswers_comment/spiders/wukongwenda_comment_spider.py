import scrapy
import os
import json
import copy
import re
import time
import urllib.parse
from urllib.parse import urljoin
import configparser
from fake_useragent import UserAgent
from wemedia_comment.items import QuestionsanswersCommentItem

import sys
sys.path.append("..")
from Tools.wenda_package import get_logger,Get_md5,str_to_timestamp
from Tools.dupClient import DUPClient
dupClient = DUPClient()


parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(parent_dir + "/../../config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")
logger = get_logger('wenda', logger_path)

os_path = os.getcwd()
ua = UserAgent(path=r".\Tools\useragent.json")


class wukongwenda_comment_Spider():
    def __init__(self):
        print("wukongwenda")
        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.headers = {"User-Agent": ua.chrome}

        self.logger = get_logger('wenda', logger_path)
        # self.page = 0

    def formatEntryUrl(self,cfg):
        print("conf:",cfg)
        "https://www.wukong.com/m/wapshare/comment/brow/?ansid={}&offset={}"
        tmp_url = cfg["detail_url"].format(cfg["detail_id"],cfg["total_page"])
        print("tmp_url:",tmp_url)
        self.logger.info("datil_id=%s,datil_url=%s" % (cfg["detail_id"], tmp_url))

        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):

        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        json_obj = json.loads(response.body)
        datas = json_obj.get("comments")
        next_page = True
        if len(datas)<1:
            next_page = False
            return
        for data in datas:
            item = QuestionsanswersCommentItem()
            item.init()
            user_info = data["user_info"]


            item["user_id"] = user_info["user_id"]
            author_url = "https://www.wukong.com/user/?uid={}".format(user_info["user_id"])
            item["user_url"] = author_url

            item["detail_id"] = cfg["detail_id"]
            item["publish_time"] = data["create_time"]
            item["gather_time"] = int(time.time()) * 1000

            # 用户头像
            item["user_img"] = user_info["avatar_url"]

            # 用户名
            item["user_name"] = user_info["uname"]

            item["comment_id"] = data["comment_id"]

            # 回帖
            item["comment"] = data["content"]
            # 点赞数
            # try:
            like_num = data["digg_count"]
            # like_num = int(like_num)
            # except:
            #     like_num=0
            item["likes_count"] = like_num
            # 评论数  常量
            item["comments_count"] = 0
            # like_num= int(like_num)
            yield item

        if next_page:
            offset = cfg["total_page"]*10
            "https://www.wukong.com/m/wapshare/comment/brow/?ansid={}&offset={}"
            tmp_url = cfg["detail_url"].format(cfg["detail_id"], offset)
            # self.headers["Referer"] = response.url
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers,)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
