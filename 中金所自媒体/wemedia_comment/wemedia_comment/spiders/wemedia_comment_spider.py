import scrapy
import json
from wemedia_comment.spiders.choice_spider import abstractFactory
from wemedia_comment.task_handle.get_task import GetTask
import configparser
conf = configparser.ConfigParser()

class media_commentSpider(scrapy.Spider):

    name = "wemedia_comment"
    def __init__(self):
        print ("wemedia_comment")
        self.seed_item_list = []
        self.get_seed()

    def get_seed(self):
        # seedcontent =['{"site_name": "东方财富APP", "site_id": 91, "board_name": "东方财富APP-评论", "board_id": -1, "url": "http://mguba.eastmoney.com/mguba/article/0/1093595424", "detail_id": "1093595424", "detail_url": "http://guba.eastmoney.com/interface/GetData.aspx", "insert_time": 1634288819}', '{"site_name": "东方财富APP", "site_id": 91, "board_name": "东方财富APP-评论", "board_id": -1, "url": "http://mguba.eastmoney.com/mguba/article/0/1093595431", "detail_id": "1093595431", "detail_url": "http://guba.eastmoney.com/interface/GetData.aspx", "insert_time": 1634288819}']
        for sub in GetTask.get_user_wemediacomment_task():
            seed_item={}
            seed_item["detail_id"] = sub['detail_id']
            seed_item["detail_url"] = sub['detail_url']
            seed_item["site_id"] = sub['site_id']
            seed_item["site_name"] = sub["site_name"]
            seed_item["board_name"] = sub["site_name"]+"-评论"
            seed_item["board_id"] = sub["board_id"]
            seed_item["url"] = sub.get("url","")
            seed_item["total_page"] = 0
            self.seed_item_list.append(seed_item)

    def start_requests(self):
        # print(self.seed_item_list)
        for cfg in self.seed_item_list:
            spider = abstractFactory().getFactory(cfg["site_id"]).formatEntryUrl(cfg)
            # print("spider:",spider)
            if not spider:
                continue
            yield spider
