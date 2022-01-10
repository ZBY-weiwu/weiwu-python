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


class Baiduzhidao_comment_Spider():
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
        self.detail_cookie = {'BIDUPSID': 'EAC73AF735E21F0CD8E38B2450D35165', ' PSTM': '1622612033',
                              ' BAIDUID': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1',
                              ' BDUSS': 'jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN',
                              ' BDUSS_BFESS': 'jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN',
                              ' __yjs_duid': '1_4b51fe5680eb2b4c1233ff30196299da1622619657966',
                              ' PREV_DAILY_PERIOD': '2897', ' shitong_key_id': '2', ' delPer': '0',
                              ' BAIDUID_BFESS': 'EAC73AF735E21F0C4DF7F8A03A75A591:FG=1',
                              ' BDRCVFR[feWj1Vr5u3D]': 'I67x6TjHwwYf0', ' PSINO': '1',
                              ' BDORZ': 'B490B5EBF6F3CD402E515D22BCDA1598',
                              ' H_PS_PSSID': '34401_34380_34363_31660_34403_34004_34073_34092_34106_34111_26350_34306',
                              ' BA_HECTOR': '2501ahak2g0l80a5tb1gh3ppb0r', ' BCLID': '7782616907397801223',
                              ' BDSFRCVID': 'lyPOJeC62C5o3ZJHLSIiEXcive50oYTTH6aoW1C7_ZTvVgAxsqEyEG0P8f8g0KubGvTAogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5',
                              ' H_BDCLCKID_SF': 'tbue_II5JIP3qn7I5-Oo5P6HbxoXK-JqHD7XVh_Kbp7keqOzyb7cDjLvM4AjXUbU3Gb2B4QHWhk2ep72y-vSh6OyWhJ0QtoaLD6C-qcH0KQpsIJM5-DWbT8U5f5mLbQGaKviaKJjBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6obDaDfqTDef573BR6OHJTVbp6aLUnkbfJBDGJC5RTTK2bUW4823xnjjtQHBU55LnK7yajK2-P8-b6Z-x7LQPcrstchD4QpQT8rBUDOK5OibCrp5Rcgab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_efnCe_C_Qb-3bK4Jpb-OSbJ8_bMOQKC6y-DkX3buQfU7r8pcNLTDKh5OWhh5IBUjrQbR4hnOVbJct8f8wylO1j4_P2q8q5tRI2D5gVnRjbxJbDl5jDh31b6ksD-RteltH366y0hvctn6cShnCqfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNLqJ5_ftnAsL-35HtbEHJrlMtr2q4tehHRQhlO9WDTm_DonJRA5olcSXhbzMfLR-UrqK6Ljaa5n-pPKKR7Rhq86Bp6x5lKsLq7ebxQ83mkjbInDfn02OP5PQnjxLt4syP4j2xRnWTFLKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8ZDTLBj63P',
                              ' BCLID_BFESS': '7782616907397801223',
                              ' BDSFRCVID_BFESS': 'lyPOJeC62C5o3ZJHLSIiEXcive50oYTTH6aoW1C7_ZTvVgAxsqEyEG0P8f8g0KubGvTAogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0f5',
                              ' H_BDCLCKID_SF_BFESS': 'tbue_II5JIP3qn7I5-Oo5P6HbxoXK-JqHD7XVh_Kbp7keqOzyb7cDjLvM4AjXUbU3Gb2B4QHWhk2ep72y-vSh6OyWhJ0QtoaLD6C-qcH0KQpsIJM5-DWbT8U5f5mLbQGaKviaKJjBMb1MlvDBT5h2M4qMxtOLR3pWDTm_q5TtUJMeCnTDMFhe6obDaDfqTDef573BR6OHJTVbp6aLUnkbfJBDGJC5RTTK2bUW4823xnjjtQHBU55LnK7yajK2-P8-b6Z-x7LQPcrstchD4QpQT8rBUDOK5OibCrp5Rcgab3vOIJzXpO15CuzBN5thURB2DkO-4bCWJ5TMl5jDh3Mb6ksD-Ftqj_efnCe_C_Qb-3bK4Jpb-OSbJ8_bMOQKC6y-DkX3buQfU7r8pcNLTDKh5OWhh5IBUjrQbR4hnOVbJct8f8wylO1j4_P2q8q5tRI2D5gVnRjbxJbDl5jDh31b6ksD-RteltH366y0hvctn6cShnCqfjrDRLbXU6BK5vPbNcZ0l8K3l02V-bIe-t2XjQhDNLqJ5_ftnAsL-35HtbEHJrlMtr2q4tehHRQhlO9WDTm_DonJRA5olcSXhbzMfLR-UrqK6Ljaa5n-pPKKR7Rhq86Bp6x5lKsLq7ebxQ83mkjbInDfn02OP5PQnjxLt4syP4j2xRnWTFLKfA-b4ncjRcTehoM3xI8LNj405OTbIFO0KJDJCcjqR8ZDTLBj63P',
                              ' ZD_ENTRY': 'baidu', ' cflag': '13%3A3',
                              ' Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925': '1628482558,1628564731,1628564752,1628564765',
                              ' Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c': '1628482559,1628564732,1628564752,1628564765',
                              ' Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925': '1628564801',
                              ' ab_sr': '1.0.1_N2UxYzg0NDU3YzZlMDA1Y2VlODEyNzRiYzgzMTI4YWFjYTVlNjFkMmU1NzQ4Zjg5OWM0ZTAzNGY4Y2RjMTI0YWE1NTZlYjM0MzhmYTgxZTJjOWEwOTM2YTcyNjNjNjBhOWI2MDg0YTViMGNkYzg2MzBhMzYzYzdiODhiZTFhOTgxMjVlYjUyODAxZjczZjUxYjNmM2IzYWIyOTMxOTMwMzE2N2M3ZjA1NmJjZTkzYTFjMTczMjgzNmQ2MTI4MTEz',
                              ' shitong_data': '82da467dfa4d7cf4e952a2fd6cd79a89c93647c37456fb06484cc3e1a9867bb7892a8b7b05583801069c2fd683b05abd42312a7a18ecae51a90f674bc6b0ddbc6a06b0e70f747f2b0879caf2023a82954b830608b0ba0a7fc583e6e41096add91d4299e61253bb18fe8016c9cf97353c5f49e5b671b977242723447b1b4a4ff5',
                              ' shitong_sign': '6f040207', ' Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c': '1628564803'}

        self.detail_headers = {"Host": "zhidao.baidu.com", "Connection": "keep-alive", "Cache-Control": "max-age=0",
                               "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                               "sec-ch-ua-mobile": "?0", "Upgrade-Insecure-Requests": "1",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                               "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                               "Sec-Fetch-Dest": "document",
                               "Referer": "https://zhidao.baidu.com",
                               "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9"}

        self.detail_headers1 = {"Host": "zhidao.baidu.com", "Connection": "keep-alive", "Cache-Control": "max-age=0",
                               "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
                               "sec-ch-ua-mobile": "?0", "Upgrade-Insecure-Requests": "1",
                               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
                               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                               "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1",
                               "Sec-Fetch-Dest": "document",
                               "Referer": "https://zhidao.baidu.com",
                               "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "zh-CN,zh;q=0.9",
                                "Cookie":"BIDUPSID=EAC73AF735E21F0CD8E38B2450D35165; PSTM=1622612033; BDUSS=jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN; BDUSS_BFESS=jBGUEd5cXlFQXpJOWFwUldlWVdBcTBBR35LeENYNGtJQmgzZ3F4UW9aY2t2TjVnRVFBQUFBJCQAAAAAAAAAAAEAAABBiwU6zqjO7-zhzu~Kx8jLt8cAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACQvt2AkL7dgN; __yjs_duid=1_4b51fe5680eb2b4c1233ff30196299da1622619657966; PREV_DAILY_PERIOD=2897; MCITY=-131%3A; IK_FORCE_UHOME=0; BAIDUID=4E53CB410867F3B1EE35043808F274D3:FG=1; BDSFRCVID_BFESS=m98OJeC6269asEQHanbfEXcivt6Y0J5TH6aoRzKDxKNWjVBmtePSEG0PSU8g0Ku-S2-BogKK0mOTHv-F_2uxOjjg8UtVJeC6EG0Ptf8g0M5; H_BDCLCKID_SF_BFESS=tb48oK0afCK3fP36q46Eh4-hMhoK2D62aJ3aXpjvWJ5TMC_mXtJTK-In-J3yQUQvKK5q0l72Mn5DShPC-tnOKh3beajRXnv3-enzVlOt3l02V-OIe-t2ynLVKxo7e4RMW20jWl7mWPLVsxA45J7cM4IseboJLfT-0bc4KKJxbnLWeIJIjjC5j5oyeHAftTnK2670LnK8bb58jJjk247HhCCShUFs3KrJB2Q-5KL-MUj1HUJ4y-Q_-4_kWMb0-tQiymnhafbdJJL5eDbue5JV0t47jR5jQfcLLmTxoUJz5DnJhhvGXfno5P4ebPRiJPr9QgbqslQ7tt5W8ncFbT7l5hKpbt-q0x-jLTnhVn0M5DK0hD89Dj8Ke5P8qx5Ka43tHD7yWCvEfCncOR5Jj6K-et_yQJQ7546a5eTv3bTKbIQZhhFG3MA--t4w24RRhUnwQKQp5J625xJ6sq0x0hble-bQyp_LQ5DL0DOMahkMal7xO-LzQlPK5JkgMx6MqpQJQeQ-5KQN3KJmfbL9bT3YjjISKx-_tjDJtJRP; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; H_PS_PSSID=31660_26350; BAIDUID_BFESS=4E53CB410867F3B1EE35043808F274D3:FG=1; delPer=0; PSINO=7; ZD_ENTRY=empty; Hm_lvt_6859ce5aaf00fb00387e6434e4fcc925=1629941224,1630311023,1630559997,1630578341; shitong_key_id=2; Hm_lvt_eaa57ca47dacb4ad4f5a257001a3457c=1629707375,1630311023,1630559999,1630578341; cflag=13%3A3; ab_sr=1.0.1_M2NlOTI5MzM1ODk5NjIzZjRhZjBmNmEyMTA3ZWFlNjA5ZWFkMmZiNzU3MTljNzg5ZDc5ODgwM2QwYjNhMDA4MzBiZTRiNDViOGQ2ZjM4N2UzNzZmMjQwOTJlYTgyMmM5NTZkOWNmNDA5YTlkNjA2YzAyNWMwZDc4NmNmNGJmYWIzNjM3MzU1NDA5MjNkNjE4YjEwMDE5NjFmN2I5M2U1NzkxYmI0Yjk0N2VjYmE4NWMxMWUzNzJlNGE4OWM4ZWVj; Hm_lpvt_6859ce5aaf00fb00387e6434e4fcc925=1630581892; shitong_data=82da467dfa4d7cf4e952a2fd6cd79a89c93647c37456fb06484cc3e1a9867bb7892a8b7b05583801069c2fd683b05abd42312a7a18ecae51a90f674bc6b0ddbc6a06b0e70f747f2b0879caf2023a82954b830608b0ba0a7fc583e6e41096add9d3b108c52887207806e0cc2ed025eb0f446a2e5b7cec0e77ae700d4e7e3a0cfd; shitong_sign=7052983d; Hm_lpvt_eaa57ca47dacb4ad4f5a257001a3457c=1630581892"}
        self.logger = get_logger('wenda', logger_path)
        # self.page = 0


    def Whether_Crawler(self,url,cfg):

        code_distinguish = golaxy_Downloader(call_proxy=1)
        HTML = code_distinguish.get_html(url,headers=self.detail_headers1)
        response = etree.HTML(HTML)
        comments_count = "".join(response.xpath("//*[@id=\"qb-content\"]/div[2]/span[2]/text()"))
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

    def formatEntryUrl(self,cfg):

        tmp_url = cfg["detail_url"]+"?rn=5&pn={}".format(cfg["total_page"])
        print("tmp_url:",tmp_url)

        self.logger.info("datil_id=%s,datil_url=%s" % (cfg["detail_id"], tmp_url))
        cfg["Whether_Crawler"] = self.Whether_Crawler(tmp_url, cfg)
        request = scrapy.Request(tmp_url, callback=self.parse,headers=self.detail_headers,cookies=self.detail_cookie)
        request.meta['cfg'] = copy.deepcopy(cfg)
        return request

    def parse(self,response):
        cfg = response.meta["cfg"]

        if cfg["Whether_Crawler"]:
            return
        cfg["total_page"]+=1
        page = response.body
        page = page.decode("gbk", 'ignore')
        datas = response.xpath("//*[@id=\"wgt-best\"]/div") + response.xpath("//*[@id=\"wgt-answers\"]/div/div")
        for data in datas:
            item = QuestionsanswersCommentItem()
            item.init()

            item["board_id"] = cfg["board_id"]
            item["board_name"] = cfg["board_name"]
            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            author_url = "".join(data.xpath("./div[@class=\"wgt-replyer-all\"]/a[1]/@href").extract())

            if len(author_url) == 0:
                continue
            item["user_url"] = author_url
            user_id = "".join(re.findall("https://zhidao\.baidu\.com/usercenter\?uid=(.*?)&",author_url))

            item["user_id"] = user_id

            item["detail_id"] = cfg["detail_id"]
            item["publish_time"] = int(str_to_timestamp("".join(data.xpath(".//span[@class=\"wgt-replyer-all-time\"]/text()").extract())))*1000
            item["gather_time"] = int(time.time()) * 1000

            # 用户头像
            author_img = "".join(data.xpath(".//div[@class=\"wgt-replyer-all-avatar\"]/@style").extract())
            author_img = re.sub("background-image: url\(", "", author_img)
            author_img = re.sub("\)", "", author_img)

            item["user_img"] = author_img

            # 用户名
            author = "".join(data.xpath(".//div[@class=\"wgt-replyer-all\"]/a[2]//text()").extract()).strip()
            item["user_name"] = author

            comment_id= "".join(data.xpath(".//div[@accuse=\"aContent\"]/@id").extract())
            item["comment_id"] = re.sub("answer-content-","",comment_id)

            isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["comment_id"])
            if (isExist):
                continue
            # 回帖
            content = data.xpath(".//div[@accuse=\"aContent\"]//text()").extract()
            content = re.sub("\n展开全部", "", "\n".join(content))
            content = re.sub("\n\n", "\n", content)
            content = re.sub("\n\n", "\n", content)
            item["comment"] = content
            # 点赞数
            like_num = "".join(data.xpath(".//div[@class=\"line content\"]/div[3]/div/div/span[1]/@data-evaluate").extract())
            if len(like_num)==0:
                like_num =0
            like_num = int(like_num)
            item["likes_count"] = like_num

            # 评论数  常量
            item["comments_count"] = 0
            # like_num= int(like_num)
            self.logger.info("media_id=%s,comment_id=%s" % (str(item["media_id"]),item["comment_id"]))
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["comment_id"])
            yield item
            # print(json.dumps(item, ensure_ascii=False))
        next_page_url = "".join(data.xpath("//a[@class=\"pager-next\"]/@href").extract())
        if len(next_page_url)>0:
            next_page_url = urljoin(self.index_url,next_page_url)
            self.detail_headers["Referer"] = response.url
            request = scrapy.Request(next_page_url, callback=self.parse, headers=self.detail_headers,
                                     cookies=self.detail_cookie)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request