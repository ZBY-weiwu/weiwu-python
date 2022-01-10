import scrapy
import os
import json
from wemedia_comment.spiders.choice_spider import abstractFactory

# class BaiduzhidaoSpiderSpider(scrapy.Spider):
#     name = 'baiduzhidao_spider'
#     allowed_domains = ['baidu.com']
#     start_urls = ['http://baidu.com/']
#
#     def parse(self, response):
#         pass

class BaiduzhidaoSpiderSpider(scrapy.Spider):

    name = "wenda_comment"
    def __init__(self, cfg):
        print ("wenda_comment")

        self.seed_item_list = []
        # self.taskid = cfg
        self.w_pid(cfg)
        self.readTaskFile("seed/"+cfg+".txt")


    def w_pid(self,cfg):
        pid=os.getpid()
        fp = open("./pid/"+cfg+".pid",'w')
        fp.write(str(pid))
        fp.close()

    def readTaskFile(self, filename):
        f = open(filename,"r+",encoding="utf-8")
        seedcontent = f.readlines()

        for conf in seedcontent:
            sub = json.loads(conf)
            print("sub    ：",sub)
            seed_item={}

            seed_item["detail_id"] = sub['detail_id'][2:]
            seed_item["detail_url"] = sub['detail_url']
            seed_item["site_id"] = sub['site_id']
            seed_item["site_name"] = sub["site_name"]
            seed_item["board_name"] = sub["board_name"]
            seed_item["board_id"] = sub["board_id"]

            # seed_item["location"] = sub['location']
            seed_item["total_page"] = 0

            self.seed_item_list.append(seed_item)

    def start_requests(self):
        for cfg in self.seed_item_list:
            print(cfg)
            spider = abstractFactory().getFactory(cfg["site_id"]).formatEntryUrl(cfg)
            if not spider:
                continue
            yield spider
