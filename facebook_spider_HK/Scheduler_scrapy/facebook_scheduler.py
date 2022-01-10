# try:
#     from facebook_spider_HK.FacebookSpider_by.fb_spider import  FacebookSpider
# except:
from FacebookSpider_by.fb_spider import  FacebookSpider
from fake_useragent import UserAgent
import json,re
from multiprocessing.pool import ThreadPool
import time
import configparser
from urllib.parse import unquote
import requests
import sys
import atexit
import urllib3,os


urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
conf = configparser.ConfigParser()
parent_dir = os.path.dirname(os.path.abspath(__file__))
conf.read(parent_dir+"/../config/config.ini",encoding="utf-8")

Multithreading = int(conf.get("Request","Multithreading"))
read_seed = conf.get("Read_Seed","read_seed")
pool = ThreadPool(processes=Multithreading)




# @atexit.register
# def quit():
#     print("请处理不正规的公共页url")

def request_fb_server(data):
    #resp = requests.post("http://192.168.1.20:5580/facebook_spider",data=data)
    print(data)
    # resp = requests.get("http://127.0.0.1:5580/facebook_spider?json_data="+data)
    resp = requests.get("http://192.168.31.68:5580/facebook_spider?json_data=" + data)
    if resp.status_code==200:
        print("开始采集")
    else:
        print("服务请求异常")

"""
def scheduler_running():
    seed_file = open(parent_dir+"/../SeedTask/{}.json".format(read_seed), "r+", encoding="utf-8")
    seed_datas = seed_file.readlines()
    screen_list = []
    for seed_obj in seed_datas:
        screen_list.append(seed_obj)

    pool.map(request_fb_server, (i for i in screen_list))
    pool.close()
"""

def scheduler_running():
    seed_file = open(parent_dir+"/../SeedTask/{}.json".format(read_seed), "r+", encoding="utf-8")
    seed_datas = seed_file.readlines()
    for seed_data in seed_datas:
        request_fb_server(seed_data)

if __name__ == '__main__':
    scheduler_running()
