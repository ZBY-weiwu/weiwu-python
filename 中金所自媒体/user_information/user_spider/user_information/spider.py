# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import requests
import json
from user_spider.user_information.weibo import WeiboInformation
from user_spider.pipelines import UserInformationPipelines

toutiao_url = "https://profile.zjurl.cn/rogue/ugc/profile/?user_id=105220535018&media_id=1614254699279364&request_source=1"
toutiao_url = "https://profile.zjurl.cn/rogue/ugc/profile/?user_id=102913575337&media_id=1614254699279364&request_source=1"

guba_url = "https://i.eastmoney.com/6176326305794400"
xueqiu_url = "https://xueqiu.com/u/5996592085"


class UserInformationSpider:

    def __init__(self, list_seed):
        self.headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
        self.index_url = "http://10.20.18.10:30086/golaxy/wde/dataservice/v1/wemediaUser/baseinfo"
        self.list_seed = list_seed

    def get_wemedia_user(self, url):
        data = {"url": url}
        resp = requests.post(self.index_url, headers=self.headers, data=data)
        try:
            return resp.json()
        except:
            return {}

    def get_weibo_user(self, url):
        return WeiboInformation(url).run()

    def parse(self, seed_data, resp):
        # print("seed_data:",seed_data)
        resp["media_id"] = seed_data["site_id"]
        resp["media_name"] = seed_data["site_name"]
        resp["profile_url"] = seed_data["profile_url"]
        resp["channel"] = seed_data["channel"]
        return resp

    def item(self, seed_data, resp):
        user_obj = self.parse(seed_data, resp)

        user_info = user_obj.get("datas") or user_obj.get("data")
        if not user_info:
            return
        list_item = []
        if isinstance(user_info, list):
            for user_data in user_info:
                item = {}
                item["uid"] = str(user_data.get("uid"))
                item["_ch"] = user_obj['channel']
                item["id"] = str(item["_ch"]) + item["uid"]
                item["media_id"] = str(user_obj["media_id"])
                item["media_name"] = user_obj["media_name"]
                item["profile_url"] = user_obj["profile_url"]
                item["name"] = user_data.get("user_name")
                item["screen_name"] = user_data.get('screen_name') or ''
                item["description"] = user_data.get("user_info") or ''
                item["verified_reason"] = user_data.get("desc") or user_data.get("verified_info") or ''
                if len(item["verified_reason"]) > 0:
                    item["verified"] = True
                else:
                    item["verified"] = False
                item["register_location"] = user_data.get("area") or ''
                item["register_time"] = int(user_data.get("create_time"))
                item["profile_image_url"] = user_data.get("user_img") or ''
                item["statuses_count"] = user_data.get("statuses_count") or 0
                item["followers_count"] = user_data.get("fans_count") or 0
                item["friends_count"] = user_data.get("follow_count") or 0
                item["gender"] = user_data.get("gender") or -1

                extra_info_list = []
                extra_info = {}
                extra_info["visits_count"] = user_data.get("visits_count") or 0
                extra_info["like_count"] = user_data.get("like_count") or 0
                extra_info["video_total_counter"] = user_data.get("video_total_counter") or 0

                extra_info_list.append(extra_info)
                item["extra_info"] = json.dumps(extra_info_list)
                list_item.append(item)

        elif isinstance(user_info, dict):
            user_data = user_info
            item = {}
            item["uid"] = str(user_data.get("uid"))
            item["_ch"] = user_obj['channel']
            item["id"] = str(item["_ch"]) + item["uid"]
            item["media_id"] = str(user_obj["media_id"])
            item["media_name"] = user_obj["media_name"]
            item["profile_url"] = user_obj["profile_url"]
            item["name"] = user_data.get("user_name")
            item["screen_name"] = user_data.get('screen_name') or ''
            item["description"] = user_data.get("user_info") or ''
            item["verified_reason"] = user_data.get("desc") or user_data.get("verified_info") or ''
            if len(item["verified_reason"]) > 0:
                item["verified"] = True
            else:
                item["verified"] = False
            item["register_location"] = user_data.get("area") or ''
            # print("user_data:",user_data)
            try:
                item["register_time"] = int(user_data.get("create_time")) * 1000
            except:
                return
            item["profile_image_url"] = user_data.get("user_img") or ''
            item["statuses_count"] = user_data.get("statuses_count") or 0
            item["followers_count"] = user_data.get("fans_count") or 0
            item["friends_count"] = user_data.get("follow_count") or 0
            item["gender"] = user_data.get("gender") or -1
            extra_info_list = []
            extra_info = {}
            extra_info["visits_count"] = user_data.get("visits_count") or 0
            extra_info["like_count"] = user_data.get("like_count") or 0
            extra_info["video_total_counter"] = user_data.get("video_total_counter") or 0
            extra_info_list.append(extra_info)
            item["extra_info"] = json.dumps(extra_info_list)
            list_item.append(item)
        return list_item

    def Engine(self):
        for seed_data in self.list_seed:
            if seed_data["site_id"] == 55130:
                url = seed_data["uid"]
                items = self.item(seed_data, self.get_weibo_user(url))
            elif seed_data["site_id"] == 33798:
                url = "https://profile.zjurl.cn/rogue/ugc/profile/?user_id={}&media_id=0&request_source=1".format(
                    seed_data["uid"])
                items = self.item(seed_data, self.get_wemedia_user(url))
            else:
                url = seed_data["profile_url"]
                items = self.item(seed_data, self.get_wemedia_user(url))
            if not items:
                return
            for item in items:
                UserInformationPipelines.process_item(item)

    def run_Engine(self):
        self.Engine()


