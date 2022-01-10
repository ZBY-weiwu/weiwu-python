import scrapy
import os
import json
import copy
import re
import time
import urllib.parse
from urllib.parse import urljoin
import configparser
import requests
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

def get_detailurl(url):
    headers = {"Host": "www.sogou.com",
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
               "Accept-Language": "zh-CN,zh;q=0.9",
               "Cookie": "ABTEST=0|1628850669|v17; SNUID=A067F9323236FB5C6BB8E2E2334C343A; IPLOC=CN1100; SUID=9255CA016555A00A00000000611649ED; SUV=1628850670109804; ld=8kllllllll2PV6XHlllllp9QvKylllllltIq6kllllwlllllRylll5@@@@@@@@@@"}


    resp = requests.get(url, headers=headers)
    url_data = "".join(re.findall("replace\(\"(.*?)\"\)</script>", resp.text))
    return url_data


class sougouwenda_search_Spider():
    def __init__(self):
        print("sougouwenda_search_Spider")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://www.sogou.com/sogou"
        self.cookie_data = {'IPLOC': 'CN1100', ' SUID': '9255CA011431A40A0000000060D18B85', ' SUV': '1624345477282507', ' ssuid': '5385277170', ' Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c': '1624345478,1624501403,1624868105', ' sw_uuid': '7107154944', ' ABTEST': '3|1628822255|v17', ' sg_mu': '1188735892', ' sg_lu': '693912151-b2xOTlR3YU03M0VTYmZfUWZEcllZS1pNTmV1RQ..', ' sg_uname': '%40', ' sg_upic': 'https%3A%2F%2Fthirdwx.qlogo.cn%2Fmmopen%2Fvi_32%2FQ0j4TwGTfTLcAEmPg0ohKfywCEPiaAh79D66b0NBRaC6KPjAEfK50DCpSFkL6ibtWMgWGd0B7f5rxgPgLTqOH8oA%2F132', ' sg_uuid': '7215477986', ' SNUID': '9054CB000107C86E9123351902CB85CD', ' taspeed': 'taspeedexist', ' pid': 'ww.fly.11', ' ss_pidf': '1', ' ld': 'Qkllllllll2PVAZOlllllp9QymtlllllltIq6kllll6lllllRylll5@@@@@@@@@@', ' LSTMV': '0%2C221', ' LCLKINT': '7210\n'}

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
                        "Accept-Language": "zh-CN,zh;q=0.9",
                        "Cookie": "ABTEST=0|1628850669|v17; SNUID=A067F9323236FB5C6BB8E2E2334C343A; IPLOC=CN1100; SUID=9255CA016555A00A00000000611649ED; SUV=1628850670109804; ld=8kllllllll2PV6XHlllllp9QvKylllllltIq6kllllwlllllRylll5@@@@@@@@@@"}



        self.logger = get_logger('wenda', logger_path)
        # self.page = 0


    def formatEntryUrl(self,cfg):
        cfg["total_page"]+=1
        tmp_url = "https://www.sogou.com/sogou?query={}&insite=wenwen.sogou.com&page={}"
        cfg["search_url"] = tmp_url
        tmp_url = tmp_url.format(urllib.parse.quote(cfg["keyword"]),cfg["total_page"])

        self.logger.info("site_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers,cookies=self.cookie_data)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):

        cfg = response.meta["cfg"]

        list_data = response.xpath("//div[@class=\"results\"]/div[@class=\"vrwrap\"]")
        print("list_data",list_data)
        a = 1
        for data in list_data:
            a+=1

            list_item={}
            # print("url:","".join(data.xpath("./h3[@class=\"vrTitle\"]/a/@href").extract()))
            list_item["answer_url"] = urljoin(self.index_url,"".join(data.xpath("./h3[@class=\"vrTitle\"]/a/@href").extract()))
            list_item["answer_url"] =self.get_detailurl(list_item["answer_url"])
            list_item["title"] = "".join(data.xpath("./h3[@class=\"vrTitle\"]//text()").extract()).strip()
            publish_time = "".join(data.xpath("./p[@class=\"str_time\"]/text()").extract())
            list_item["publish_time"] = str_to_timestamp(publish_time)
            comment_num = "".join(data.xpath("./p[@class=\"str_time\"]/text()").extract())

            list_item["comment_num"] = "".join(re.findall("(\d+)个答案",comment_num))
            if len(list_item["comment_num"])>0:
                list_item["comment_num"] = int(list_item["comment_num"])
            else:
                list_item["comment_num"] = 0

            likes_count = "".join(data.xpath("./p[@class=\"str_time\"]/text()").extract())
            print("likes_count",likes_count)
            try:
                likes_count = int("".join(re.findall("(\d+)个赞 ",likes_count)))
            except:
                likes_count=0
            list_item["likes_count"] = likes_count
            md5_url = Get_md5(list_item["answer_url"])
            list_item["md5_url"] = md5_url
            list_item["root_id"] = "".join(re.findall("https://wenwen.sogou.com/z/(q\d+).htm",list_item["answer_url"]))
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, md5_url)
            if (isExist):
                continue
            # self.detail_headers["Referer"] = response.url

            request = scrapy.Request(list_item["answer_url"], callback=self.detail_parse, headers=self.detail_headers, cookies=self.detail_cookie)
            # request = scrapy.Request(list_item["answer_url"], callback=self.detail_parse, headers=self.headers,dont_filter=True)
            request.meta["list_item"] = copy.deepcopy(list_item)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request


        next_data = "".join(response.xpath("//*[@id=\"sogou_next\"]/@href").extract())
        next_page= urljoin(self.index_url,next_data)
        if len(next_data)>0:
            tmp_url = next_page
            print("tmp_url", tmp_url)
            self.logger.info("site_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
            # request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers, cookies=self.cookie_data)
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers)
            request.meta['cfg'] = copy.deepcopy(cfg)

            yield request

    def get_detailurl(self,url):
        headers = {"Host": "www.sogou.com",
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
                   "Accept-Language": "zh-CN,zh;q=0.9",
                   "Cookie": "ABTEST=0|1628850669|v17; SNUID=A067F9323236FB5C6BB8E2E2334C343A; IPLOC=CN1100; SUID=9255CA016555A00A00000000611649ED; SUV=1628850670109804; ld=8kllllllll2PV6XHlllllp9QvKylllllltIq6kllllwlllllRylll5@@@@@@@@@@"}

        resp = requests.get(url, headers=headers)
        url_data = "".join(re.findall("replace\(\"(.*?)\"\)</script>", resp.text))
        return url_data

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

        # 标题
        item["title"] = list_item["title"]
        # 悬赏数
        reward_number = 0

        extra_info_data = {}
        extra_info_data["reward_number"] = reward_number
        extra_info = json.dumps(extra_info_data,ensure_ascii=False)
        item["extra_info"] = extra_info

        item["gather_time"] = int(time.time())*1000
        item["publish_time"] = list_item["publish_time"]
        item["update_time"] = item["gather_time"]

        # 阅读数

        item["views_count"] = 0
        # 标签
        item["tags"] = response.xpath("//div[@class=\"tags\"]/a/text()").extract()
        # 回答数
        item["comments_count"] = list_item["comment_num"]
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
        self.logger.info("media_id=%s,id=%s" % (item["media_id"],item["root_id"]))
        comments_data = {}
        comments_data["comments_count"] = item["comments_count"]
        comments_data["comment_index"] = False
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["root_id"], params)
        yield item

