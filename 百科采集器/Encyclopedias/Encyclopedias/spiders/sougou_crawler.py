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


class sougou_baikeSpider(scrapy.Spider):

    name = 'sougou_baike'

    def __init__(self):
        # self.headers = {"user-agent":ua.chrome}
        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')
        self.headers = {"Host": "baike.sogou.com",
           "Connection": "keep-alive",
           "sec-ch-ua": "\"Chromium\";v=\"92\", \" Not A;Brand\";v=\"99\", \"Google Chrome\";v=\"92\"",
           "Accept": "*/*",
           "X-Requested-With": "XMLHttpRequest",
           "sec-ch-ua-mobile": "?0",
           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36",
           "Sec-Fetch-Site": "same-origin",
           "Sec-Fetch-Mode": "cors",
           "Sec-Fetch-Dest": "empty",
           "Referer": "https://baike.sogou.com/",
           "Accept-Language": "zh-CN,zh;q=0.9"}
        self.index_url = "https://baike.sogou.com/"
        w_pid(self.name)
        self.key_word_data = readTaskFile("./seed")



    def start_requests(self):
        for key_word_list in self.key_word_data:
            for keyword in key_word_list:
                board_list = {}
                print("keyword:",keyword)
                keyword = keyword.strip()
                board_list["keyword"] = keyword
                entryurl = "https://baike.sogou.com/bapi/searchBarEnter?searchText={}".format(urllib.parse.quote(keyword))
                logger.info("entryurl={},crawler_name={}".format("https://baike.sogou.com/bapi/searchBarEnter?searchText={}".format(keyword),self.name))
                request = scrapy.Request(entryurl, callback=self.Jump_detail,headers=self.headers)
                request.meta["board_list"] = copy.deepcopy(board_list)
                yield request

    def Jump_detail(self,response):

        pages = response.body.decode('utf-8')
        board_list = response.meta["board_list"]
        entryurl = urljoin(self.index_url,pages)
        request = scrapy.Request(entryurl, callback=self.detail_index, headers=self.headers)
        request.meta["board_list"] = copy.deepcopy(board_list)
        yield request

    def detail_index(self, response):
        board_list = response.meta["board_list"]
        list_datas = response.xpath("//*[@id=\"ambi_items\"]/li/a")
        if len(list_datas)>0:
            for list_data in list_datas:
                list_detail = {}
                list_detail["keyword"] = board_list["keyword"]
                detail_url = "".join(list_data.xpath("./@data-href").extract()).strip()

                list_detail["detail_url"] = urljoin(self.index_url,detail_url)
                detail_title = "".join(list_data.xpath("./text()").extract())
                list_detail["detail_title"] = detail_title
                # print(index_detail_url)
                request = scrapy.Request(list_detail["detail_url"], callback=self.detail_parse, headers=self.headers)
                request.meta["list_detail"] = copy.deepcopy(list_detail)
                yield request

        title = "".join(response.xpath("//div[@class=\"abstract_wrap\"]/div/strong/text()").extract())
        key_title = "".join(response.xpath("//*[@id=\"title\"]/text()").extract())
        if len(title)>0:
            item = EncyclopediasItem()
            item.init()
            try:
                content_obj = response.xpath("//div[@class=\"lemma_container\"]").extract()[0]
            except:
                content_obj= ""
            content_obj = ""
            item["content"] = content_obj
            item["desc"] = ""
            item["title"] = board_list["keyword"]+"-"+title
            item["keyword"] = board_list["keyword"]
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(item["title"]))
            if (isExist):
                return
            item["url"] = response.url
            item["media_name"] = "搜狗百科"
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["media_name"]+item["title"]))
            logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
            yield item
        elif len(key_title)>0:
            item = EncyclopediasItem()
            item.init()
            try:
                content_obj = response.xpath("//div[@class=\"lemma_container\"]").extract()[0]
            except:
                content_obj= ""
            content_obj = ""
            item["content"] = content_obj
            item["desc"] = ""
            item["title"] = key_title
            item["keyword"] = board_list["keyword"]
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(item["title"]))
            if (isExist):
                return
            item["url"] = response.url
            item["media_name"] = "搜狗百科"
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["media_name"]+item["title"]))
            logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
            yield item

    def detail_parse(self,response):
        list_detail = response.meta["list_detail"]

        title = "".join(response.xpath("//div[@class=\"abstract_wrap\"]/div/strong/text()").extract())
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
            item["media_name"] = "搜狗百科"
            item["keyword"] = list_detail["keyword"]
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["media_name"]+item["title"]))
            logger.info("keyword={},title={}".format(item["keyword"], item["title"]))
            yield item