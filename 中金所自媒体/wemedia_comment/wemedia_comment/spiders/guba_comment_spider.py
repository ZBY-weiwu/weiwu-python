import scrapy
import os
import json
import copy
import time
from urllib.parse import urljoin
import configparser
from fake_useragent import UserAgent
from wemedia_comment.items import WemediaCommentItem,ChildCommentItem
from scrapy.utils.project import get_project_settings
from wemedia_comment.Tools.dupClient import DUPClient
from wemedia_comment.Tools.wenda_package import get_logger,Get_md5,str_to_timestamp,timeStamp_data
from wemedia_comment.Tools.golaxy_request import Downloader_HTML as golaxy_Downloader
parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read(os.getcwd() + "/config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "logger_path")
logger_switch = int(conf.get("LoggerPath", "logger_switch"))



ua = UserAgent(path=r"./wemedia_comment/Tools/useragent.json")
dupClient = DUPClient()

class DongfangcaifugubaCommentSpider():
    def __init__(self):
        print("DongfangcaifugubaCommentSpider")

        settings = get_project_settings()
        self.DUP_URL = settings.get('DUP_URL')
        self.DUP_CHANNEL = settings.get('DUP_CHANNEL')
        self.DUP_CHANNEL_Article = "app"
        self.DOUBLE_DUP_DOMAIN = settings.get('DOUBLE_DUP_DOMAIN')

        self.proxies = {
            "http": 'http://10.20.18.100:7777',"https": 'https://10.20.18.100:7777'
        }
        if logger_switch == 0:
            self.logger_switch=False
        else:
            self.logger_switch = True

        self.logger = get_logger('wemedia_comment', logger_path)

    def formatEntryUrl(self,cfg):
        cfg["total_page"]+=1
        tmp_url = cfg["detail_url"]
        if logger_switch:
            self.logger.info("datil_id=%s,url=%s" % (cfg["detail_id"], cfg["url"]))

        Referer = "http://mguba.eastmoney.com/mguba/article/0/{}".format(cfg["detail_id"])
        self.detail_headers = {"Content-Type": "application/x-www-form-urlencoded",
                               "Referer": Referer,
                               "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Mobile Safari/537.36"}
        # formdata = "param=postid={}&sort=1&sorttype=1&p={}&ps=30&path=reply/api/Reply/ArticleNewReplyList".format(cfg["detail_id"],cfg["total_page"])
        formdata = {"param":"","postid":str(cfg["detail_id"]),"sorttype":"1","p":str(cfg["total_page"]),"ps":"30","path":"reply/api/Reply/ArticleNewReplyList"}
        Whether_Crawler= self.WhetherCrawler(cfg)
        data = "param=postid={}&sort=1&sorttype=1&p={}&ps=30&path=reply/api/Reply/ArticleNewReplyList".format(
            cfg["detail_id"], cfg["total_page"])
        if Whether_Crawler:
            # request = scrapy.FormRequest(tmp_url, callback=self.parse,formdata=formdata,headers=self.detail_headers)

            request = scrapy.Request(tmp_url,method="post", callback=self.parse,body=data,headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            return request
        else:
            if self.logger_switch:
                self.logger.info("No need to update comments!")
            return


    def WhetherCrawler(self,cfg):
        data = "param=postid={}&sort=1&sorttype=1&p={}&ps=30&path=reply/api/Reply/ArticleNewReplyList".format(
            cfg["detail_id"], cfg["total_page"])
        url = cfg["detail_url"]
        GolaxyDownloader = golaxy_Downloader(call_proxy=0)
        HTML = GolaxyDownloader.post(url,headers=self.detail_headers,data=data)
        json_data =json.loads(HTML)
        comments_count = int(json_data.get("count",0))
        # get_data = dupClient.getPara(self.DUP_URL, self.DUP_CHANNEL, cfg["detail_id"])
        get_data = dupClient.getPara(self.DUP_URL, self.DUP_CHANNEL_Article, cfg["url"])
        try:
            get_comment_obj = json.loads(get_data)
        except:
            return True
        # 若果评论采集过comment_index_v1=False，默认为True
        if isinstance(get_comment_obj,int):
            if comments_count == get_comment_obj:
                return False
            else:
                return True
        comment_index_v1 = get_comment_obj.get("comment_index",True)
        comments_data = {}
        comments_data["comments_count"] = comments_count
        comments_data["comment_index"] = comment_index_v1
        params = json.dumps(comments_data)
        # dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, cfg["detail_id"],params)
        dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL_Article, cfg["url"],params)
        if comments_count == get_comment_obj["comments_count"]:
            return False
        else:
            return True

    def parse(self,response):

        cfg = response.meta["cfg"]
        cfg["total_page"]+=1
        json_obj = json.loads(response.body)
        datas = json_obj.get("re")

        if not datas:
            return
        for data in datas:

            item = WemediaCommentItem()
            item.init()

            item["media_name"] = cfg["site_name"]
            item["media_id"] = cfg["site_id"]
            user_data = data.get("reply_user")
            item["comment_id"] = data.get("reply_id")
            item["user_id"] = user_data.get("user_id")
            item["user_name"] = user_data.get("user_name")
            item["screen_name"] = user_data.get("user_nickname")
            item["publish_time"] = timeStamp_data(data.get("reply_publish_time"))

            item["content"] = data.get("reply_text")
            item["comments_count"] = int(data.get("reply_count"))
            item["gather_time"] = int(time.time()*1000)
            item["url"] = "http://guba.eastmoney.com/news,gssz,{}.html".format(cfg["detail_id"])

            # 和文章关联的id
            item["root_id"] = Get_md5(cfg["url"])
            item["likes_count"] = data.get("reply_like_count",0)
            if len(data.get("child_replys"))>0 or item["comments_count"]>0:
                for child_reply_data in data.get("child_replys"):
                    child_item = ChildCommentItem()
                    child_item.init()
                    child_user_data = child_reply_data.get("reply_user")
                    child_item['media_name'] = cfg["site_name"]
                    child_item['media_id'] = cfg["site_id"]
                    child_item['comment_id'] = child_reply_data.get("reply_id")
                    child_item['user_id'] = child_reply_data.get("user_id")
                    child_item['user_name'] = child_user_data.get("user_name")
                    child_item['screen_name'] = child_user_data.get("user_nickname")
                    child_item['publish_time'] = timeStamp_data(child_reply_data.get("reply_publish_time")),
                    child_item['publish_time']=int(child_item["publish_time"][0])
                    child_item['content'] = child_reply_data.get("reply_text")
                    child_item['likes_count'] = child_reply_data.get("reply_like_count")
                    child_item['url'] = item["url"]
                    child_item["root_id"] = item["root_id"]
                    child_item['parent_id'] = item["comment_id"]
                    # child_isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, child_item["comment_id"])
                    # if child_isExist:
                    #     continue
                    # dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, child_item["comment_id"])
                    yield child_item

            # isExist = dupClient.findAndSet(self.DUP_URL, self.DUP_CHANNEL, 3600, item["comment_id"])
            # if isExist:
            #     continue

            comments_data = {}
            comments_data["comments_count"] = item['comments_count']
            # 采集过 comments_data=False
            comments_data["comment_index"] = False
            params = json.dumps(comments_data)
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, cfg["detail_id"], params)
            dupClient.confirm(self.DUP_URL, self.DUP_CHANNEL, item["comment_id"])
            yield item
            # print(json.dumps(item, ensure_ascii=False))

        if cfg["total_page"]<=10:
            cfg["total_page"] += 1
            tmp_url = cfg["detail_url"]
            formdata = {"param": "", "postid": str(cfg["detail_id"]), "sorttype": "1", "p": str(cfg["total_page"]),
                        "ps": "30", "path": "reply/api/Reply/ArticleNewReplyList"}
            request = scrapy.FormRequest(tmp_url, callback=self.parse, formdata=formdata, headers=self.detail_headers)
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request
