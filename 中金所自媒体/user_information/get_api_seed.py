# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/1
import requests,json
import time
from user_spider.user_information.spider import UserInformationSpider
from user_spider.user_behavior.spider import UserBehaviorSpider
from user_spider.task_handle.get_task import GetTask

class GetUserBehavior:

    @classmethod
    def user_behavior_scheduling(cls):
        url = '4617540770729849'  # weibo
        while True:
            time.sleep(1)
            item_list = GetTask.get_user_behavior_task()
            for data in item_list:
                url = data["url"]
                UserBehaviorSpider.run_Engine(url=url)

class GetUserinformation:
    # 1：帖子或视频信息；2：用户信息；3：粉丝；4：好友；5：转发；6：评论；7：点赞 8：群组信息；9：成员信息
    api_url = "http://data-service.golaxy.cn:8080/management/crawler/account/v1/queryTasks?sid={}&update=1&taskType={}"
    seedlist_id = [33798,25953,7010,55130]
    # seedlist_id = [55130]
    @classmethod
    def get_seed(cls,task_id,**kwargs):
        url = cls.api_url.format(task_id,2)
        resp = requests.get(url,**kwargs)
        return resp.json()

    @classmethod
    def task_scheduling(cls):
        while True:
            for task_id in cls.seedlist_id:
                time.sleep(1)
                # print(json.dumps(cls.get_seed(task_id).get("tasks"),ensure_ascii=False))
                UserInformationSpider(cls.get_seed(task_id).get("tasks")).run_Engine()


if __name__ == '__main__':
    GetUserinformation.task_scheduling()
    # GetUserBehavior.user_behavior_scheduling()
