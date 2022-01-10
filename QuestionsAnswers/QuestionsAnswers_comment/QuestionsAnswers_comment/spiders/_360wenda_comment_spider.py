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
from wemedia_comment.items import QuestionsanswersCommentItem
from scrapy.utils.project import get_project_settings
import requests
from lxml import etree

import sys
# sys.path.append("..")
from Tools.wenda_package import get_logger,Get_md5,str_to_timestamp
from Tools.dupClient import DUPClient
from Tools.requests_data import CodeDistinguish as golaxy_Downloader
dupClient = DUPClient()


parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(parent_dir + "/../../config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")
logger = get_logger('wenda', logger_path)

os_path = os.getcwd()
ua = UserAgent(path=r".\Tools\useragent.json")




class _360wenda_comment_Spider():
    def __init__(self):
        print("360wenda")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://wenda.so.com/"
        self.detail_cookie ={'gtHuid': '1', ' test_cookie_enable': 'null', ' erules': 'p2-15%7Cecl-2%7Ckd-1%7Cp1-3%7Cp3-2', ' __guid': '9114931.2302920673738409000.1628738227035.168', ' __autoShowTip': 'show', ' WDTKID': 'fa1d06b3d3617943', ' __huid': '11LsCBRSYcm8JZy3PLQtwO5B%2FsH6Rt7nXWW8SGFdzo76Y%3D', ' __sid': '9114931.3809253806408311000.1628747656032.3743', ' count': '22', ' monitor_count': '22', ' __gid': '9114931.125088310.1628738227260.1628748245657.71'}

        self.detail_headers = {"Host": "wenda.so.com",
                        "Connection": "keep-alive",
                        "Cache-Control": "max-age=0",
                        "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                        "sec-ch-ua-mobile": "?0",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Sec-Fetch-Site": "none",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Accept-Language": "zh-CN,zh;q=0.9"}



        self.logger = get_logger('wenda', logger_path)
        # self.page = 0

    def formatEntryUrl(self,cfg):

        tmp_url = cfg["detail_url"]+"?pn={}".format(cfg["total_page"])
        self.logger.info("datil_id=%s,datil_url=%s" % (cfg["detail_id"], tmp_url))
        cfg["Whether_Crawler"] = self.Whether_Crawler(tmp_url,cfg)
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.detail_headers,cookies=self.detail_cookie)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def Whether_Crawler(self,url,cfg):

        code_distinguish = golaxy_Downloader(call_proxy=1)
        HTML = code_distinguish.get_html(url,headers=self.detail_headers)
        response = etree.HTML(HTML)
        comments_count = "".join(response.xpath("//*[@id=\"answer\"]/div[1]/span/text()").extract())
        comments_count = int(re.sub("个回答","",comments_count))

        get_data = dupClient.getPara(self.DUP_URL, self.DUP_CHANNEL, cfg["detail_id"])

        get_comment_obj = json.loads(get_data)
        comment_index_v1 = get_comment_obj["comment_index"]

        comments_data = {}
        comments_data["comments_count"] = comments_count
        comments_data["comment_index"] = True
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, cfg["detail_id"],params)
        if not comment_index_v1:
            return comment_index_v1
        if comments_count !=get_comment_obj["comments_count"]:
            return False
        else:
            return True

    def parse(self,response):
        cfg = response.meta["cfg"]
        if cfg["Whether_Crawler"]:
            return
        cfg["total_page"]+=1

        datas = response.xpath("//*[@id=\"answer\"]/div[@class=\"answer-part js-answer-part\"]") + response.xpath("//*[@id=\"answer\"]/div[@class=\"js-unfold-answer answer-fold-box\"]/div[@class=\"answer-part js-answer-part\"]")+response.xpath("//*[@id=\"answer\"]/div[2]/div[@class=\"answer-part js-answer-part\"]")

        for data in datas:
            item = QuestionsanswersCommentItem()
            item.init()
            author_url = urljoin(self.index_url,"".join(data.xpath("./div[1]/a/@href").extract()))

            if len(author_url) == 0:
                continue

            item["board_id"] = cfg["board_id"]
            item["board_name"] = cfg["board_name"]
            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]

            item["user_url"] = author_url
            item["user_id"] = "".join(data.xpath("./div[1]/a/@index").extract())
            item["detail_id"] = cfg["detail_id"]
            item["publish_time"] = int(str_to_timestamp("".join(data.xpath("./div[1]/div[1]/span[@class=\"user-info-desc\"]/text()").extract())))*1000
            item["gather_time"] = int(time.time()) * 1000

            # 用户头像
            author_img = "".join(data.xpath("./div[1]/a/img/@src").extract())
            item["user_img"] = author_img

            # 用户名
            author = "".join(data.xpath("./div[1]/div/a//text()").extract()).strip()
            item["user_name"] = author

            comment_id= "".join(data.xpath(".//div[@accuse=\"aContent\"]/@id").extract())
            item["comment_id"] = re.sub("answer-content-","",comment_id)
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["comment_id"])
            if (isExist):
                continue

            # 回帖
            content = "".join(data.xpath(".//div[@class=\"answer-content\"]//text()").extract()).strip()
            content = re.sub("\n\n", "\n", content)
            item["comment"] = content
            # 点赞数
            like_num = "".join(data.xpath(".//div[@class=\"answer-part-opt\"]/span[1]/span[1]//text()").extract())
            like_num = int(like_num)
            item["likes_count"] = like_num

            # 评论数  常量
            item["comments_count"] = 0
            # like_num= int(like_num)
            self.logger.info("media_id=%s,comment_id=%s" % (str(item["media_id"]),item["comment_id"]))
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["comment_id"])
            yield item
            # print(json.dumps(item, ensure_ascii=False))
        next_page_url = "".join(response.xpath("//p[@class=\"pages\"]/a[2]/@href").extract())
        if len(next_page_url)>0:
            next_page_url = urljoin(response.url,next_page_url)
            self.detail_headers["Referer"] = response.url
            request = scrapy.Request(next_page_url, callback=self.parse, headers=self.detail_headers,
                                     cookies=self.detail_cookie)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
