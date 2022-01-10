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

dupClient = DUPClient()


parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.getcwd() + "/config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")
logger_switch = int(conf.get("LoggerPath", "logger_switch"))


os_path = os.getcwd()
ua = UserAgent(path=r".\wemedia_comment\Tools\useragent.json")


class JinritoutiaoCommentSpider():
    def __init__(self):
        print("JinritoutiaoCommentSpider")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')
        self.DUP_CHANNEL_Article = "app"
        self.detail_headers = {"User-Agent": ua.chrome}
        self.ChildTotalPage = 0
        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }

        if logger_switch == 0:
            self.logger_switch=False
        else:
            self.logger_switch = True
        self.logger = get_logger('wemedia_comment', logger_path)

    def formatEntryUrl(self,cfg):

        tmp_url = cfg["detail_url"].format(cfg["total_page"],cfg["detail_id"])
        if self.logger_switch:
            self.logger.info("datil_id=%s,url=%s" % (cfg["detail_id"], cfg["url"]))

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

        url = cfg["detail_url"].format(cfg["total_page"],cfg["detail_id"])
        GolaxyDownloader = golaxy_Downloader(call_proxy=1)
        HTML = GolaxyDownloader.get(url,headers=self.detail_headers)
        json_data = json.loads(HTML)
        comments_count = int(json_data.get("total_number",0))
        get_data = dupClient.getPara(self.DUP_URL, self.DUP_CHANNEL_Article, cfg["url"])
        try:
            get_comment_obj = json.loads(get_data)
        except:

            return True
        # 如果评论采集过comment_index_v1=False，默认为True
        if isinstance(get_comment_obj,int):
            if comments_count == get_comment_obj:
                return False
            else:
                return True
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
        # print("body:",response.body)
        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        json_obj = json.loads(response.body)

        datas = json_obj.get("data")

        count_data = len(datas)
        for data in datas:
            data = data.get("comment")
            item = WemediaCommentItem()
            item.init()

            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            user_data = data.get("reply_user")
            item["comment_id"] = data.get("id_str")
            item["user_id"] = data.get("user_id")
            item["screen_name"] = data.get("user_name")
            item["publish_time"] = int(data.get("create_time"))*1000
            item["content"] = data.get("text")
            item["comments_count"] = int(data.get("reply_count"))
            item["gather_time"] = int(time.time()*1000)
            item["url"] = "https://www.toutiao.com/a{}".format(cfg["detail_id"])

            # 和文章关联的id
            item["root_id"] = Get_md5(cfg["url"])
            item["likes_count"] = data.get("digg_count",0)
            if item["comments_count"]>0:

                Child_url = "https://www.toutiao.com/2/comment/v2/reply_list/?app_name=toutiao_web&id={}&offset={}&count=20".format(item["comment_id"],self.ChildTotalPage)
                print("Child_url:",Child_url)
                Child_request = scrapy.Request(Child_url, callback=self.ChildCommentParse, headers=self.detail_headers)
                Child_request.meta['cfg'] = copy.deepcopy(cfg)
                Child_request.meta['item'] = copy.deepcopy(item)
                yield Child_request

            # isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["comment_id"])
            # if isExist:
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

        if count_data==20:
            cfg["total_page"] += 20
            tmp_url = cfg["detail_url"].format(cfg["total_page"],["detail_id"])
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            # request.meta['item'] =copy.deepcopy(item)
            yield request


    def ChildCommentParse(self,response):
        cfg = response.meta["cfg"]
        json_obj = json.loads(response.body)
        item = response.meta["item"]
        data= json_obj.get("data")
        data= data.get("data")
        if not data:
            return
        for child_reply_data in data:
            print ("child_reply_data:",child_reply_data)
            child_item = ChildCommentItem()
            child_item.init()
            child_user_data = child_reply_data.get("user")

            child_item['media_name'] = cfg["site_name"]
            child_item['media_id'] = cfg["site_id"]
            child_item['comment_id'] = child_reply_data.get("id_str")
            child_item['user_id'] = str(child_user_data.get("user_id"))
            child_item['user_name'] = child_user_data.get("name")
            child_item['screen_name'] = child_user_data.get("screen_name")
            child_item['publish_time'] = child_reply_data.get("create_time") * 1000
            child_item['content'] = child_reply_data.get("content")
            child_item['likes_count'] = child_reply_data.get("digg_count")
            child_item['url'] = item["url"]
            child_item["root_id"] = item["root_id"]
            child_item['parent_id'] = item["comment_id"]

            # child_isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, child_item["comment_id"])
            # if child_isExist:
            #     print("子评论过滤")
            #     continue
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, child_item["comment_id"])
            yield child_item