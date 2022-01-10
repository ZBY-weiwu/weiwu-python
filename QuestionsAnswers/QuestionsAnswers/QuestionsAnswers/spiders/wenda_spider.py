import scrapy
import os
import json
from QuestionsAnswers.spiders.choice_spider import abstractFactory

# class BaiduzhidaoSpiderSpider(scrapy.Spider):
#     name = 'baiduzhidao_spider'
#     allowed_domains = ['baidu.com']
#     start_urls = ['http://baidu.com/']
#
#     def parse(self, response):
#         pass

class WendaSpiderSpider(scrapy.Spider):

    name = "QuestionsAnswersspider"
    def __init__(self, cfg):
        print ("QuestionsAnswersspider")

        self.seed_item_list = []
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

            seed_item["site_id"] = sub['site_id']
            seed_item["board_id"] = sub['board_id']
            seed_item["board_name"] = sub['board_name']
            seed_item["site_name"] = sub['site_name']
            seed_item["entry_url"] = sub['entry_url']
            seed_item["board_url"] = sub["board_url"]
            seed_item["config"] = sub.get('config',"")
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
