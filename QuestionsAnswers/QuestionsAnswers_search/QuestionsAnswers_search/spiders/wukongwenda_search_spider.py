import scrapy
import os
import json
import copy
import re
import time
import urllib.parse
from urllib.parse import urljoin
import configparser
import requests
from fake_useragent import UserAgent
from QuestionsAnswers_search.items import Questionsanswers_searchItem
from scrapy.utils.project import get_project_settings

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



class wukongwenda_search_Spider():
    def __init__(self):
        print("wukongwenda_search_Spider")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.index_url = "https://www.wukong.com/wenda/wapshare/feed/brow/"
        self.headers = {"User-Agent": ua.chrome}
        self.logger = get_logger('wenda', logger_path)
        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')


    def formatEntryUrl(self,cfg):

        tmp_url = "https://www.wukong.com/wenda/wapshare/search/brow/?search_text={}&offset={}"
        cfg["search_url"] = tmp_url
        tmp_url = tmp_url.format(urllib.parse.quote(cfg["keyword"]),cfg["total_page"])

        self.logger.info("site_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):

        cfg = response.meta["cfg"]
        item = Questionsanswers_searchItem()
        item.init()
        cfg["total_page"] += 1
        item["media_name"] = cfg["site_name"]
        item["media_id"] = cfg["site_id"]

        page = response.body
        jsonObject = json.loads(page)["data"]
        data_list = jsonObject["feed_question"]

        next_page = True
        if len(data_list)<1:
            next_page = False
            return

        a = 1
        for data in data_list:
            a += 1
            list_item = {}
            item["keyword"] = cfg["keyword"]
            # ??????
            item["title"] = data["question"]["title"]

            # ??????
            try:
                item["reward_number"] = 0
            except:
                item["reward_number"] = 0

            extra_info_data = {}
            extra_info_data["reward_number"] = item["reward_number"]
            extra_info = json.dumps(extra_info_data, ensure_ascii=False)
            item["extra_info"] = extra_info

            # ????????????
            item["publish_time"] = data["question"]["create_time"] * 1000

            # ????????????
            item["tags"] = []

            user_data = data["question"]["user"]

            item["author_id"] = user_data["user_id"]
            item["author_img"] = user_data["avatar_url"]
            item["author_screen_name"] = user_data["uname"]

            # ?????????
            item["comments_count"] = 0
            #  ?????????
            item["views_count"] = 0

            item["root_id"] = data["question"]["qid"]

            # ?????????
            item["favourites_count"] = data["question"]["follow_count"]

            # ???????????????
            item["url"] = "https://www.wukong.com/question/{}/?origin_source=question_click_write_answer_feed".format(
                item["root_id"])


            md5_url = Get_md5(item["url"])

            item["md5"] = md5_url
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["root_id"])
            if (isExist):
                continue

            item["gather_time"] = int(time.time()) * 1000
            item["update_time"] = item["gather_time"]
            item["content"] = data["question"]["content"]

            item["picture_urls"] = [i.get("url") for i in data["question"]["content"]["pic_uri_list"]]

            self.logger.info("media_id=%s,id=%s" % (item["media_id"], item["root_id"]))
            comments_data = {}
            comments_data["comments_count"] = item["comments_count"]
            comments_data["comment_index"] = False
            params = json.dumps(comments_data)
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["root_id"], params)
            yield item



        if next_page:
            offset = cfg["total_page"]*10

            tmp_url = "https://www.wukong.com/wenda/wapshare/search/brow/?search_text={}&offset={}"
            cfg["search_url"] = tmp_url
            tmp_url = tmp_url.format(urllib.parse.quote(cfg["keyword"]), offset)
            self.logger.info("board_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
