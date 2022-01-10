# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random
import time
import requests
import os
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin


import numpy as np
import random
from FaceBook_public.FB_spider.fb_comment import FacebookPrivate_user
from Tools.facebook_package import proxies_list
from config.user_config import UserList


proxies = random.choice(proxies_list)
# print(proxies)
import os.path


def public_comment_Scheduler():
    file_dir = "../SeedTask/Public_comment_seed_list/"
    f = open("../SeedTask/Public_comment_seed_list/Public_Comment.json","r+",encoding="utf-8")
    # seed_list = f.readlines()

    for root, dirs, files in os.walk(file_dir):
        for file_name in files:


            flie_cont = open(file_dir + "/" + file_name, "r+", encoding="utf-8")
            seed_list = flie_cont.readlines()
            for seed_data in seed_list:
                seed_data = json.loads(seed_data)
                print(type(seed_data))
                print(seed_data)
                # FacebookPrivate_spider.Fb_spider(seed_data)
if __name__ == '__main__':
    # public_comment_Scheduler()

    print(UserList)
