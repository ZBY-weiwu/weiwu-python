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
from wemedia_comment.items import WemediaCommentItem,ChildCommentItem
from scrapy.utils.project import get_project_settings
from lxml import etree

from wemedia_comment.Tools.wenda_package import get_logger,Get_md5,str_to_timestamp,timeStamp_data
from wemedia_comment.Tools.dupClient import DUPClient
from wemedia_comment.Tools.golaxy_request import Downloader_HTML as golaxy_Downloader
from wemedia_comment.Tools.get_Cookie import get_Cookie

dupClient = DUPClient()


parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.getcwd() + "/config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")

os_path = os.getcwd()
ua = UserAgent(path=r"./wemedia_comment/Tools/useragent.json")
logger_switch = int(conf.get("LoggerPath", "logger_switch"))

class XueqiuCommentSpider():
    def __init__(self):
        print("XueqiuCommentSpider")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DUP_CHANNEL_Article = "app"
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')
        cookie = get_Cookie.get_xueqie_cookie()
        self.detail_headers = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
           "Accept-Encoding": "gzip, deflate, br",
           "Accept-Language": "zh-CN,zh;q=0.9",
           "Cache-Control": "max-age=0",
           "Connection": "keep-alive",
           "Cookie": cookie,
           "Host": "xueqiu.com",
           "sec-ch-ua": "\"Chromium\";v=\"94\", \"Google Chrome\";v=\"94\", \";Not A Brand\";v=\"99\"",
           "sec-ch-ua-mobile": "?0",
           "sec-ch-ua-platform": "\"Windows\"",
           "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none",
           "Sec-Fetch-User": "?1",
           "Upgrade-Insecure-Requests": "1",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"}

        if logger_switch == 0:
            self.logger_switch=False
        else:
            self.logger_switch = True
        self.logger = get_logger('wemedia_comment', logger_path)

    def formatEntryUrl(self,cfg):
        cfg["total_page"]+=1
        tmp_url = cfg["detail_url"].format(cfg["detail_id"],cfg["total_page"])
        if self.logger_switch:
            self.logger.info("url=%s" % (cfg["url"]))
        # self.detail_headers = {"User-Agent": ua.chrome}

        Whether_Crawler= self.WhetherCrawler(cfg)
        if Whether_Crawler:
            request = scrapy.Request(tmp_url, callback=self.parse,headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            return request
        else:
            if self.logger_switch:
                self.logger.info("No need to update comments!")
            return

    def WhetherCrawler(self,cfg):

        url = cfg["detail_url"].format(cfg["detail_id"],cfg["total_page"])
        GolaxyDownloader = golaxy_Downloader(call_proxy=0)
        HTML = GolaxyDownloader.get(url,headers=self.detail_headers)
        json_data =json.loads(HTML)
        comments_count = int(json_data.get("count",0))
        get_data = dupClient.getPara(self.DUP_URL, self.DUP_CHANNEL_Article, cfg["url"])
        try:
            get_comment_obj = json.loads(get_data)
        except:
            return True
        if isinstance(get_comment_obj,int):
            if comments_count == get_comment_obj:
                return False
            else:
                return True
        # 如果评论采集过comment_index_v1=False，默认为True
        comment_index_v1 = get_comment_obj.get("comment_index",True)
        comments_data = {}
        comments_data["comments_count"] = comments_count
        comments_data["comment_index"] = comment_index_v1
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL_Article, cfg["url"],params)
        if comments_count == get_comment_obj["comments_count"]:
            return False
        else:
            return True

    def parse(self,response):
        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        json_obj = json.loads(response.body)

        datas = json_obj.get("comments")

        for data in datas:
            item = WemediaCommentItem()
            item.init()

            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            user_data = data.get("user")
            item["comment_id"] = data.get("id")
            item["user_id"] = user_data.get("id")
            item["user_name"] = user_data.get("screen_name")
            item["screen_name"] = user_data.get("screen_name")
            item["publish_time"] = data.get("created_at")
            item["content"] = data.get("text")
            item["comments_count"] = int(data.get("reply_count"))
            item["gather_time"] = int(time.time()*1000)
            item["url"] = cfg["url"]
            reply_comment_data = data.get("reply_comment","")
            if isinstance(reply_comment_data,dict):
                item["parent_id"] =reply_comment_data.get("id")
            # 和文章关联的id
            item["root_id"] = Get_md5(cfg["url"])
            item["likes_count"] = data.get("like_count",0)

            # isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["comment_id"])
            # if isExist:
            #     print("去重过滤")
            #     continue

            comments_data = {}
            comments_data["comments_count"] = item['comments_count']
            # 采集过 comments_data=False
            comments_data["comment_index"] = False
            params = json.dumps(comments_data)
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, cfg["detail_id"], params)
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["comment_id"])
            yield item
            # print(json.dumps(item, ensure_ascii=False))

        if cfg["total_page"]<=10:
            cfg["total_page"] += 1

            tmp_url = cfg["detail_url"].format(cfg["detail_id"],cfg["total_page"])
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request

