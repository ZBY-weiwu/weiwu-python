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

class SchedulingMysql:
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

    def dispatch_spider(self):

        es = Elasticsearch(hosts=es_hosts,sniff_on_start=True ,http_auth=(es_user, es_password),sniff_on_connection_fail=True ,sniffer_timeout=60
                           ,ignore=[400, 405, 502])  # 以列表的形式忽略多个状态码
        # 三天内
        time_gte = int(time.time()-259200)*1000

        query_json = {
        "query": {
            "bool": {
                "must": [
                    {
                        "range": {
                            "gt": {
                                "gte": time_gte
                            }
                        }
                    },
                    {
                        "terms": {
                            "i_sid":["8","77","91"]
                        }
                    }
                ]
            }
        },
        "_source": ["i_bid","i_sn","i_sid","url"]
    }
        page_num = seed_generation_number  # 每次获取数据
        # query = es.search(index="hs_twitter", body=query_json, scroll='5m', size=page_num)
        query = es.search(index=index_name, body=query_json, scroll='5m', size=page_num)
        # results = query['hits']['hits']  # es查询出的结果第一页

        total = query['hits']['total']  # es查询出的结果总量

        scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
        every_num = int(total/page_num)  #

        for i in range(0, every_num +1):
            sql = "insert into `{}` (site_name,site_id,board_name,board_id,url,detail_id,detail_url,insert_time) values (%s,%s,%s,%s,%s,%s,%s,%s)".format(table_name)
            query_scroll = es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
            # results += query_scroll
            results = query_scroll
            print(len(results))
            item_list = []
            for key in results:

                source = key['_source']
                item_data_list = []
                item = {}
                item["site_name"] = source["i_sn"]
                item["site_id"] = source["i_sid"]
                item["board_name"] = source["i_sn"]+"-评论"
                item["board_id"] = -1
                item["url"] = source["url"]
                if item["site_id"]==8:
                    if "group" in source["url"]:
                        item["detail_id"] = re.sub("http://toutiao\.com/group/", "", source["url"]).replace("/","")
                    else:
                        item["detail_id"] = re.sub("https://m\.toutiao\.com/i", "", source["url"]).replace("/","")
                    item["detail_url"] = "https://www.toutiao.com/article/v2/tab_comments/?aid=24&app_name=toutiao_web&offset={}&count=20&group_id={}"
                elif item["site_id"]==77:
                    detail_id = re.findall("https://xueqiu\.com/\d+/(\d+)", source["url"])
                    item["detail_id"] = detail_id[0]
                    item["detail_url"] = "https://xueqiu.com/statuses/comments.json?id={}&count=20&page={}&reply=true&asc=false&type=status&split=true"
                elif item["site_id"] == 91:
                    detail_id=re.findall("http://mguba\.eastmoney\.com/mguba/article/\d+/(\d+)", source["url"])
                    detail_id = detail_id[0]
                    item["detail_id"] =detail_id
                    item["detail_url"] = "http://guba.eastmoney.com/interface/GetData.aspx"
                else:
                    pass

                insert_time = int(time.time())
                item["insert_time"] = insert_time
                # item_data = json.dumps(item, ensure_ascii=False)
                item_list.append(tuple(item.values()))
            sql_item = tuple(item_list)
            print(sql)
            print(sql_item)
            self.mysql_helper.executemany(sql,sql_item)


if __name__ == '__main__':
    WD = SchedulingMysql()
    WD.dispatch_spider()


