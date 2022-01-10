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

class Baiduzhidao_search_Spider():
    def __init__(self):
        print("baiduwenda_search")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://zhidao.baidu.com"
        self.cookie_data = {'BIDUPSID': 'EAC73AF735E21F0CD8E38B2450D35165', ' PSTM': '1622612033', ' BAIDUID': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1', ' BDUSS': 'jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN', ' BDUSS_BFESS': 'jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN', ' __yjs_duid': '1_4b51fe5680eb2b4c1233ff30196299da1622619657966', ' PREV_DAILY_PERIOD': '2897', ' BDSFRCVID_BFESS': 'lyPOJeC62C5o3ZJHLSIiEXcive50oYTTH6aoW1C7_ZTvVgAxsqEyEG0P8f8g0KubGvTAogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5', ' H_BDCLCKID_SF_BFESS': 'tbue_II5JIP3qn7I5-Oo5P6HbxoXK-JqHD7XVh_Kbp7keqOzyb7cDjLvM4AjXUbU3Gb2B4QHWhk2ep72y-vSh6OyWhJ0QtoaLD6C-qcH0KQpsIJM5-DWbT8U5f5mLbQGaKviaKJjBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6obDaDfqTDef573BR6OHJTVbp6aLUnkbfJBDGJC5RTTK2bUW4823xnjjtQHBU55LnK7yajK2-P8-b6Z-x7LQPcrstchD4QpQT8rBUDOK5OibCrp5Rcgab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_efnCe_C_Qb-3bK4Jpb-OSbJ8_bMOQKC6y-DkX3buQfU7r8pcNLTDKh5OWhh5IBUjrQbR4hnOVbJct8f8wylO1j4_P2q8q5tRI2D5gVnRjbxJbDl5jDh31b6ksD-RteltH366y0hvctn6cShnCqfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNLqJ5_ftnAsL-35HtbEHJrlMtr2q4tehHRQhlO9WDTm_DonJRA5olcSXhbzMfLR-UrqK6Ljaa5n-pPKKR7Rhq86Bp6x5lKsLq7ebxQ83mkjbInDfn02OP5PQnjxLt4syP4j2xRnWTFLKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8ZDTLBj63P', ' MCITY': '-131%3A', ' IK_FORCE_UHOME': '0', ' BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598', ' shitong_key_id': '2', ' BAIDUID_BFESS': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1', ' cflag': '13%3A3', ' BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0', ' delPer': '0', ' PSINO': '1', ' H_PS_PSSID': '34401_34380_34363_31660_34403_34004_34073_34092_34106_34111_26350_34323_34306', ' BA_HECTOR': 'a18k042h85akaka5d11gh79ln0q', ' Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925': '1628564765,1628570962,1628591087,1628678929', ' Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c': '1628564765,1628570962,1628591088,1628678930', ' ZD_ENTRY': 'empty', ' ab_sr': '1.0.1_MzFjYTE1MzFmODMyNDBlZDhjMjEwY2Y4MTM2ZDQ2MWU3ZWRkM2UzNWU2NWNiOWVjMzkzZjY5ZGRlMzhlMzE2ODg5NDZjMmNhNDM3ZmZjNzE3YWJlYzNjMDAyMTQyMzNjNTJlMDQxMmRhOWU0YjVhYjBjNDkwMDM5ZTljZGEyMzY1Y2NlOTJlZTA4ZWQzMWNhMjc3YTQxNzNmYjM0MDNhNzE1OWZlZmM4MTZlNTlkNzk4NTkzOGNlZjU2MmM2YTVj', ' Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925': '1628680170', ' shitong_data': '82da467dfa4d7cf4e952a2fd6cd79a89c93647c37456fb06484cc3e1a9867bb7892a8b7b05583801069c2fd683b05abd42312a7a18ecae51a90f674bc6b0ddbc6a06b0e70f747f2b0879caf2023a82954b830608b0ba0a7fc583e6e41096add91c1cb578b5b5697aa08ba7f6a560b243f19b2e1c9ddbff61f13f394dbb0b845a', ' shitong_sign': '03cbe2c4', ' Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c': '1628680170'}
        self.detail_cookie ={' BAIDUID': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1'}
        self.detail_headers = {"Host": "zhidao.baidu.com",
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


        self.headers = {"Host": "zhidao.baidu.com",
                        "Connection": "keep-alive",
                        "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                        "sec-ch-ua-mobile": "?0",
                        "Upgrade-Insecure-Requests": "1",
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                        "Sec-Fetch-Site": "same-origin",
                        "Sec-Fetch-Mode": "navigate",
                        "Sec-Fetch-User": "?1",
                        "Sec-Fetch-Dest": "document",
                        "Referer": "https://zhidao.baidu.com/",
                        "Accept-Language": "zh-CN,zh;q=0.9"}

        self.logger = get_logger('wenda', logger_path)


    def formatEntryUrl(self,cfg):
        tmp_url = "https://zhidao.baidu.com/search?word={}&pn={}"
        cfg["search_url"] = tmp_url
        tmp_url = tmp_url.format(urllib.parse.quote(cfg["keyword"]),cfg["total_page"])

        self.logger.info("site_id=%s,entry_url=%s" % (cfg["site_id"], tmp_url))
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers,cookies=self.cookie_data)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):

        cfg = response.meta["cfg"]
        # cfg["total_page"]+=1

        list_data = response.xpath("//*[@id=\"wgt-list\"]/dl")
        a = 1
        for data in list_data:
            a+=1

            list_item={}
            list_item["answer_url"] = "".join(data.xpath("./dt/a/@href").extract()).split("?")[0]
            list_item["answer_url"] = list_item["answer_url"].replace("http","https")
            list_item["update_time"] = str_to_timestamp("".join(data.xpath("./dd[2]/span[1]/text()").extract()))
            list_item["comment_num"] = "".join(data.xpath("./dd[3]/span[3]//text()").extract())
            if len(list_item["comment_num"])>0:

                list_item["comment_num"]  = int(re.sub("个回答","",list_item["comment_num"]).strip())
            else:
                list_item["comment_num"] = 0

            list_item["like_num"] = "".join(data.xpath("./dd[3]/span[4]/text()").extract()).strip()
            if len(list_item["like_num"]) > 0:
                list_item["like_num"] = int(list_item["like_num"])

            else:
                list_item["like_num"] =0
                # next_page_url = next_page

            md5_url = Get_md5(list_item["answer_url"])
            list_item["md5_url"] = md5_url
            list_item["root_id"] = "".join(re.findall("https://zhidao\.baidu\.com/question/(\d+)\.html",list_item["answer_url"]))
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, list_item["root_id"])
            if (isExist):
                continue
            self.detail_headers["Referer"] = "https://zhidao.baidu.com/"
            request = scrapy.Request(list_item["answer_url"], callback=self.detail_parse, headers=self.detail_headers, cookies=self.detail_cookie,dont_filter=True)
            request.meta["list_item"] = copy.deepcopy(list_item)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
        next_page = urljoin(self.index_url,"".join(response.xpath("//a[@class=\"pager-next\"]/@href").extract()))
        if len(next_page)>0:
            tmp_url = next_page
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
        # 标题
        item["title"] = "".join(response.xpath("//h1/span[@class=\"ask-title\"]/text()").extract())

        # 悬赏数
        try:
            reward_number = int("".join(response.xpath("//h1/span[@class=\"ask-wealth\"]/em/text()").extract()))
        except:
            reward_number = 0
        # 扩展字段
        extra_info_data = {}
        extra_info_data["reward_number"] = reward_number
        extra_info = json.dumps(extra_info_data,ensure_ascii=False)

        item["extra_info"] = extra_info

        item["gather_time"] = int(time.time())*1000
        item["update_time"] = int(list_item["update_time"])*1000
        item["publish_time"] = item["update_time"]
        # 标签
        item["tags"] = []
        # 回答数
        item["comments_count"] = list_item["comment_num"]

        item["md5"] = list_item["md5_url"]
        item["url"] = response.url.split("?")[0]
        try:
            item["root_id"] = "".join(re.findall("https://zhidao\.baidu\.com/question/(\d+)\.html",response.url))
        except:
            return
        content = "".join(response.xpath("//*[@id=\"wgt-ask\"]/div[1]//text()").extract())
        content = re.sub("\n展开", "", content)
        content = re.sub("\n\n", "\n", content)
        item["content"] = content
        images = []
        images_data = response.xpath("//*[@id=\"wgt-ask\"]/div[3]/div/ul/li/div[@class=\"q-img-item-box\"]").extract()
        for image in images_data:
            image = re.sub("background-image: url\(", "", image)
            image = re.sub("\)", "", image)
            images.append(image)
        item["picture_urls"] = images
        self.logger.info("media_id=%s,id=%s" % (cfg["site_id"], item["root_id"]))
        comments_data = {}
        comments_data["comments_count"] = item["comments_count"]
        comments_data["comment_index"] = False
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL,self.DUP_CHANNEL, item["root_id"],params)
        yield item

