# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin
import pymysql
import os

def wenda_insert(file_dir):

    conn= pymysql.connect(host='10.20.18.100',port = 3306,user='root',passwd='123456',db ='wenda',)
    cur = conn.cursor()

    for root, dirs, files in os.walk(file_dir):
        for sub in files:
            file = open("./seed_json/"+sub,"r+",encoding="utf-8")
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                sub = json.loads(line)

                site_id = sub["site_id"]
                site_name = sub["site_name"]
                board_id = sub["board_id"]
                board_name = sub["board_name"]
                entryurl = sub["entry_url"]
                config = sub["config"]
                board_url = sub["board_url"]
                create_time = int(time.time())
                insertsql = "insert into `wenda-crawl` (site_id,site_name,board_id,board_name,entryurl,config,board_url,create_time) VALUES (%d,'%s',%d,'%s','%s','%s','%s',%d)" % (site_id, site_name, board_id, board_name,entryurl, config,board_url,create_time)
                # try:
                #     #print insertsql
                #     print ("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                #     cur.execute(insertsql)
                #     cur.commit()
                #
                # except:
                #     print("Error")
                #     pass
                #     #db.rollback()

                print ("插入完成：board_name:%s"%board_name)
                cur.execute(insertsql)
                conn.commit()

    conn.close()

if __name__ == '__main__':
    wenda_insert("./seed_json")