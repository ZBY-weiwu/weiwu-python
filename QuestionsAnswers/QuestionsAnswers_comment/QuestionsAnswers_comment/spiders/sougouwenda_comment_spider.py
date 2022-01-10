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
sys.path.append("..")
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


class sougouwenda_comment_Spider():
    def __init__(self):
        print("sougouwenda")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://wenwen.sogou.com/"
        self.detail_cookie ={'IPLOC': 'CN1100', ' SUID': '9255CA011431A40A0000000060D18B85', ' SUV': '1624345477282507', ' ssuid': '5385277170', ' SNUID': '4A8D13D8D9DD1C16CD34B340D90F3BCD', ' LCLKINT': '2214', ' LSTMV': '108%2C29', ' sw_uuid': '7107154944', ' pid': 'ww.fly.1', ' ss_pidf': '1'}
        self.detail_headers = {"Host": "wenwen.sogou.com",
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
                        "Accept-Encoding": "gzip, deflate, br",
                        "Accept-Language": "zh-CN,zh;q=0.9"}

        self.detail_headers1 = {"Host": "wenwen.sogou.com",
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
                                "Accept-Encoding": "gzip, deflate, br",
                                "cookie": "IPLOC=CN1100; SUID=9255CA011431A40A0000000060D18B85; SUV=1624345477282507; ssuid=5385277170; sw_uuid=7107154944; sg_uuid=7215477986; ld=Iyllllllll2PVAZOlllllp9QSD6lllllltIq6klllxwlllllRylll5@@@@@@@@@@; LSTMV=347%2C185; LCLKINT=3009203; SNUID=9453CF040600CFC5A46154CD06CBC863; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1629255305,1629255332,1629255379,1630583006; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1630583006",
                                "Accept-Language": "zh-CN,zh;q=0.9"}

        self.logger = get_logger('wenda', logger_path)
        # self.page = 0

    def formatEntryUrl(self,cfg):

        tmp_url = cfg["detail_url"]+"?pg={}".format(cfg["total_page"])
        print("tmp_url:",tmp_url)
        self.logger.info("datil_id=%s,datil_url=%s" % (cfg["detail_id"], tmp_url))
        cfg["Whether_Crawler"] = self.Whether_Crawler(tmp_url, cfg)
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.detail_headers,cookies=self.detail_cookie)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request


    def Whether_Crawler(self,url,cfg):

        code_distinguish = golaxy_Downloader(call_proxy=1)
        HTML = code_distinguish.get_html(url,headers=self.detail_headers1)
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
        cfg["total_page"]+=1

        datas = response.xpath("//div[@class=\"replay-wrap common_answers\"]/div[@class=\"replay-section answer_item\"]")

        for data in datas:
            item = QuestionsanswersCommentItem()
            item.init()
            item["board_id"] = cfg["board_id"]
            item["board_name"] = cfg["board_name"]
            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            author_url = urljoin(self.index_url,"".join(data.xpath("./div[@class=\"user-thumb-box\"]/a/@href").extract()))
            if len(author_url) == 0:
                continue
            item["user_url"] = author_url
            item["user_id"] = "".join(data.xpath("./div[@class=\"user-thumb-box\"]/a/@data-uid").extract())
            if len(item["user_id"])==0:
                item["user_url"]=""
            item["detail_id"] = cfg["detail_id"]
            item["publish_time"] = int(str_to_timestamp("".join(data.xpath("./div[@class=\"replay-info\"]/div[@class=\"user-txt\"]/text()").extract())))*1000
            item["gather_time"] = int(time.time()) * 1000

            # 用户头像
            author_img = "".join(data.xpath("./div[@class=\"user-thumb-box\"]/a/img/@src").extract())
            item["user_img"] = author_img

            # 用户名
            author = "".join(data.xpath("./div[@class=\"replay-info\"]//a[@class=\"user-name\"]/text()").extract()).strip()

            item["user_name"] = author
            if len(item["user_name"])==0:
                item["user_name"]="匿名用户"

            item["comment_id"] = "".join(data.xpath("./@data-id").extract())

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["comment_id"])
            if (isExist):
                continue

            # 回帖
            content = "".join(data.xpath("./div[@class=\"replay-info\"]/pre[@class=\"replay-info-txt answer_con\"]//text()").extract()).strip()
            content = re.sub("\n\n", "\n", content)
            item["comment"] = content
            # 点赞数
            # try:
            like_num = "".join(data.xpath(".//span[@class=\"txt-num\"]/text()").extract())
            # like_num = int(like_num)
            # except:
            #     like_num=0
            item["likes_count"] = like_num
            # 评论数  常量
            item["comments_count"] = 0
            self.logger.info("media_id=%s,comment_id=%s" % (str(item["media_id"]),item["comment_id"]))
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["comment_id"])
            yield item
            # print(json.dumps(item, ensure_ascii=False))

        next_page_url = "".join(response.xpath("//a[@class=\"btn-page-next next_page\"]/@href").extract())
        if len(next_page_url)>0:
            next_page_url = urljoin(response.url,next_page_url)
            self.detail_headers["Referer"] = response.url
            request = scrapy.Request(next_page_url, callback=self.parse, headers=self.detail_headers,
                                     cookies=self.detail_cookie)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
