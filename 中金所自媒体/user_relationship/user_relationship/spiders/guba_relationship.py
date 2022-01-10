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
from user_relationship.items import UserRelationshipItem
from scrapy.utils.project import get_project_settings

import configparser
from user_relationship.Tools.my_package import get_logger,Get_md5,str_to_timestamp,timeStamp_data
from user_relationship.Tools.dupClient import DUPClient


dupClient = DUPClient()


parent_dir = os.path.dirname(os.path.abspath(__file__))

conf = configparser.ConfigParser()
conf.read("./config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")



ua = UserAgent(path=r".\user_relationship\Tools\useragent.json")


class DongfangcaifugubaRelationship():
    def __init__(self):

        print("DongfangcaifugubaRelationship")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.logger = get_logger('user_Relationship', logger_path)

    def formatEntryUrl(self,cfg):
        cfg["total_page"]+=1
        if cfg["relationship_type"] == "follower":
            tmp_url = "https://i.eastmoney.com/api/guba/userfans?uid={}&pageindex={}".format(cfg["user_id"],cfg["total_page"])
        elif cfg["relationship_type"] == "follow":
            tmp_url = "https://i.eastmoney.com/api/guba/userFollowPerson?uid={}&pageindex={}".format(cfg["user_id"],cfg["total_page"])
        else:
            return
        self.logger.info("site_name=%s,url=%s" % (cfg["site_name"], tmp_url))
        self.detail_headers = {"User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"}
        request = scrapy.Request(tmp_url, callback=self.parse, headers=self.detail_headers)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request


    def parse(self,response):
        print(response.body)
        cfg = response.meta["cfg"]
        json_obj = json.loads(response.body)

        result = json_obj.get("result")

        datas = result.get("list","")
        if len(datas)==0:
            return

        for data in datas:

            item = UserRelationshipItem()
            item.init()

            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            item["relationship_type"] = cfg["relationship_type"]
            item["owner_uid"] = cfg["user_id"]
            item["owner_name"] = cfg["user_name"]
            item["user_id"] = data["user_id"]
            item["user_name"] = data["user_nickname"]
            item["screen_name"] = data["user_first_en_name"]
            item["friends_count"] = data["user_following_count"]
            item["followers_count"] = data["user_fans_count"]
            item["description"] = data["user_introduce"]
            item["register_time"] = int(time.time())*1000
            item["statuses_count"] = data["user_post_count"]
            item["id"] = Get_md5("11"+str(cfg["user_id"])+str(data["user_id"])+cfg["relationship_type"])

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["id"])
            if isExist:
                continue
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["id"])

            yield item

        if len(datas)==10:
            cfg["total_page"] += 1
            if cfg["relationship_type"] == "follower":
                tmp_url = "https://i.eastmoney.com/api/guba/userfans?uid={}&pageindex={}".format(cfg["user_id"],
                                                                                                 cfg["total_page"])
            elif cfg["relationship_type"] == "follow":
                tmp_url = "https://i.eastmoney.com/api/guba/userFollowPerson?uid={}&pageindex={}".format(cfg["user_id"],cfg["total_page"])
            else:
                return
            self.logger.info("site_name=%s,url=%s" % (cfg["site_name"], tmp_url))
            request = scrapy.FormRequest(tmp_url, callback=self.parse,headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
