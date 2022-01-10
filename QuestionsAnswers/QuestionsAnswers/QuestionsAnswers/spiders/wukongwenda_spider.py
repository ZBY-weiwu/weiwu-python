import scrapy
import os
import json
import copy
import re
import time
import urllib.parse
from urllib.parse import urljoin
import configparser
from QuestionsAnswers.items import QuestionsanswersItem
from fake_useragent import UserAgent
from scrapy.utils.project import get_project_settings
import random

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


class wukongwenda_Spider():
    def __init__(self):
        print("wukongwenda_spider")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://www.wukong.com/wenda/wapshare/feed/brow/"
        self.headers = {"User-Agent": ua.chrome}

        self.logger = get_logger('wenda', logger_path)


    def formatEntryUrl(self,cfg):

        t = int(time.time()*1000)
        cfg["t"] =t
        a = [1, 2, 3, 4, 5, 6, 7, 8]
        t_random=random.choice(a)
        max_behot_time =t-(t_random*1000)
        tmp_url = cfg["board_url"]+"&t={}&max_behot_time={}"
        tmp_url = tmp_url.format(cfg["config"], t, max_behot_time)

        self.logger.info("board_id=%s,entry_url=%s" % (cfg["board_id"], tmp_url))

        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):
        cfg = response.meta["cfg"]
        item = QuestionsanswersItem()
        item.Init()
        cfg["total_page"]+=1
        item["board_id"] = cfg["board_id"]
        item["board_name"] = cfg["board_name"]
        item["media_name"] = cfg["site_name"]
        item["media_id"] = cfg["site_id"]

        page = response.body
        jsonObject = json.loads(page)
        data_list = jsonObject["data"]
        if len(data_list)<1:
            return

        a = 1
        for data in data_list:
            a+=1

            # 问题
            item["title"] = data["question"]["title"]

            # 悬赏
            try:
                item["reward_number"] = 0
            except:
                item["reward_number"] = 0

            extra_info_data = {}
            extra_info_data["reward_number"] = item["reward_number"]
            extra_info = json.dumps(extra_info_data, ensure_ascii=False)
            item["extra_info"] = extra_info

            # 发布时间
            item["publish_time"] = data["question"]["create_time"]*1000

            # 所属标签
            item["tags"] = []

            user_data =  data["question"]["user"]

            item["author_id"] = user_data["user_id"]
            item["author_img"] = user_data["avatar_url"]
            item["author_screen_name"] = user_data["uname"]

            # 回答数
            item["comments_count"] = 0
            #  游览数
            item["views_count"] = 0

            item["root_id"] = data["question"]["qid"]

            # 收藏数
            item["favourites_count"] = data["question"]["follow_count"]

            #详情页链接
            item["url"] ="https://www.wukong.com/question/{}/?origin_source=question_click_write_answer_feed".format(item["root_id"])

            md5_url = Get_md5(item["url"])
            item["md5"] = md5_url

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["root_id"])
            if (isExist):
                continue

            item["gather_time"] = int(time.time()) * 1000
            item["update_time"] = item["gather_time"]
            item["content"] = data["question"]["content"]
            item["picture_urls"] = [i.get("url") for i in data["question"]["content"]["thumb_image_list"]]
            self.logger.info("board_id=%s,id=%s" % (item["board_id"], item["root_id"]))
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["root_id"])
            yield item

        try:
            max_behot_time = data_list[1]["behot_time"]
        except:
            return

        next_url = cfg["board_url"]+"&t={}&max_behot_time={}"
        next_url = next_url.format(cfg["config"], cfg["t"], max_behot_time)
        if 3>cfg["total_page"]:
            cfg["total_page"] +=1
            tmp_url = next_url
            self.logger.info("board_id=%s,entry_url=%s" % (cfg["board_id"], tmp_url))
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
