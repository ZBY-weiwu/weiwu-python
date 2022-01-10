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
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
conf = configparser.ConfigParser()

print("parent_dir:",parent_dir)
conf.read(parent_dir + "/../../config/config.ini", encoding="utf-8")

time_interval = int(conf.get("Scheduler_Time", "time_interval"))
logger_path = conf.get("LoggerPath", "logger_path")


# proxies_list = conf.get("Request", "proxies_list")

# 处理facebook、twitter的（Fri Jan 31 16:24:39 +0000 2020）


# 日志
def get_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)
    return l

def readTaskFile(file_dir):
    for root, dirs, files in os.walk(file_dir):
        print(files)  # 当前路径下所有非目录子文件
        for file_name in files:
            flie_cont = open(file_dir + "/" + file_name, "r+", encoding="utf-8")
            keyword_list = flie_cont.readlines()
            yield keyword_list


def Get_md5(url):
    import hashlib
    a = hashlib.md5(url.encode())
    md5_str = a.hexdigest()
    return md5_str

def w_pid(cfg):
    pid=os.getpid()
    fp = open("./pid/"+cfg+".pid",'w')
    fp.write(str(pid))
    fp.close()

proxies_list = [{'http': 'http://192.168.1.44:1081', 'https': 'https://192.168.1.44:1081'}]

if __name__ == '__main__':
    for i in readTaskFile("../../seed"):
        print(i)
