import scrapy
from fake_useragent import UserAgent
from urllib.parse import urljoin
import copy
import os
import json
import time
import urllib.parse
import configparser
from scrapy.utils.project import get_project_settings
from Encyclopedias.items import EncyclopediasItem

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


class baidu_baikeSpider(scrapy.Spider):

    name = 'baidu_baike'

    def __init__(self):
        self.headers = {"user-agent":ua.chrome}
        self.index_url = "https://baike.baidu.com/"
        w_pid(self.name)
        self.key_word_data = readTaskFile("./seed")
        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

    def start_requests(self):
        for key_word_list in self.key_word_data:
            for keyword in key_word_list:
                board_list = {}
                print("keyword:",keyword)
                keyword = keyword.strip()
                board_list["keyword"] = keyword
                entryurl = "https://baike.baidu.com/item/{}?force=1".format(urllib.parse.quote(keyword))
                logger.info("entryurl={},crawler_name={}".format("https://baike.baidu.com/item/{}?force=1".format(keyword),self.name))
                request = scrapy.Request(entryurl, callback=self.data_parse,headers=self.headers)
                request.meta["board_list"] = copy.deepcopy(board_list)
                yield request

    def data_parse(self, response):
        board_list = response.meta["board_list"]
        detail = False

        html_obj = response.xpath("//div[@class=\"main-content J-content\"]/div[@class=\"top-tool \"]").extract()
        if len(html_obj)>0:
            detail = True

        if detail:
            html = ""
            item= EncyclopediasItem()
            item.init()
            html_obj1 = response.xpath("//div[@class=\"main-content J-content\"]").extract()
            for html_data in html_obj1:
                html += html_data
            item["content"] = html
            item["desc"] = ""
            item["title"] = "".join(response.xpath("//dd[@class=\"lemmaWgt-lemmaTitle-title J-lemma-title\"]//h1//text()").extract()) +"".join(response.xpath("//dd[@class=\"lemmaWgt-lemmaTitle-title J-lemma-title\"]//h2//text()").extract())
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(item["title"]))
            if (isExist):
                return
            item["url"] = response.url
            item["media_name"] = "百度百科"
            item["keyword"] = board_list["keyword"]
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["title"]))
            logger.info("keyword={},url={}".format(board_list["keyword"], response.url))
            yield item

        else:
            print("列表页解析------------------------------")
            list_item = {}
            a_list = response.xpath("//div[@class=\"main-content J-content\"]/ul/li//a")
            for a in a_list:
                list_item["keyword"] = board_list["keyword"]
                list_item["title"] = "".join(a.xpath("./text()").extract())
                isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, Get_md5(list_item["title"]))
                if (isExist):
                    return
                list_item["url"] = urljoin(self.index_url,"".join(a.xpath("./@href").extract()))
                print("list_url:",list_item["url"])
                request = scrapy.Request(list_item["url"], callback=self.detail_parse,headers=self.headers)
                request.meta["list_item"] = copy.deepcopy(list_item)
                yield request

    def detail_parse(self, response):
        list_item = response.meta["list_item"]
        html = ""
        item = EncyclopediasItem()
        item.init()
        html_obj1 = response.xpath("//div[@class=\"main-content J-content\"]").extract()
        for html_data in html_obj1:
            html += html_data
        item["content"] = html
        item["desc"] = ""
        item["title"] = list_item["title"]
        item["url"] = response.url
        item["media_name"] = "百度百科"
        item["keyword"] = list_item["keyword"]
        dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, Get_md5(item["title"]))
        logger.info("keyword={},url={}".format(list_item["keyword"], response.url))
        yield item
