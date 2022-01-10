import scrapy
import os
import json
from QuestionsAnswers_search.spiders.choice_spider import abstractFactory

# class BaiduzhidaoSpiderSpider(scrapy.Spider):
#     name = 'baiduzhidao_spider'
#     allowed_domains = ['baidu.com']
#     start_urls = ['http://baidu.com/']
#
#     def parse(self, response):
#         pass

class wenda_searchSpider(scrapy.Spider):

    name = "QuestionsAnswersspider_search"
    def __init__(self, cfg):
        print ("QuestionsAnswersspider")

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
            seed_item={}

            seed_item["site_id"] = sub['site_id']
            seed_item["site_name"] = sub['site_name']
            seed_item["keyword"] = sub.get('keyword',"")
            # seed_item["location"] = sub['location']
            seed_item["total_page"] = 0
            print("seed_item:",json.dumps(seed_item))
            self.seed_item_list.append(seed_item)

    def start_requests(self):
        for cfg in self.seed_item_list:

            spider = abstractFactory().getFactory(cfg["site_id"]).formatEntryUrl(cfg)
            if not spider:
                continue
            yield spider
