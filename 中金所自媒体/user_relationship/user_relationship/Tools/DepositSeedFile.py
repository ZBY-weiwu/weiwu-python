#coding:utf-8

import requests
import urllib3
from elasticsearch import Elasticsearch
import os,json
import time
from scrapy.cmdline import execute
import asyncio
from wemedia_comment.Tools.wenda_package import get_logger
import configparser
import re
from wemedia_comment.Tools.wenda_package import W_mysql
from wemedia_comment.core.golaxy.common.utils import db

urllib3.disable_warnings()
parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()

conf.read(parent_dir + "/config/config.ini", encoding="utf-8")
logger_path = conf.get("LoggerPath", "task_seed_logger_path")
es_hosts = conf.get("Es", "es_hosts")
index_name = conf.get("Es", "index_name")
es_user = conf.get("Es", "es_user")
es_password = conf.get("Es", "es_password")
seed_generation_number = int(conf.get("TaskSchedul", "seed_generation_number"))
task_files_count = int(conf.get("TaskSchedul", "task_files_count"))

#mysql config
hosts = conf.get("Mysql", "hosts")
port = int(conf.get("Mysql", "port"))
user = conf.get("Mysql", "user")
password = conf.get("Mysql", "password")
database_name = conf.get("Mysql", "database_name")
table_name = conf.get("Mysql", "table_name")

async  def scrapy_main(seed_name):
    execute(["scrapy", "crawl", "wemedia_comment", "-a", "cfg={}".format(seed_name)])

class WemediaCommentSchedulingSpider:
    path_name = "../../../../../../facebook_login/Facebook_Public_page/Seed/"
    logger = get_logger('SchedulingLog', logger_path)

    def __init__(self):
        self.item_list = []
        pool = db.MySQLPooled(pool_kwargs={
            'mincached': 2,
            'maxcached': 5,
            'maxconnections': 10,
            'port': port,
            'host': hosts,
            'user': user,
            'password': password,
            'database': database_name
        })
        self.mysql_helper = db.MySQLPooledHandler(pool)

    def write_seed(self,item_data):
        file_name = str(int(time.time()))
        f = open("./seed/{}.txt".format(file_name), "w+", encoding="utf-8")
        f.write(item_data)
        f.flush()
        f.close()

    def time_(self,timeStamp:int):
        timeStamp = timeStamp/1000
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return otherStyleTime

    # 异步下发任务
    def TaskDistribution(self):
        # def file_name():
        file_dir = self.path_name
        for root, dirs, files in os.walk(file_dir):
            # 生成10个文件就下发
            if len(files)>=task_files_count:
                tasks = [scrapy_main(file_name.replace(".txt","")) for file_name in files]
                loop = asyncio.get_event_loop()
                loop.run_until_complete(asyncio.wait(tasks))
            else:
                self.logger.error("Too few task files.")
        self.del_file()

    def del_file(self):
        ls = os.listdir(self.path_name)
        for i in ls:
            c_path = os.path.join(self.path_name, i)
            if os.path.isdir(c_path):
                self.del_file()
            else:
                os.remove(c_path)

    def read_mysql_data(self):
        sql ="SELECT * FROM `{}` ORDER BY update_time LIMIT {}".format(table_name,int(task_files_count))
        sql_dtatas = self.mysql_helper.fetchall(sql)
        item_list = []
        for sql_dtata in sql_dtatas:
            item=dict(
                site_name = sql_dtata[1],
                site_id = sql_dtata[0],
                board_name = sql_dtata[3],
                board_id = sql_dtata[2],
                detail_url = sql_dtata[4],
                detail_id = sql_dtata[5]

            )
            updata_time = int(time.time())
            item_list.append(item)
            print(item)
            updata_sql = 'UPDATE  `{}` set update_time={} WHERE detail_id={}'.format(table_name,updata_time,item["detail_id"])
            self.mysql_helper.execute(updata_sql)

        return json.dumps(item_list,ensure_ascii=False)

    def main(self):
        a= 0
        while True:
            a+=1
            print(a)
            self.write_seed(self.read_mysql_data())


if __name__ == '__main__':
    Schedul_spider = WemediaCommentSchedulingSpider()
    Schedul_spider.main()
