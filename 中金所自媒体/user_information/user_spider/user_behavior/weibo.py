#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @创建时间 : 2020/6/18 09:49
# @爬虫作者 : SpiderMan
# @爬虫编码 :
# @执行频率 :
# @文件作用 :
# @其他说明 :
import random
import requests
import json
from fake_useragent import UserAgent
import time

class WeiboBehavior():
    def __init__(self, url,proxy=None, time_out=3, retry_times=3):
        self.url = url
        self.api = 'https://c.api.weibo.com/2/statuses/count/biz.json?access_token={}&ids={}'
        self.proxy = None if not proxy else {"http": proxy}
        self.time_out = time_out
        self.retry_times = retry_times
        # self.ua = UserAgent()
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'}
        # self.headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.72 Safari/537.36'
        self.max_code = 403
        self.max_txt = '达到最大重试次数'
        self.tomany_code = 500
        self.tomany_res = '传递参数超过限制'
        self.bad_token = 400
        self.bad_token_res = '当前token已失效'
        self.max_res = dict(code=self.max_code, message=self.max_txt, total=0, datas=[])
        self.token_list = ['2.00qeux5GEnpTBCe5c786bb86e2qsRB']


    def request(self, url, headers, method='GET', data=None, verify=True):
        for retry_time in range(0, self.retry_times):
            if method == 'GET':
                try :
                    resp = requests.get(url=url, headers=headers, timeout=self.time_out, proxies=self.proxy, verify=verify)

                    return resp
                except Exception as e:
                    continue
            else:
                try :
                    resp = requests.post(url=url, headers=headers, timeout=self.time_out, proxies=self.proxy, data=data, verify=verify)
                    return resp
                except Exception as e:
                    continue

    def trans_time(self, time_str):
        struct_time = time.strptime(time_str, '%a %b %d %H:%M:%S %z %Y')
        t = time.mktime(struct_time)
        return t

    def parse_data(self, resp):
        try:
            json_data = resp.json()
        except:
            json_data = {}

        if isinstance(json_data, list):
            empty_list = []
            for data_info in json_data:
                weibo_info = dict(
                    id=data_info.get('idstr', ''),  # 微博ID
                    title='',
                    content='',
                    author='',
                    publish_time=0,  # 创建时间 需要转格式
                    forward=int(data_info.get('reposts', 0)),  # 转发
                    comment=int(data_info.get('comments', 0)),  # 评论
                    like=int(data_info.get('attitudes', 0)),  # 点赞
                    read=0)

                empty_list.append(weibo_info)
            total = len(empty_list)
            result_dict = dict(code=resp.status_code, message='success', datas=empty_list, total=total)
            return result_dict
        else:
            result_dict = self.max_res
        return result_dict

    def weibo(self):
        token = random.choice(self.token_list)
        url = self.api.format(token, self.url)
        print(url)
        resp = self.request(url=url, headers=self.headers)
        if not resp:
            result_dict = self.max_res
            return result_dict
        if resp.text:
            result_dict = self.parse_data(resp)
        else:
            result_dict = self.max_res
        return result_dict

    def run(self):
        result = self.weibo()
        return result


if __name__ == '__main__':

    # url = "4519641491857024,4520136784982635,4516046692942889,4509898404454932,4375607116565612,4507015894228296,4506646188218361,4506601685356860,4504307276571276,4460390178502053,4504129428484398,4503604831405068,4494240933299890,4494087355094812,4494117134355636,4487786508320714,4475863661881105,4493312566120282,4492477170017573,4484336004605481,4472602255359256,4471260887551137,4491762695276153,4491762079280990,4491829112406361,4491833004953770,4491833650782625,4491833708775109,4519641491857024,4520136784982635,4516046692942889,4509898404454932,4375607116565612,4507015894228296,4506646188218361,4506601685356860,4504307276571276,4460390178502053,4504129428484398,4503604831405068,4494240933299890,4494087355094812,4494117134355636,4487786508320714,4475863661881105,4493312566120282,4492477170017573,4484336004605481,4472602255359256,4471260887551137"

    url = '4617540770729849'
    # url = "4519641491857024,4520136784982635,4516046692942889,4509898404454932,4375607116565612,4507015894228296,4506646188218361,4506601685356860,4504307276571276,4460390178502053,4504129428484398,4503604831405068,4494240933299890,4494087355094812,4494117134355636,4487786508320714,4475863661881105,4493312566120282,4492477170017573,4484336004605481,4472602255359256,4471260887551137,4491762695276153,4491762079280990,4491829112406361,4491833004953770,4491833650782625,4491833708775109,"
    # url = "4506601685356860,4504307276571276,4506601685356860,4504307276571276,4460390178502053,4504129428484398,4503604831405068,4494240933299890,4494087355094812,4494117134355636,4487786508320714,4475863661881105,4493312566120282,4492477170017573,4484336004605481,4472602255359256,4471260887551137,4491762695276153,4491762079280990,4491829112406361,4491833004953770,4491833650782625,4491833708775109,4519641491857024,4520136784982635,4516046692942889,4509898404454932,4375607116565612,4507015894228296,4506646188218361,4506601685356860,4504307276571276,4460390178502053,4504129428484398,4503604831405068,4494240933299890,4494087355094812,4494117134355636,4487786508320714,4475863661881105,4493312566120282,4492477170017573,4484336004605481,4472602255359256,4471260887551137,4491762695276153,4491762079280990,4491829112406361,4491833004953770,4491833650782625,4491833708775109,4522544361964339,"
    # url = "4522650494369316"
    news = WeiboBehavior(url=url)
    # news.run()
    print(json.dumps(news.run(),ensure_ascii=False))
    # print(len(url.split(',')))



