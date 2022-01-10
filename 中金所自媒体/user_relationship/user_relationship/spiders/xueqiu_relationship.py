import scrapy
import os
import json
import copy
import configparser
from fake_useragent import UserAgent
from user_relationship.items import UserRelationshipItem
from scrapy.utils.project import get_project_settings

from user_relationship.Tools.my_package import get_logger,Get_md5,str_to_timestamp,timeStamp_data
from user_relationship.Tools.dupClient import DUPClient
from user_relationship.Tools.get_Cookie import get_Cookie
from user_relationship.Tools.golaxy_request import Downloader_HTML as golaxy_Downloader

dupClient = DUPClient()


parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read("./config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")

os_path = os.getcwd()
ua = UserAgent(path=r".\user_relationship\Tools\useragent.json")


class XueqiuRelationship():
    def __init__(self):
        print("XueqiuRelationship")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')
        Cookie = get_Cookie.get_xueqie_cookie()
        self.detail_headers = {"Accept-Encoding": "gzip, deflate, br",
                 "Accept-Language": "zh-CN,zh;q=0.9",
                 "Connection": "keep-alive",
                 "Cookie": Cookie,
                 "Referer": "https://xueqiu.com/",
                 "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
                 "sec-ch-ua-mobile": "?0",
                 "sec-ch-ua-platform": "\"Windows\"",
                 "Sec-Fetch-Dest": "empty",
                 "Sec-Fetch-Mode": "cors", "Sec-Fetch-Site": "same-origin",
                 "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36",
                 "X-Requested-With": "XMLHttpRequest"}

        self.logger = get_logger('user_relationship', logger_path)

    def formatEntryUrl(self,cfg):
        cfg["total_page"]+=1
        if cfg["relationship_type"] == "follower":
            tmp_url = "https://xueqiu.com/friendships/followers.json?uid={}&pageNo={}&gid=0".format(cfg["user_id"],cfg["total_page"])
        elif cfg["relationship_type"] == "follow":
            tmp_url = "https://xueqiu.com/friendships/groups/members.json?uid={}&page={}&gid=0".format(cfg["user_id"],cfg["total_page"])
        else:
            return
        self.logger.info("site_name=%s,url=%s" % (cfg["site_name"], tmp_url))
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.detail_headers)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):
        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        json_obj = json.loads(response.body)
        if cfg["relationship_type"]=="follow":
            datas = json_obj.get("users",[])
        elif cfg["relationship_type"]=="follower":
            datas = json_obj.get("followers", [])
        for data in datas:
            item = UserRelationshipItem()
            item.init()
            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            item["relationship_type"] = cfg["relationship_type"]
            item["owner_uid"] = cfg["user_id"]
            item["owner_name"] = cfg["user_name"]
            item["user_id"] = str(data["id"])
            item["user_name"] = data["screen_name"]
            item["screen_name"] = data["screen_name"]
            item["friends_count"] = data["friends_count"]
            item["followers_count"] = data["followers_count"]
            item["description"] = ""
            item["register_time"] = data["created_at"]
            item["statuses_count"] = data["status_count"]
            profile_image_url = "https"+data["photo_domain"]+data["profile_image_url"].split(",")[0]
            item["profile_image_url"] = profile_image_url
            item["id"] = Get_md5("11"+str(cfg["user_id"])+str(item["user_id"])+cfg["relationship_type"])

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["id"])
            if isExist:
                continue

            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["id"])
            yield item
            # print(json.dumps(item, ensure_ascii=False))

        if len(datas)==20:
            cfg["total_page"] += 1
            if cfg["relationship_type"] == "follower":
                tmp_url = "https://xueqiu.com/friendships/followers.json?uid={}&pageNo={}&gid=0".format(cfg["user_id"],
                                                                                                        cfg[
                                                                                                            "total_page"])
            elif cfg["relationship_type"] == "follow":
                tmp_url = "https://xueqiu.com/friendships/groups/members.json?uid={}&page={}&gid=0".format(
                    cfg["user_id"], cfg["total_page"])
            else:
                return
            self.logger.info("site_name=%s,url=%s" % (cfg["site_name"], tmp_url))
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request