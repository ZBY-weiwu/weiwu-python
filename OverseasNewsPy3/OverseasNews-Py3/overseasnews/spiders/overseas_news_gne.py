import scrapy
import os
import json
import time
# import opencc
from overseasnews.Tools.my_package import Get_md5
from overseasnews.Tools.my_package import DUPClient
from overseasnews.Tools.my_package import get_task
from overseasnews.Tools.my_package import blacklist_url
from overseasnews.Tools.my_package import Is_url
from overseasnews.Tools.my_package import parse_publish_time
from overseasnews.Tools.my_package import golaxy_translate
from overseasnews.Tools.my_package import domain_extraction1
from fake_useragent import UserAgent
from overseasnews.Tools.golaxy_gne.Downloader.GolaxyRequests import GolaxyRequests
from overseasnews.Tools.golaxy_gne import GeneralNewsExtractor
import configparser
from urllib.parse import urljoin
import langid
import uuid
import re
from overseasnews.items import overseanewsItem
import copy
conf = configparser.ConfigParser()

conf.read( "./config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "task_seed_logger_path")

dupClient = DUPClient()

class overseasSpider(scrapy.Spider):

    name = "overseas_news_gne"

    def __init__(self):
        print ("overseas_news")
        self.seed_item_list = []

        self.users_list = []
        self.spider_count_item = 0
        self.DUP_URL = conf.get("DUPClient", "dup_url")
        self.DUPChannel = conf.get("DUPClient", "dup_channel")
        self.SPLASH_URL = conf.get('SPLASH_SERVER', "splash_url")
        self.get_tasks_url = conf.get('GetTASKS', "get_tasks_url")
        ua = UserAgent(path='./config/fake_useragent.json')
        self.headers = {"User-Agent": ua.chrome}
        self.raedseed()


    def get_task(self):
        response = GolaxyRequests.get(self.get_tasks_url)
        tasks_data = json.loads(response.text)
        tasks = tasks_data["tasks"]
        list_task=[]
        for task in tasks:
            task_data={}
            task_data["proxy_enabled"] = task["proxy_enabled"]
            task_data["js_enabled"] = task["js_enabled"]
            task_data["media_name"] = task["site_name"]
            task_data["board_name"] = task["board_name"]
            task_data["media_id"] = task["site_id"]
            task_data["board_id"] = task["board_id"]
            task_data["entry_url"] = task["url"]
            task_data["extractor_config"] = task["extractor_config"]
            list_task.append(task_data)
        print(json.dumps(list_task,ensure_ascii=False))
        return list_task


    def raedseed(self)->list:

        for sub in self.get_task():
            print("sub:",sub)
            # sub = json.loads(sub)
            seed_item={}
            seed_item["media_name"] = sub['media_name']
            seed_item["media_id"] = sub['media_id']
            seed_item["entry_url"] = sub['entry_url']
            seed_item["board_name"] = sub['board_name']
            seed_item["board_id"] = sub['board_id']
            seed_item["extractor_config"] = sub['extractor_config']
            seed_item["GarbledCode"] = sub.get("GarbledCode",False)
            seed_item["js_enabled"] = sub.get("js_enabled",0)
            seed_item["proxy_enabled"] = sub.get("proxy_enabled",0)

            # 首页起始
            seed_item["indexPage"] = 0
            # 详情页起始
            seed_item["DetailTurnPages"] = 0
            # 首页统计
            seed_item["SpreadingDepth"] = int(conf.get("SpreadingDepth", "spreading_depth"))
            # 详情页深度统计
            seed_item["detail_spreading_depth"] = int(conf.get('SpreadingDepth', "detail_spreading_depth"))
            self.seed_item_list.append(seed_item)

    # allowed_domains =["gd.wenweipo.com"]
    def start_requests(self):
        seed_item_list=[{"proxy_enabled": 0, "js_enabled": 0, "media_name": "香港文汇网", "board_name": "文汇报-广东频道-健美探索", "media_id": 2181, "board_id": 10472725, "entry_url": "http://gd.wenweipo.com/?action-category-catid-16", "extractor_config": {"common_extract_service": "GOLAXYNPCE", "extract_type": 0, "extract_config": {}, "boardurl_page_regex": "http://gd.wenweipo.com/?action-category-catid-d+?-page-d+?", "docurl_regex_yes": "http://gd.wenweipo.com/?action-viewnews-itemid-d+?", "boardurl_max_pages": 10}}]
        for cfg in self.seed_item_list:
        # for cfg in seed_item_list:
            self.logger.info("media_id=%s,entry_url=%s" % (cfg["media_id"], cfg["entry_url"]))
            cfg["domain_name"] = domain_extraction1(cfg["entry_url"])

            if int(cfg["js_enabled"]) == 1:
                entry_url = self.SPLASH_URL % cfg["entry_url"]
            else:
                entry_url = cfg["entry_url"]
            if cfg["proxy_enabled"] == 0:
                request = scrapy.Request(entry_url, headers=self.headers, callback=self.parse)
                request.meta['cfg'] = copy.deepcopy(cfg)
                yield request
            else:
                request = scrapy.Request(entry_url, headers=self.headers, callback=self.parse,
                                         meta={'proxy': 'http://127.0.0.1:10809'})
                request.meta['cfg'] = copy.deepcopy(cfg)
                yield request

    def parse(self, response):
        cfg = response.meta['cfg']
        if (response.status != 200):
            self.logger.error("[ErrorCode:%d] [BoardID:%s] [ErrorMsg:'entry url gather failed!',%s]" % (
            21001, cfg["board_id"], cfg["entry_url"]))
            return
        # print("resonse:",response.body)
        urllist=response.xpath("//a")
        # 必须在详情页初始化，以免计数加错
        cfg["DetailTurnPages"] = 0
        cfg["indexPage"] += 1

        for each in urllist:
            now = int(time.time())
            if each.xpath('./@href').extract():
                detail_url=each.xpath('./@href').extract()[0]
                if blacklist_url(detail_url) or Is_url(detail_url):
                    continue
                if "http" not in detail_url:
                    if int(cfg["js_enabled"]) == 1:
                        response_url = re.sub("http://crawler-splash\.golaxy\.local/render\.html\?url=", "", response.url)
                        response_url = re.sub("&timeout=30&wait=0.5","",response_url)
                        full_url = urljoin(response_url,detail_url)
                    else:
                        full_url = response.urljoin(detail_url)
                else:
                    full_url=detail_url
                existence_domain = re.findall(cfg["domain_name"], response.url)
                # existence_domain = re.findall(self.domain_name,cfg["entry_url"])
                if not existence_domain:
                    self.logger.info("Not in domain name")
                    continue
                # print("existence_domain:",existence_domain)
                url =full_url
                md5_url = Get_md5(url)

                isExist = dupClient.findAndSet(self.DUP_URL, self.DUPChannel, 3600, md5_url)
                if (isExist):
                    continue
                # request = scrapy.Request(url, callback=self.parse_detail_content,
                #                          meta={'proxy': 'http://10.20.18.100:8118'})
                request = scrapy.Request(url, headers=self.headers, callback=self.parse_detail_content)
                request.meta['cfg'] = copy.deepcopy(cfg)
                yield request

                if cfg["SpreadingDepth"] >=cfg["indexPage"]:
                    # --------------------
                    if int(cfg["js_enabled"]) == 1:
                        url = self.SPLASH_URL % url
                    if cfg["proxy_enabled"] == 0:
                        request = scrapy.Request(url, headers=self.headers, callback=self.parse)
                        request.meta['cfg'] = copy.deepcopy(cfg)
                        self.logger.info("media_id:[%s],url:[%s]" % (cfg["media_id"], url))
                        yield request
                    else:
                        request = scrapy.Request(url, headers=self.headers, callback=self.parse,
                                                 meta={'proxy': 'http://http://127.0.0.1:10809'})
                        request.meta['cfg'] = copy.deepcopy(cfg)
                        self.logger.info("media_id:[%s],url:[%s]" % (cfg["media_id"], url))
                        yield request


    # 编码未处理|gne图片|翻译接口
    def parse_detail_content(self, response):

        # resp = GolaxyRequests.GetResponse(response)
        try:
            resp = response.body.decode("utf-8")
        except:
            resp = response.body.decode('gbk')
        cfg = response.meta['cfg']

        now = int(time.time())
        board_id = int(cfg['board_id'])
        url = response.url
        PageTurningStatus = False
        if (response.status != 200 or len(response.body) < 10):
            self.logger.error(
                "[ErrorCode:%d] [BoardID:%s] [ErrorMsg:%s,%s]" % (31000, board_id, "News page gather error", url))
            return
        item = overseanewsItem()
        item.Init()
        cfg["DetailTurnPages"] += 1
        item["detail_gather_time"] = now
        item["detail_evidence_degree"] = 0
        item["detail_importance_degree"] = 0
        item["detail_is_homepage"] = 0
        item['detail_board_class_tag'] = []
        item["detail_site_id"] = str(cfg['media_id'])
        item['detail_site_id'] = cfg["media_id"]
        item['detail_board_id'] = cfg["board_id"]
        item['detail_board_name'] = cfg["board_name"]
        item['detail_site_name'] = cfg["media_name"]
        # item['entry_url'] = cfg["entry_url"]
        # {"docurl_regex_yes":"https://www\\.gnlm\\.com\\.mm/\\w+(-\\w+)*/","boardurl_page_regex":"","boardurl_max_pages":10,"extract_type":2,"common_extract_service":"gne-npce","extract_config":{"title_xpath":"//*[@id=\"article-title\"]/h2","title_re":"","content_xpath":"//div[@class=\"entry-content mt-2\"]/p","content_re":"","publish_time_xpath":"//*[@id=\"article-title\"]/ul/li[@class=\"post-date\"]","publish_time_re":"","source_xpath":"","source_re":"","author_xpath":"","author_re":""}}
        extractor_config = cfg.get("extractor_config")
        extract_config = extractor_config["extract_config"]
        # if "gne-npce" in common_extract_service or "GOLAXYNPCE" in common_extract_service or not extractor_config:
        title_xpath = extract_config.get("title_xpath")
        content_xpath = extract_config.get("content_xpath")
        publish_time_xpath = extract_config.get("publish_time_xpath")
        # print("resp:",resp)
        # try:
        if title_xpath and content_xpath and publish_time_xpath:
            if "//text()" not in title_xpath:
                title_xpath += "//text()"
            if "//text()" not in publish_time_xpath:
                publish_time_xpath += "//text()"
            content_xpath = content_xpath.replace("//text()", "")
            data_obj = GeneralNewsExtractor().extract(resp, title_xpath=title_xpath,body_xpath=content_xpath,publish_time_xpath=publish_time_xpath,with_body_html=True)
        else:
            data_obj = GeneralNewsExtractor().extract(resp,with_body_html=True)
        # print("url,{}data_obj:{}".format(response.url,json.dumps(data_obj,ensure_ascii=False)))
        # except:
        #     PageTurningStatus = True
        #     self.logger.error("GNE解析失败")
        #     return
    #----------------------------------------------------------------
        # if PageTurningStatus and cfg["SpreadingDepth"] >=cfg["DetailTurnPages"]:

        if cfg["SpreadingDepth"] >=cfg["DetailTurnPages"]:
            urllist = response.xpath("//a")
            cfg["DetailTurnPages"]+=1
            for each in urllist:
                if each.xpath('./@href').extract():
                    detail_url = each.xpath('./@href').extract()[0]
                    if "javascript:" in detail_url:
                        continue
                    if "http" not in detail_url:
                        full_url = response.urljoin(detail_url)
                    else:
                        full_url = detail_url
                    if Is_url(detail_url):
                        continue
                    existence_domain = re.findall(cfg["domain_name"], response.url)
                    # existence_domain = re.findall(self.domain_name,cfg["entry_url"])
                    if not existence_domain:
                        self.logger.info("Not in domain name")
                        continue
                    url = full_url
                    md5_url = Get_md5(url)
                    isExist = dupClient.findAndSet(self.DUP_URL, self.DUPChannel, 3600, md5_url)
                    if (isExist):
                        continue
                    if cfg["proxy_enabled"] == 0:
                        request = scrapy.Request(url, headers=self.headers, callback=self.parse_detail_content)
                    else:
                        request = scrapy.Request(url, callback=self.parse_detail_content, meta={'proxy': 'http://http://127.0.0.1:10809'})
                    request.meta['cfg'] = copy.deepcopy(cfg)
                    yield request

        title_re = extract_config.get("title_re")
        content_re = extract_config.get("content_re")
        publish_time_re = extract_config.get("publish_time")
        if title_re:
            item["detail_title"] = "".join(re.findall(title_re, data_obj["title"]))
        else:
            item["detail_title"] = data_obj["title"]
        item["detail_author"] = data_obj["author"]
        images = []
        for images_link in  data_obj["images"]:
            images_url =response.urljoin(images_link)
            images.append(images_url)
        item["detail_picture_vector"] = images
        if content_re:
            item["detail_content"] = "".join(re.findall(content_re,data_obj["content"]))
        else:
            item["detail_content"] =data_obj["content"]
        if publish_time_re:
            publish_time = "".join(re.findall(publish_time_re, data_obj["publish_time"]))
            publish_time = parse_publish_time(publish_time) * 1000
        else:
            publish_time = parse_publish_time(data_obj["publish_time"]) * 1000
        item["detail_publish_time"] = publish_time
        item["detail_url"] = url
        item["detail_md5"] = Get_md5(url)
        item["detail_raw_content"] = []
        item["detail_abstract"] = ""
        item["detail_language"] = langid.classify(item["detail_content"])[0]
        item["detail_id"] = str(uuid.uuid1())
        dupClient.confirm(self.DUP_URL, self.DUPChannel, Get_md5(item["detail_title"]))
        # if len(item["detail_content"]) < 1:
        #     self.logger.error(
        #         "[ErrorCode:%d] [BoardID:%s] [ErrorMsg:%s,%s]" % (33000, board_id, "content length is too short", url))
        #     dupClient.delete(self.DUP_URL, self.DUPChannel, item["detail_md5"])
        #     return
        # 翻转简体
        # item["detail_content"] = cc.convert(item["detail_content"])
        # item["detail_title"] = cc.convert(item["detail_title"])
        if len(item["detail_content"])==0:
            self.logger.error("content Characters less than 1,Url:{url}".format(url=url))
            return

        self.logger.info('Crawler new item board_id={},url={},title={}'.format(item["detail_board_id"],item["detail_url"],item["detail_title"]))
        print("详情页url：", response.url)
        print(item)
        self.spider_count_item += 1
        print("spider_count_item:",self.spider_count_item)
        yield item

