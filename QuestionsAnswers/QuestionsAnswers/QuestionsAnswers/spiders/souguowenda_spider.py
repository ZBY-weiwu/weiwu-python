import scrapy
import os
import json
import copy
import re
import time
import urllib.parse
from urllib.parse import urljoin
import configparser
from QuestionsAnswers.items import QuestionsanswersItem
from scrapy.utils.project import get_project_settings
from fake_useragent import UserAgent


import sys
sys.path.append("..")
from Tools.wenda_package import get_logger,Get_md5,str_to_timestamp
from Tools.dupClient import DUPClient
dupClient = DUPClient()

parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(parent_dir + "/../../config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")
logger = get_logger('wenda', logger_path)

os_path = os.getcwd()
ua = UserAgent(path=r".\Tools\useragent.json")


class souguowenda_Spider():
    def __init__(self):
        print("360wenda")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://wenwen.sogou.com/"
        # self.cookie_data = {"BAIDUID":"DC004BE9E557DCA2CE1FD6542FAD4207:FG=1;"}
        self.cookie_data = {'IPLOC': 'CN1100', ' SUID': '9255CA011431A40A0000000060D18B85', ' SUV': '1624345477282507', ' ssuid': '5385277170', ' SNUID': '4A8D13D8D9DD1C16CD34B340D90F3BCD', ' LCLKINT': '2214', ' LSTMV': '108%2C29', ' sw_uuid': '7107154944', ' pid': 'ww.fly.1', ' ss_pidf': '1'}

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

        self.headers = {"Host": "www.sogou.com",
                        "Connection": "keep-alive",
                        "Pragma": "no-cache",
                        "Cache-Control": "no-cache",
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

        self.logger = get_logger('wenda', logger_path)


    def formatEntryUrl(self,cfg):

        tmp_url = cfg["board_url"]+"?tag_id={}&pno={}".format(cfg["config"],cfg["total_page"])
        # tmp_url = "https://zhidao.baidu.com/list?category=%E5%A8%B1%E4%B9%90%E4%BC%91%E9%97%B2"
        print("tmp_url",tmp_url)

        self.logger.info("board_id=%s,entry_url=%s" % (cfg["board_id"], tmp_url))

        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers,cookies=self.cookie_data)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):
        print(response.body)
        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        page = response.body

        page = page.decode("gbk", 'ignore')


        list_xpath = response.xpath("//*[@id=\"questionList\"]/ul/li")
        a = 1
        for data in list_xpath:
            a+=1
            # print("count:",a)
            # print("data",data)
            list_item = {}
            # 问题
            list_item["title"] = "".join(data.xpath("./a/p/text()").extract())
            list_item["title"] = list_item["title"].strip()

            # 悬赏
            try:
                list_item["reward_number"] = int("".join(data.xpath("./a/p/span/text()").extract()))
            except:
                list_item["reward_number"] =0

            # 发布时间
            list_item["pt"] = str_to_timestamp("".join(data.xpath("./a/div[@class=\"sort-rgt\"]/span[2]/text()").extract()))

            # 所属标签
            question_tags = data.xpath("./a/span[@class=\"sort-tag\"]/text()").extract()
            list_item["question_tags"] = [i for i in question_tags]


            # 回答数
            list_item["comments_count"] = "".join(data.xpath("./a/div[@class=\"sort-rgt\"]/span[1]/text()").extract()).strip()
            list_item["comments_count"] = re.sub("个回答","",list_item["comments_count"])

            #详情页链接
            list_item["answer_url"] = urljoin(self.index_url,"".join(data.xpath("./a/@href").extract()))

            md5_url = Get_md5(list_item["answer_url"])
            list_item["md5_url"] = md5_url

            list_item["root_id"] = "".join(re.findall("https://wenwen\.sogou\.com/question/(q\d+)\.htm", list_item["answer_url"]))

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, list_item["root_id"])
            if (isExist):
                continue

            self.detail_headers["Referer"] = response.url
            request = scrapy.Request(list_item["answer_url"], callback=self.detail_parse, headers=self.detail_headers, cookies=self.detail_cookie)
            request.meta["list_item"] = copy.deepcopy(list_item)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
        next_data = "".join(response.xpath("//*[@id=\"questionList\"]/div[2]/a[@class=\"btn-page-next\"]/@href").extract())
        next_url = urljoin(response.url, next_data)
        if len(next_data)>1 and 3>cfg["total_page"]:
            cfg["total_page"] +=1
            tmp_url = next_url
            self.logger.info("board_id=%s,entry_url=%s" % (cfg["board_id"], tmp_url))
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers, cookies=self.cookie_data)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request


    def detail_parse(self,response):

        list_item = response.meta["list_item"]
        cfg = response.meta["cfg"]
        item = QuestionsanswersItem()
        item.Init()
        item["board_id"] = cfg["board_id"]
        item["board_name"] = cfg["board_name"]
        item["media_name"] = cfg["site_name"]
        item["media_id"] = cfg["site_id"]

        # 标题
        item["title"] = list_item["title"]
        # 悬赏数
        reward_number = list_item["reward_number"]

        extra_info_data = {}
        extra_info_data["reward_number"] = reward_number
        extra_info = json.dumps(extra_info_data,ensure_ascii=False)
        item["extra_info"] = extra_info

        item["gather_time"] = int(time.time())*1000
        item["publish_time"] = int(list_item["pt"])*1000
        item["update_time"] = item["gather_time"]
        # 用户信息
        item["author_id"] = "".join(response.xpath("//div[@class=\"ft-info-box\"]/div[@class=\"user-thumb-box\"]/a/@data-uid").extract())
        item["author_img"] ="".join(response.xpath("//div[@class=\"ft-info-box\"]/div[@class=\"user-thumb-box\"]/a/img/@src").extract())
        item["author_screen_name"] = "".join(response.xpath("//div[@class=\"ft-info-box\"]/div[@class=\"user-name-box\"]/a/text()").extract())

        # 阅读数
        views_count = "".join(response.xpath("//div[@class=\"user-txt\"]/span[1]/text()").extract())
        views_count = re.sub("次浏览","",views_count).strip()
        item["views_count"] = int(re.sub("次", "", views_count))
        # 标签浏览
        item["tags"] = list_item["question_tags"]
        # 回答数
        item["comments_count"] = list_item["comments_count"]
        item["md5"] = list_item["md5_url"]
        item["url"] = response.url.split("?")[0]
        item["root_id"] = list_item["root_id"]
        content = "".join(response.xpath("//*[@id=\"question_content\"]//text()").extract())
        content = re.sub("\n\n", "\n", content)
        item["content"] = content
        images = []
        images_data = response.xpath("//*[@id=\"question_images\"]/a/img/@src").extract()
        for image in images_data:
            images.append(image)
        item["picture_urls"] = images
        # print(json.dumps(item,ensure_ascii=False))
        self.logger.info("board_id=%s,id=%s" % (item["board_id"], item["root_id"]))
        comments_data = {}
        comments_data["comments_count"] = item["comments_count"]
        comments_data["comment_index"] = False
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL,self.DUP_CHANNEL, item["root_id"],params)
        yield item

