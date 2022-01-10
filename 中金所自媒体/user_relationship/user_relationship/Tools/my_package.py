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

# -*- coding: UTF-8 -*-
import re
import random
import json
import requests
import time, datetime
import logging  # 引入logging模块
from logging.handlers import TimedRotatingFileHandler
import os.path
import time
import configparser
import urllib3, requests
import dateutil.parser
import warnings
import socket
import socks

warnings.filterwarnings("ignore")

# logging.disable(30)
parent_dir = os.path.dirname(os.path.abspath(__file__))

conf = configparser.ConfigParser()


conf.read(parent_dir + "\..\..\config\config.ini", encoding="utf-8")

logger_path = conf.get("LoggerPath", "logger_path")
hosts = conf.get("Mysql", "hosts")
port = int(conf.get("Mysql", "port"))
user = conf.get("Mysql", "user")
password = conf.get("Mysql", "password")
database_name = conf.get("Mysql", "database_name")
table_name = conf.get("Mysql", "table_name")

GetTasksSid = conf.get("GetTasks", "sitenames")


# proxies_list = conf.get("Request", "proxies_list")

# 处理facebook、twitter的（Fri Jan 31 16:24:39 +0000 2020）
# 1：帖子或视频信息；2：用户信息；3：粉丝；4：好友；5：转发；6：评论；7：点赞 8：群组信息；9：成员信息


# 时间戳转时间
def format_pubtime(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime


# 时间转时间戳
def timeStamp_data(pt_data):
    timeArray = time.strptime(pt_data, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray)) * 1000
    return timeStamp


# 去重策略
def query_repeat(channel, id):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36",
        "Accept": "application/json"}
    reponse = requests.get(
        "http://192.168.1.20:8090/api/v2/web/browse/duplicateByChannelAndId?channel=%s&id=%s" % (channel, id),
        headers=headers)
    resp = json.loads(reponse.text)
    data = resp['data']
    return data


# 日志
def get_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)

    return logging.getLogger(logger_name)

def get_task():
    tasks = GetTasksSid.split("|")
    print(tasks)
    tasks_list =[]
    users_relationship = ["follower", "follow"]
    for task in tasks:
        url = "http://data-service.golaxy.cn:8080/management/crawler/account/v2/queryTasks?sid={}&update=1&taskType={}".format(task,3)
        print("task_url:",url)
        resp = requests.get(url)
        datas = resp.json()

        api_tasks = datas.get("tasks")
        for user_relationship in users_relationship:
            for task in api_tasks:
                task_dict = dict(
                site_name = task.get("site_name"),
                site_id = task.get("site_id"),
                relationship_type = user_relationship,
                user_id = task.get("uid"),
                user_name = task.get("name"))
                tasks_list.append(task_dict)
    return tasks_list


