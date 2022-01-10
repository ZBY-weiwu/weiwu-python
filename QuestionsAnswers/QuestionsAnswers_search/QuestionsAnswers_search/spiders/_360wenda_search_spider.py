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
from QuestionsAnswers_search.items import Questionsanswers_searchItem
from scrapy.utils.project import get_project_settings

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


class _360wenda_search_Spider():
    def __init__(self):
        print("360wenda_search")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://wenda.so.com/search"
        self.cookie_data = {'gtHuid': '1', ' test_cookie_enable': 'null', ' erules': 'p1-36%7Cecl-2%7Cp4-5%7Cecr-1%7Ckd-2%7Cp2-1', ' __guid': '9114931.2302920673738409000.1628738227035.168', ' __autoShowTip': 'show', ' WDTKID': 'fa1d06b3d3617943', ' __huid': '11LsCBRSYcm8JZy3PLQtwO5B%2FsH6Rt7nXWW8SGFdzo76Y%3D', ' __sid': '9114931.3092967026862794000.1628751059996.384', ' search_last_sid': '', ' search_last_kw': 'python', ' count': '55', ' monitor_count': '55', ' __gid': '9114931.125088310.1628738227260.1628760208559.561\n'}

        self.detail_cookie = {'gtHuid': '1', ' test_cookie_enable': 'null',
                              ' erules': 'p2-15%7Cecl-2%7Ckd-1%7Cp1-3%7Cp3-2',
                              ' __guid': '9114931.2302920673738409000.1628738227035.168', ' __autoShowTip': 'show',
                              ' WDTKID': 'fa1d06b3d3617943',
                              ' __huid': '11LsCBRSYcm8JZy3PLQtwO5B%2FsH6Rt7nXWW8SGFdzo76Y%3D',
                              ' __sid': '9114931.3809253806408311000.1628747656032.3743', ' count': '22',
                              ' monitor_count': '22', ' __gid': '9114931.125088310.1628738227260.1628748245657.71'}

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


        self.headers = {"Host": "wenda.so.com",
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
        tmp_url = "https://wenda.so.com/search/?q={}&pn={}"
        cfg["search_url"] = tmp_url
        tmp_url = tmp_url.format(urllib.parse.quote(cfg["keyword"]),cfg["total_page"])


        self.logger.info("site_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers,cookies=self.cookie_data)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):

        cfg = response.meta["cfg"]

        list_data = response.xpath("//*[@id=\"js-qa-list\"]/li[@class=\"item js-normal-item\"]")
        a = 1
        for data in list_data:
            a+=1

            list_item={}
            list_item["answer_url"] = urljoin(self.index_url,"".join(data.xpath("./div[1]/h3/a/@href").extract()))
            list_item["title"] = "".join(data.xpath("./div[1]/h3/a//text()").extract()).strip()
            publish_time = "".join(data.xpath("./div[3]/text()").extract())
            list_item["publish_time"] = str_to_timestamp(publish_time)
            comment_num = "".join(data.xpath("./div[3]/text()").extract())

            list_item["comment_num"] = "".join(re.findall("- (\d+)个回答",comment_num))
            if len(list_item["comment_num"])>0:
                list_item["comment_num"] = int(list_item["comment_num"])
            else:
                list_item["comment_num"] = 0

            md5_url = Get_md5(list_item["answer_url"])
            list_item["md5_url"] = md5_url
            list_item["root_id"] ="".join(re.findall("https://wenda.so.com/q/(\d+)",list_item["answer_url"]))

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, list_item["root_id"])
            if (isExist):
                continue
            self.detail_headers["Referer"] = response.url
            request = scrapy.Request(list_item["answer_url"], callback=self.detail_parse, headers=self.detail_headers, cookies=self.detail_cookie,dont_filter=True)
            request.meta["list_item"] = copy.deepcopy(list_item)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request

        next_data = "".join(response.xpath("//*[@id=\"qaresult-page\"]/p/a[@class=\"next\"]/@href").extract())
        next_page= urljoin(self.index_url,next_data)
        if len(next_data)>0:
            tmp_url = next_page
            print("tmp_url", tmp_url)
            self.logger.info("site_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers, cookies=self.cookie_data)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request


    def detail_parse(self,response):

        # print(response.body)
        page = response.body
        page = page.decode("gbk", 'ignore')
        list_item = response.meta["list_item"]
        cfg = response.meta["cfg"]
        item = Questionsanswers_searchItem()
        item.init()
        item["keyword"] = cfg["keyword"]
        item["media_name"] = cfg["site_name"]
        item["media_id"] = cfg["site_id"]

        item["author_id"] = "".join(
            response.xpath("//div[@class=\"question-info\"]/a[1]/@index").extract())
        item["author_img"] = "".join(
            response.xpath("//div[@class=\"question-info\"]/a[1]/img/@src").extract())
        item["author_screen_name"] = "".join(
            response.xpath("//div[@class=\"question-info\"]/a[2]/text()").extract())
        # 标题

        # 标题
        item["title"] = list_item["title"]
        # 悬赏数
        reward_number = int("".join(response.xpath("//h1//i/text()").extract()))

        extra_info_data = {}
        extra_info_data["reward_number"] = reward_number
        extra_info = json.dumps(extra_info_data,ensure_ascii=False)
        item["extra_info"] = extra_info

        item["gather_time"] = int(time.time())*1000
        item["publish_time"] = list_item["publish_time"]
        item["update_time"] = item["gather_time"]

        # 阅读数
        views_count = "".join(response.xpath("//div[@class=\"question-info\"]/span[2]/text()").extract())
        views_count = re.sub("浏览","",views_count)
        item["views_count"] = int(re.sub("次", "", views_count))
        # 标签
        item["tags"] = []
        # 回答数
        item["comments_count"] = list_item["comment_num"]
        item["md5"] = list_item["md5_url"]
        item["url"] = response.url.split("?")[0]
        item["root_id"] = list_item["root_id"]
        content = "".join(response.xpath("//div[@class=\"question\"]/div[@class=\"question-content\"]//text()").extract())
        content = re.sub("\n\n", "\n", content)
        item["content"] = content
        images = []
        images_data = response.xpath("//div[@class=\"question\"]/div[@class=\"question-content\"]//img/@src").extract()
        for image in images_data:

            images.append(image)
        item["picture_urls"] = images

        self.logger.info("media_id=%s,id=%s" % (item["media_id"],item["root_id"]))
        comments_data = {}
        comments_data["comments_count"] = item["comments_count"]
        comments_data["comment_index"] = False
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL,self.DUP_CHANNEL, item["root_id"],params)

        yield item