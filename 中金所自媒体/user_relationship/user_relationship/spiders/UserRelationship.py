import scrapy
import os
import json
import time
from user_relationship.spiders.choice_spider import abstractFactory
from wemedia_comment.core.golaxy.common.utils import db
from user_relationship.Tools.my_package import get_user_relationship_task
import configparser

conf = configparser.ConfigParser()

conf.read( "./config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "task_seed_logger_path")
es_hosts = conf.get("Es", "es_hosts")
index_name = conf.get("Es", "index_name")
es_user = conf.get("Es", "es_user")
es_password = conf.get("Es", "es_password")
seed_generation_number = int(conf.get("TaskSchedul", "seed_generation_number"))
task_files_count = int(conf.get("TaskSchedul", "task_files_count"))


# redis_config
redis_hosts = conf.get("Redis", "hosts")
redis_port = conf.get("Redis", "port")
redis_db = conf.get("Redis", "db")
redis_table = conf.get("Redis", "redis_table")

class UserRelationship(scrapy.Spider):

    name = "WemediaUserRelationship"
    # board_sc = db.RedisQueueScheduler(redis_kwargs={
    #     'host': redis_hosts,
    #     "port": redis_port,
    #     "db": redis_db
    # })

    def __init__(self):
        print ("WemediaUserRelationship")
        self.seed_item_list = []
        self.raedseed()
        self.users_list = []
        self.get_apui_url = "http://data-service.golaxy.cn:8080/management/crawler/account/v2/queryTasks?sid=25953&update=1"


    def raedseed(self):
        #trim = True 的时候 是取一次 删一次
        # seedcontent = self.board_sc.get(redis_table, trim=False)
        # seedcontent = [{"site_name":"雪球","site_id":77,"relationship_type":"follower","user_id":"7006401177","user_name":"梅事聊"},{"site_name":"雪球","site_id":77,"relationship_type":"follow","user_id":"7006401177","user_name":"梅事聊"}]
        # seedcontent = [{"site_name":"东方财富股吧","site_id":91,"relationship_type":"follow","user_id":"7285395547995552","user_name":"梅事聊"},{"site_name":"东方财富股吧","site_id":91,"relationship_type":"follower","user_id":"7285395547995552","user_name":"梅事聊"}]
        seedcontent =  get_user_relationship_task()
        if len(seedcontent)==0:
            time.sleep(30)
            return

        for sub in seedcontent:
            # sub = json.loads(sub)
            seed_item={}
            seed_item["site_name"] = sub['site_name']
            seed_item["site_id"] = sub['site_id']
            seed_item["relationship_type"] = sub['relationship_type']
            seed_item["user_id"] = sub['user_id']
            seed_item["user_name"] = sub['user_name']
            seed_item["total_page"] = 0
            self.seed_item_list.append(seed_item)

    def start_requests(self):
        for cfg in self.seed_item_list:
            print(cfg)
            spider = abstractFactory().getFactory(cfg["site_id"]).formatEntryUrl(cfg)
            if not spider:
                continue
            yield spider