# 时间抽取转换
def str_to_timestamp(date):
    dt = datetime.datetime.now()
    year = dt.year

    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    now = int(time.time())
    isParse = False
    # if not "前" in date:
    #    isParse=True
    m = None
    if not isParse:
        m = re.search('(\d+)\s*秒之*前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))
    if not isParse:
        m = re.search('(\d+)\s*分钟之*前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60
    if not isParse:
        m = re.search('(\d+)\s*小时之*前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60 * 60
    if not isParse:
        m = re.search('(\d+)\s*天之*前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60 * 60 * 24
    if not isParse:
        m = re.search('(\d+)\s*个月之*前', date, re.M | re.I)
        if m:
            isParse = True
            now = now - int(m.group(1)) * 60 * 60 * 24 * 30

    if not isParse:
        m = re.search('昨天', date, re.M | re.I)
        if m:
            isParse = True
            day_time = int(time.mktime(datetime.date.today().timetuple()))
            now = day_time - 60 * 60 * 24

    if not isParse:
        m = re.search('今天\s*(\d+):(\d+)', date, re.M | re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                hour = m.group(1)
            if m.group(2):
                minute = m.group(2)
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search('(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?', date, re.M | re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                year = m.group(1)
                if len(str(year)) == 2:
                    year = "20" + year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)
            if m.group(4):
                hour = m.group(4)
            if m.group(5):
                minute = m.group(5)
            if m.group(6):
                second = m.group(6)
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + str(second)
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))

    if not isParse:
        m = re.search('(\d{2,4})?年?(\d{1,2})月(\d{1,2})日', date, re.M | re.I)
        if m:
            isParse = True

            if m.group(1):
                year = m.group(1)
                if len(str(year)) == 2:
                    year = "20" + year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)

            hour = "00"
            minute = "00"
            second = "00"
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))



    if not isParse:
        m = re.search('(\d{2,4})?\.(\d{1,2})\.(\d{1,2})\s*(\d{1,2}):(\d{1,2})', date, re.M | re.I)
        if m:
            isParse = True

            if m.group(1):
                year = m.group(1)
                if len(str(year)) == 2:
                    year = "20" + year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)

            if m.group(4):
                hour = m.group(4)

            if m.group(5):
                minute = m.group(5)

            second = "00"
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))


    if not isParse:
        m = re.search('(\d{2,4})?\.(\d{1,2})\.(\d{1,2})', date, re.M | re.I)
        if m:
            isParse = True

            if m.group(1):
                year = m.group(1)
                if len(str(year)) == 2:
                    year = "20" + year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)

            hour = "00"
            minute = "00"
            second = "00"
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))

    if not isParse:
        m = re.search('(\d{1,2})-(\d{1,2})\s*(\d{1,2}):(\d{1,2})', date, re.M | re.I)
        if m:
            isParse = True
            if m.group(1):
                month = m.group(1)
            if m.group(2):
                day = m.group(2)
            if m.group(3):
                hour = m.group(3)
            if m.group(4):
                minute = m.group(4)

            second = "00"
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + str(hour) + ":" + str(minute) + ":" + second
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))


    if not isParse:
        m = re.search('(\d{2,4})?-(\d{1,2})-(\d{1,2})', date, re.M | re.I)
        if m:
            isParse = True

            if m.group(1):
                year = m.group(1)
                if len(str(year)) == 2:
                    year = "20" + year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)

            hour = "00"
            minute = "00"
            second = "00"
            s = str(year) + "-" + str(month) + "-" + str(day) + " " + hour + ":" + minute + ":" + second
            d = dateutil.parser.parse(s, fuzzy=True)
            now = int(time.mktime(d.timetuple()))


    if not isParse:
        m = re.search(
            r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2}\w\d{1,2}:\d{1,2}:\d{1,2})',
            date, re.M | re.I)

        if m:

            isParse = True
            date = m.group()
            d = dateutil.parser.parse(date, fuzzy=True)
            t = int(time.mktime(d.timetuple()))
            if t < now:
                now = t
    return now



def W_mysql(site_name:str,site_id:int,board_name:str,board_id:int,url:str,detail_id:str,detail_url:str):
    import pymysql
    conn = pymysql.connect(host=hosts, port=port, user=user, passwd=password, db=database_name)
    cur = conn.cursor()  # 使用cursor()方法创建一个游标对象cur
    insert_time = int(time.time())
    print(table_name,site_name,site_id,board_name,board_id,url,detail_id,detail_url,insert_time)
    sql = "insert into `%s` (site_name,site_id,board_name,board_id,url,detail_id,detail_url,insert_time) values ('%s',%s,'%s',%s,'%s','%s','%s',%s)"%(table_name,site_name,site_id,board_name,board_id,url,str(detail_id),detail_url,insert_time)
    print(sql)
    cur.execute(sql)
    conn.commit()

def Get_md5(url):
    import hashlib
    a = hashlib.md5(url.encode())
    md5_str = a.hexdigest()
    return md5_str


proxies_list = [{'http': 'http://192.168.1.44:1081', 'https': 'https://192.168.1.44:1081'}]

if __name__ == '__main__':
    pass
