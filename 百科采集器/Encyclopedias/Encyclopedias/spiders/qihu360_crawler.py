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


class qihu360_baikeSpider(scrapy.Spider):

    name = '360_baike'

    def __init__(self):
        # self.headers = {"user-agent":ua.chrome}
        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')
        self.headers = {"Host": "baike.so.com", "Referer": "https", "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"", "sec-ch-ua-mobile": "?0", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-User": "?1", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36", "Cookie": "__mid=; gtHuid=1; test_cookie_enable=null; erules=p1-112%7Cp3-10%7Cp4-17%7Cecl-12%7Ckd-33%7Cp2-24%7Cecr-5; __huid=11LsCBRSYcm8JZy3PLQtwO5B%2FsH6Rt7nXWW8SGFdzo76Y%3D; __gid=9114931.125088310.1628738227260.1629280123830.935; QiHooGUID=4C682FE297EDB3B1CF01BA19FB88D5E0.1629357029167; __guid=98281438.1722303104179916000.1629357047495.3848; refer=https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DFGASEaRLPgClGy8p_dN-h-HDrbjK4ucZ9DEj_XjB_DC%26wd%3D%26eqid%3Ddd16507d0000cdb1; __DC_sid=6491553.3648763845137791500.1630287462323.1653; __mid=; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1630287463; test_cookie_enable=null; keyforsearchbar=%E5%AE%9D%E7%8E%89; count=12; __DC_monitor_count=12; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1630288953; __DC_gid=9114931.125088310.1628738227260.1630289026318.962"}
        self.index_url = "https://baike.so.com/"
        w_pid(self.name)
        self.key_word_data = readTaskFile("./seed")

    def start_requests(self):
        for key_word_list in self.key_word_data:
            for keyword in key_word_list:
                board_list = {}
                print("keyword:",keyword)
                keyword = keyword.strip()
                board_list["keyword"] = keyword
                entryurl = "https://baike.so.com/doc/search?word={}".format(urllib.parse.quote(keyword))
                logger.info("entryurl={},crawler_name={}".format("https://baike.so.com/doc/search?word={}".format(keyword),self.name))
                request = scrapy.Request(entryurl, callback=self.detail_index,headers=self.headers)
                request.meta["board_list"] = copy.deepcopy(board_list)
                yield request

    def detail_index(self, response):
        board_list = response.meta["board_list"]
        list_datas = response.xpath("//*[@id=\"sense-list\"]/ul/li/a")
        detail_pages = True
        if len(list_datas)>0:
            for list_data in list_datas:
                list_detail = {}
                list_detail["keyword"] = board_list["keyword"]
                detail_url = "".join(list_data.xpath("./@href").extract()).strip()
                if detail_url=="#":
                    continue
                list_detail["detail_url"] = urljoin(self.index_url,detail_url)
                detail_title = "".join(list_data.xpath("./text()").extract())
                list_detail["detail_title"] = detail_title
                # print(index_detail_url)
                request = scrapy.Request(list_detail["detail_url"], callback=self.detail_parse, headers=self.headers)
                request.meta["list_detail"] = copy.deepcopy(list_detail)
                yield request

        title = "".join(response.xpath("//*[@id=\"baike-title\"]/h1/span[1]//text()").extract())
        if len(title)>0:
            item = EncyclopediasItem()
            item.init()
            try:
                content_obj = response.xpath("//*[@id=\"baike-content\"]").extract()[0]
            except:
                content_obj= ""
            content_obj = ""
            item["content"] = content_obj
            item["desc"] = ""
            item["title"] = title
            item["keyword"] = board_list["keyword"]
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(item["title"]))
            if (isExist):
                return
            item["url"] = response.url
            item["media_name"] = "360百科"
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["title"]))
            logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
            yield item


    def detail_parse(self,response):
        list_detail = response.meta["list_detail"]

        title = "".join(response.xpath("//*[@id=\"baike-title\"]/h1/span[1]//text()").extract())
        if len(title)>0:
            item = EncyclopediasItem()
            item.init()
            try:
                content_obj = response.xpath("//*[@id=\"baike-content\"]").extract()[0]
            except:
                content_obj = ""
            content_obj = ""
            item["content"] = content_obj
            item["desc"] = ""
            item["title"] = list_detail["keyword"]+"-"+list_detail["detail_title"]
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(item["title"]))
            if (isExist):
                return
            item["url"] = response.url
            item["media_name"] = "360百科"
            item["keyword"] = list_detail["keyword"]
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["title"]))
            logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
            yield item
