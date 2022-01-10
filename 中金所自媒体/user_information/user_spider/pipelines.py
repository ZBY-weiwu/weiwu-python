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


from core.golaxy.spider import items as goalxy_item
from core.golaxy.spider import persistor
import requests,json,time


class UserInformationPipelines:

    @classmethod
    def process_item(self, item):

        d=goalxy_item.GolaxyUserInformation()
        d['id'] = item["id"]
        d['_ch'] = item["_ch"]
        d['media_id'] = item["media_id"]
        d['media_name'] = item["media_name"]
        d['uid'] = item["uid"]
        d['name'] = item["name"]
        d['screen_name'] = item["screen_name"]
        d['profile_url'] = item["profile_url"]
        d['description'] = item["description"]
        d['verified_reason'] = item["verified_reason"]
        d['verified'] = item["verified"]
        d['register_location'] = item["register_location"]
        d['register_time'] = item["register_time"]
        d['profile_image_url'] = item["profile_image_url"]
        d['statuses_count'] = item["statuses_count"]
        d['followers_count'] = item["followers_count"]
        d['friends_count'] = item["friends_count"]
        d['gender'] = item["gender"]
        d['extra_info'] = item["extra_info"]
        d['gather_time'] = int(time.time())*1000
        d['update_time'] = d['gather_time']
        d['insert_time'] = d['gather_time']
        # print("d_type:",d.item_type)
        # print("d_time:",json.dumps(d.item,ensure_ascii=False))
        # print("d_time:",d.item)
        persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item,d.item_type)


class UserBehavior:
    @classmethod
    def process_item(self, item):
        # print("item", json.dumps(item, ensure_ascii=False))

        d = goalxy_item.GolaxyUserBehaviorItem()

        d['id'] = item["id"]
        d['_key'] = item["_key"]
        d['_spec'] = item["_spec"]
        d['_ch'] = item["_ch"]
        d['media_id'] = item["media_id"]
        d['media_name'] = item["media_name"]
        d["comments_count"] = item.get("comments_count")
        d["likes_count"] = item.get("likes_count")
        d["dislikes_count"] = item.get("dislikes_count")
        d["share_count"] = item.get("share_count")
        d["reposts_count"] = item.get("reposts_count")
        d["views_count"] = item.get("views_count")
        d["attitudes_count"] = item.get("attitudes_count")

        print("d_type:", d.item_type)
        # print("d_time:", json.dumps(d.item, ensure_ascii=False))
        # print("d_time:", d.item)
        persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item, d.item_type)