import scrapy
from fake_useragent import UserAgent
from urllib.parse import urljoin
import copy
import os
import json
import time
import urllib.parse
import configparser
import execjs
import re
from Encyclopedias.items import EncyclopediasItem
from scrapy.utils.project import get_project_settings
ua = UserAgent(path=r".\Encyclopedias\Tools\useragent.json")
# import sys
# sys.path.append("..")
from Encyclopedias.Tools.by_package import get_logger,Get_md5,readTaskFile,w_pid
from Encyclopedias.Tools.dupClient import DUPClient
dupClient = DUPClient()

parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(parent_dir + "/../../config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")
logger = get_logger('baike', logger_path)


class toutiao_baikeSpider(scrapy.Spider):

    name = 'toutiao_baike'

    def __init__(self):
        # self.headers = {"user-agent":ua.chrome}
        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')
        self.headers = {"referer": "https://www.baike.com", "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"", "sec-ch-ua-mobile": "?0", "sec-fetch-dest": "script", "sec-fetch-mode": "no-cors", "sec-fetch-site": "cross-site", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"}
        self.index_url = "https://www.baike.com/"
        w_pid(self.name)
        self.key_word_data = readTaskFile("./seed")

    def start_requests(self):
        for key_word_list in self.key_word_data:
            for keyword in key_word_list:
                board_list = {}
                print("keyword:",keyword)
                keyword = keyword.strip()
                board_list["keyword"] = keyword
                entryurl = "https://www.baike.com/search?keyword={}".format(urllib.parse.quote(keyword))
                logger.info("entryurl={},crawler_name={}".format("https://www.baike.com/search?keyword={}".format(keyword),self.name))
                request = scrapy.Request(entryurl, callback=self.detail_index,headers=self.headers)
                request.meta["index_list"] = copy.deepcopy(board_list)
                yield request

    def detail_index(self, response):
        index_list = response.meta["index_list"]
        pages = response.body.decode('utf-8')
        json_obj_list = re.findall("\{\"WikiDocList.*?\"SUCCESS\"\}",pages)
        print("json_obj_list:",json_obj_list)

        if len(json_obj_list)>0:
            json_obj = "".join(json_obj_list)

            board_list = {}
            board_list["keyword"] = index_list["keyword"]
            json_data = json.loads(json_obj)
            WikiDocID= json_data["WikiDocList"][0]["WikiDocID"]

            params = execjs.eval("Number(Math.random().toString().substr(3, 8) + Date.now()).toString(36)")
            index_detail_url = "https://www.baike.com/wikiid/{}?prd=result_list&view_id={}".format(WikiDocID,params)

            # print(index_detail_url)
            request = scrapy.Request(index_detail_url, callback=self.detail_index_parse, headers=self.headers)
            request.meta["board_list"] = copy.deepcopy(board_list)
            yield request
        else:
            json_obj_list = re.findall("\[\{\"WikiDoc.*?\"SUCCESS\"\}\]", pages)
            if len(json_obj_list) > 0:
                item = EncyclopediasItem()
                item.init()
                WikiDoc = json.loads(json_obj_list[0])
                if len(WikiDoc) == 0:
                    return
                WikiDoc = WikiDoc[0]
                content_obj = WikiDoc["WikiDoc"]
                item["content"] = content_obj
                item["desc"] = ""
                item["title"] = content_obj["Title"]+"["+content_obj["Subtitle"]+"]"
                isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(item["title"]))
                if (isExist):
                    return
                item["url"] = response.url
                item["media_name"] = "头条百科"
                item["keyword"] = index_list["keyword"]
                dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["title"]))
                logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
                yield item

    def detail_index_parse(self, response):

        detail_list={}
        board_list = response.meta["board_list"]
        detail_list["keyword"] = board_list["keyword"]
        pages = response.body.decode('utf-8')
        json_obj_list = re.findall("\[\{\"WikiDoc.*?\"SUCCESS\"\}\]",pages)
        if len(json_obj_list)>0:
            WikiDoc = json.loads(json_obj_list[0])
            if len(WikiDoc)==0:
                return
            WikiDoc = WikiDoc[0]
            PolysemyList = WikiDoc["WikiDoc"]["PolysemyList"]
            for person_data in PolysemyList:
                WikiDocID = person_data["WikiDocID"]
                Subtitle = person_data["Subtitle"]
                detail_list["title"] = detail_list["keyword"]+"["+Subtitle+"]"
                isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(detail_list["title"]))
                if (isExist):
                    return
                params = execjs.eval("Number(Math.random().toString().substr(3, 8) + Date.now()).toString(36)")
                detail_url = "https://www.baike.com/wikiid/{}?prd=result_list&view_id={}".format(WikiDocID,
                                                                                                       params)
                detail_list["url"] = detail_url
                print(detail_list)
                request = scrapy.Request(detail_list["url"], callback=self.detail_parse, headers=self.headers)
                request.meta["detail_list"] = copy.deepcopy(detail_list)
                yield request

    def detail_parse(self,response):
        detail_list = response.meta["detail_list"]
        item = EncyclopediasItem()
        item.init()
        pages = response.body.decode('utf-8')
        json_obj_list = re.findall("\[\{\"WikiDoc.*?\"SUCCESS\"\}\]",pages)
        if len(json_obj_list)>0:
            WikiDoc = json.loads(json_obj_list[0])
            if len(WikiDoc)==0:
                return
            WikiDoc = WikiDoc[0]
            content = WikiDoc["WikiDoc"]
            item["content"] = content
            item["desc"] = ""
            item["title"] = detail_list["title"]
            item["url"] = response.url
            item["media_name"] = "头条百科"
            item["keyword"] = detail_list["keyword"]
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["title"]))
            logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
            yield item
