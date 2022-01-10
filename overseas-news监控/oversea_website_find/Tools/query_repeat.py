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
import tldextract


def query_file():
    query_site_file =open("overseanews-all.json","r+",encoding="utf-8")
    datas= query_site_file.read()
    datas_obj = json.loads(datas)
    query_list = datas_obj["RECORDS"]
    site_file = open("../output/oversea_site.json","r+",encoding="utf-8")
    site_all = site_file.readlines()
    for site_data in site_all:
        site_data = (json.loads(site_data.strip()))
        site_url = site_data["site_url"]
        site_domain_name = domain_name(site_url)
        Query_Wrong = False
        for query_data in query_list:
            if site_domain_name in query_data["entry_url"]:
                Query_Wrong =True
                break

        if Query_Wrong:
            continue

        Deposit_data = open("../output/整理好的网站/world68.json", "a+", encoding="utf-8")
        site_item = json.dumps(site_data,ensure_ascii=False)
        Deposit_data.write(site_item+"\n")
        Deposit_data.close()


    # 域名提取
def domain_name(site_url):
    val = tldextract.extract(site_url)

    site_domain_name = "{0}.{1}".format(val.domain, val.suffix)

    return site_domain_name





if __name__ == '__main__':
    query_file()