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
# from Tools.dupClient import DUPClient
# from Tools.wenda_package import get_logger,str_to_timestamp,timeStamp_data
# from Tools.wenda_package import get_logger,Get_md5
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


class Baiduzhidao_Spider():
    def __init__(self):
        print("baiduwenda")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        self.index_url = "https://zhidao.baidu.com"
        # self.cookie_data = {"BAIDUID":"DC004BE9E557DCA2CE1FD6542FAD4207:FG=1;"}
        self.cookie_data = {"Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"}
        self.detail_cookie ={'BIDUPSID': 'EAC73AF735E21F0CD8E38B2450D35165', ' PSTM': '1622612033', ' BAIDUID': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1', ' BDUSS': 'jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN', ' BDUSS_BFESS': 'jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN', ' __yjs_duid': '1_4b51fe5680eb2b4c1233ff30196299da1622619657966', ' PREV_DAILY_PERIOD': '2897', ' shitong_key_id': '2', ' delPer': '0', ' BAIDUID_BFESS': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1', ' BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0', ' PSINO': '1', ' BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598', ' H_PS_PSSID': '34401_34380_34363_31660_34403_34004_34073_34092_34106_34111_26350_34306', ' BA_HECTOR': '2501ahak2g0l80a5tb1gh3ppb0r', ' BCLID': '7782616907397801223', ' BDSFRCVID': 'lyPOJeC62C5o3ZJHLSIiEXcive50oYTTH6aoW1C7_ZTvVgAxsqEyEG0P8f8g0KubGvTAogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5', ' H_BDCLCKID_SF': 'tbue_II5JIP3qn7I5-Oo5P6HbxoXK-JqHD7XVh_Kbp7keqOzyb7cDjLvM4AjXUbU3Gb2B4QHWhk2ep72y-vSh6OyWhJ0QtoaLD6C-qcH0KQpsIJM5-DWbT8U5f5mLbQGaKviaKJjBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6obDaDfqTDef573BR6OHJTVbp6aLUnkbfJBDGJC5RTTK2bUW4823xnjjtQHBU55LnK7yajK2-P8-b6Z-x7LQPcrstchD4QpQT8rBUDOK5OibCrp5Rcgab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_efnCe_C_Qb-3bK4Jpb-OSbJ8_bMOQKC6y-DkX3buQfU7r8pcNLTDKh5OWhh5IBUjrQbR4hnOVbJct8f8wylO1j4_P2q8q5tRI2D5gVnRjbxJbDl5jDh31b6ksD-RteltH366y0hvctn6cShnCqfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNLqJ5_ftnAsL-35HtbEHJrlMtr2q4tehHRQhlO9WDTm_DonJRA5olcSXhbzMfLR-UrqK6Ljaa5n-pPKKR7Rhq86Bp6x5lKsLq7ebxQ83mkjbInDfn02OP5PQnjxLt4syP4j2xRnWTFLKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8ZDTLBj63P', ' BCLID_BFESS': '7782616907397801223', ' BDSFRCVID_BFESS': 'lyPOJeC62C5o3ZJHLSIiEXcive50oYTTH6aoW1C7_ZTvVgAxsqEyEG0P8f8g0KubGvTAogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5', ' H_BDCLCKID_SF_BFESS': 'tbue_II5JIP3qn7I5-Oo5P6HbxoXK-JqHD7XVh_Kbp7keqOzyb7cDjLvM4AjXUbU3Gb2B4QHWhk2ep72y-vSh6OyWhJ0QtoaLD6C-qcH0KQpsIJM5-DWbT8U5f5mLbQGaKviaKJjBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6obDaDfqTDef573BR6OHJTVbp6aLUnkbfJBDGJC5RTTK2bUW4823xnjjtQHBU55LnK7yajK2-P8-b6Z-x7LQPcrstchD4QpQT8rBUDOK5OibCrp5Rcgab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_efnCe_C_Qb-3bK4Jpb-OSbJ8_bMOQKC6y-DkX3buQfU7r8pcNLTDKh5OWhh5IBUjrQbR4hnOVbJct8f8wylO1j4_P2q8q5tRI2D5gVnRjbxJbDl5jDh31b6ksD-RteltH366y0hvctn6cShnCqfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNLqJ5_ftnAsL-35HtbEHJrlMtr2q4tehHRQhlO9WDTm_DonJRA5olcSXhbzMfLR-UrqK6Ljaa5n-pPKKR7Rhq86Bp6x5lKsLq7ebxQ83mkjbInDfn02OP5PQnjxLt4syP4j2xRnWTFLKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8ZDTLBj63P', ' ZD_ENTRY': 'baidu', ' cflag': '13%3A3', ' Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925': '1628482558,1628564731,1628564752,1628564765', ' Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c': '1628482559,1628564732,1628564752,1628564765', ' Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925': '1628564801', ' ab_sr': '1.0.1_N2UxYzg0NDU3YzZlMDA1Y2VlODEyNzRiYzgzMTI4YWFjYTVlNjFkMmU1NzQ4Zjg5OWM0ZTAzNGY4Y2RjMTI0YWE1NTZlYjM0MzhmYTgxZTJjOWEwOTM2YTcyNjNjNjBhOWI2MDg0YTViMGNkYzg2MzBhMzYzYzdiODhiZTFhOTgxMjVlYjUyODAxZjczZjUxYjNmM2IzYWIyOTMxOTMwMzE2N2M3ZjA1NmJjZTkzYTFjMTczMjgzNmQ2MTI4MTEz', ' shitong_data': '82da467dfa4d7cf4e952a2fd6cd79a89c93647c37456fb06484cc3e1a9867bb7892a8b7b05583801069c2fd683b05abd42312a7a18ecae51a90f674bc6b0ddbc6a06b0e70f747f2b0879caf2023a82954b830608b0ba0a7fc583e6e41096add91d4299e61253bb18fe8016c9cf97353c5f49e5b671b977242723447b1b4a4ff5', ' shitong_sign': '6f040207', ' Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c': '1628564803'}
        self.detail_headers = {"Host": "zhidao.baidu.com", "Connection": "keep-alive", "Cache-Control": "max-age=0", "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"", "sec-ch-ua-mobile": "?0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Referer": "https://zhidao.baidu.com/list?category=%E5%A8%B1%E4%B9%90%E4%BC%91%E9%97%B2&fr=daohang", "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9"}

        # self.headers = {"User-Agent": ua.chrome}
        self.headers = {"Host": "zhidao.baidu.com",
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
                        "Accept-Language": "zh-CN,zh;q=0.9"
                        }


        # "Cookie": "BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591"
        # BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BAIDUID=EAC73AF735E21F0C4DF7F8A03A75A591
        self.logger = get_logger('wenda', logger_path)
        # self.page = 0


    def formatEntryUrl(self,cfg):

        tmp_url = cfg["board_url"]+"&rn=40&pn={}"+"&ie=utf8&_pjax=%23j-question-list-pjax-container"
        tmp_url = tmp_url.format(urllib.parse.quote(cfg["config"]),cfg["total_page"])
        # tmp_url = "https://zhidao.baidu.com/list?category=%E5%A8%B1%E4%B9%90%E4%BC%91%E9%97%B2"
        # print("tmp_url",tmp_url)

        self.logger.info("board_id=%s,entry_url=%s" % (cfg["board_id"], tmp_url))

        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.headers,cookies=self.cookie_data)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):
        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        page = response.body
        # try:
        #     page = page.decode("utf-8").encode("utf8")
        # except:
        #     page = page.decode("gbk", 'ignore').encode("utf8")
        page = page.decode("gbk", 'ignore')


        list_xpath = response.xpath("//*[@id=\"j-question-list-pjax-container\"]/div/ul[@class=\"question-list-ul\"]/li")
        count_data = len(list_xpath)
        a = 1
        for data in list_xpath:
            a+=1
            list_item = {}
            # 问题
            list_item["question"] = "".join(data.xpath("./div[1]/div[@class=\"question-title\"]/a/text()").extract())
            list_item["question"] = list_item["question"].strip()

            # 悬赏
            try:
                list_item["reward_number"] = int("".join(data.xpath("./div[1]/div[@class=\"question-title\"]/span[@class=\"coin-count\"]/text()").extract()))
            except:
                list_item["reward_number"] =0

            # 发布时间
            list_item["pt"] = str_to_timestamp("".join(data.xpath("./div[1]/div[@class=\"question-info\"]/div[@class=\"question-time\"]/text()").extract()))

            # 所属标签
            question_tags = data.xpath("./div[1]/div[@class=\"question-tags\"]/a/text()").extract()
            list_item["question_tags"] = [i.strip() for i in question_tags]

            # 回答数
            list_item["answer_num"] = "".join(data.xpath("./div[1]/div[@class=\"question-info\"]/div[@class=\"answer-num\"]/text()").extract())
            list_item["answer_num"] = list_item["answer_num"].strip()
            list_item["answer_num"] = re.sub("回答","",list_item["answer_num"]).strip()

            #详情页链接
            list_item["answer_url"] = urljoin(self.index_url,"".join(data.xpath("./div[1]/div[@class=\"question-title\"]/a/@href").extract()))

            md5_url = Get_md5(list_item["answer_url"])
            list_item["root_id"] = "".join(re.findall("https://zhidao\.baidu\.com/question/(\d+)\.html",list_item["answer_url"]))
            list_item["md5_url"] = md5_url
            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, list_item["root_id"])
            print("find and set ,",list_item["root_id"])
            if (isExist):
                print("exist one item:",list_item["root_id"])
                continue
            self.detail_headers["Referer"] = response.url
            request = scrapy.Request(list_item["answer_url"], callback=self.detail_parse, headers=self.detail_headers, cookies=self.detail_cookie)
            request.meta["list_item"] = copy.deepcopy(list_item)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
        if count_data>0 and 10>cfg["total_page"]:
            tmp_url = cfg["board_url"] + "&rn=40&pn={}" + "&ie=utf8&_pjax=%23j-question-list-pjax-container"
            tmp_url = tmp_url.format(urllib.parse.quote(cfg["config"]), cfg["total_page"])

            self.logger.info("board_id=%s,entry_url=%s" % (cfg["board_id"], tmp_url))
            request = scrapy.Request(tmp_url, callback=self.parse, headers=self.headers, cookies=self.cookie_data)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request


    def detail_parse(self,response):
        # print(response.body)
        list_item = response.meta["list_item"]
        cfg = response.meta["cfg"]
        item = QuestionsanswersItem()
        item.Init()
        item["board_id"] = cfg["board_id"]
        item["board_name"] = cfg["board_name"]
        item["media_name"] = cfg["site_name"]
        item["media_id"] = cfg["site_id"]
        # 标题
        item["title"] = list_item["question"]
        # 悬赏数
        reward_number = list_item["reward_number"]

        extra_info_data = {}
        extra_info_data["reward_number"] = reward_number
        extra_info = json.dumps(extra_info_data,ensure_ascii=False)
        item["extra_info"] = extra_info

        item["gather_time"] = int(time.time())*1000
        item["publish_time"] = int(list_item["pt"])*1000
        item["update_time"] = int(list_item["pt"]) * 1000
        # 标签
        item["tags"] = list_item["question_tags"]
        # 回答数
        item["comments_count"] = list_item["answer_num"]
        item["md5"] = list_item["md5_url"]
        item["url"] = response.url.split("?")[0]
        item["root_id"] = list_item["root_id"]
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
        # print(json.dumps(item,ensure_ascii=False))
        self.logger.info("board_id=%s,id=%s" % (item["board_id"], item["root_id"]))
        comments_data = {}
        try:
            comments_data["comments_count"] = int(item["comments_count"])
        except:
            comments_data["comments_count"] = 0
        comments_data["comment_index"] = False
        params = json.dumps(comments_data)
        dupClient.confirm(self.DUP_URL,self.DUP_CHANNEL, item["root_id"],params)
        print("confirm target,",item['root_id'])

        yield item

