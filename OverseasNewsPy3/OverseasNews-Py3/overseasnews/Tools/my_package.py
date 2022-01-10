# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28
import re

import time, datetime
import configparser
import dateutil.parser
import warnings
import requests
import json
import logging
import base64
import tldextract
from urllib import parse

warnings.filterwarnings("ignore")

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

def replace_by_img_tag(txt):
    begin = 0
    end = 0
    i = 1
    while True:
        end = txt.find('{img}', begin)
        if end == -1:
            break
        new = '\n{IMG:' + str(i) + '}\n'
        txt = txt.replace('{img}', new, 1)
        begin = end + len(new)
        i = i + 1
    return txt

# 日志
def get_logger(logger_name, log_file, level=logging.INFO):
    conf = configparser.ConfigParser()
    conf.read("./config/config.ini", encoding="utf-8")
    logger_path = conf.get("LoggerPath", "logger_path")
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_file, mode='w')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)

    return logging.getLogger(logger_name)

def get_task():

    tasks_list =[]

    url = "http://data-service.golaxy.cn:8080/management/crawler/account/v2/queryTasks?sid={}&update=1&taskType={}"
    print("task_url:",url)
    resp = requests.get(url)
    datas = resp.json()
    api_tasks = datas.get("tasks")
    for task in api_tasks:
        task_dict = dict(
        site_name = task.get("media_name"),
        media_id = task.get("media_id"),
        board_id = task.get("board_id"),
        board_name = task.get("board_name"),
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


def Get_md5(url):
    import hashlib
    a = hashlib.md5(url.encode())
    md5_str = a.hexdigest()
    return md5_str

def golaxy_translate(cont):
    headers = {'cache-control': 'no-cache', 'content-type': 'application/x-www-form-urlencoded',
               'postman-token': '3ce3664f-fad5-3792-aed7-0faf7e4a489e'}
    if cont:
        payload = 'from=auto&to=zh&engine=baidu&content=' + cont
        while True:
            try:
                res = requests.request('POST', "http://data-service.golaxy.cn:8080/golaxy-fanyi-api/translate",
                                       headers=headers, data=payload.encode('utf-8').decode('latin-1'), timeout=60)
                trans_data = json.loads(res.text)
                trans_content = trans_data["translateResult"]
                return trans_content.strip()
            except:
                pass

# 判断是会否是标准url
def Is_url(url)->bool:
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    if len(regex.findall(url))==0:
        return True
    else:
        return False

# 黑名单url
def blacklist_url(url)->bool:
    blacklist = ["twitter","instagram","youtube","facebook","google",".pdf"]
    for black_url in blacklist:
        if re.findall(black_url,url):
            return True
    else:
        return False

def parse_publish_time(pubtime, pubtime_xpath=None)->int:

    if pubtime_xpath:
        pubtime = golaxy_translate(pubtime_xpath)
    else:
        pubtime = pubtime.replace("T", " ")
        pubtime = pubtime.replace("+", " ")
    pubtime = str_to_timestamp(pubtime)

    return pubtime

def domain_extraction1(url):
    val = tldextract.extract(url)
    return val.domain

class DUPClient:
    def __init__(self):
        self.client = requests.session()
        pass

    # channel通道，同一个channel名称，会放到一块。
    # boardId暂时不用
    # cacheDay缓存天数，为0，则永久缓存，其他值则为缓存天数。
    # url和isMD5两个参数。如果url不是md5值，isMD5设置为true，接口会将url转成md5再去重
    def findAndSet(self, dupclient_url, channel, expire, url):
        return False
        d = {}
        d["channel"] = channel
        d["expire"] = expire
        d["target"] = url
        r = self.client.post(dupclient_url + '/golaxy/wde/crawler/deduplication/v1', data=json.dumps(d),
                        headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                 'Connection': 'keep-alive'}, timeout=5000)
        d = json.loads(r.text)
        if d['code'] == 0:
            try:
                if (d['message'] == 'SUCESS'):
                    return d['targetExists']
                else:
                    return True
            except:
                return True
        else:
            return True

    def getPara(self, dupclient_url, channel, url):
        r = self.client.get(
            url=dupclient_url + "/golaxy/wde/crawler/deduplication/v1?channel=" + channel + "&target=" + parse.quote(
                url, ''), headers={'Accept': 'application/json'}, timeout=5000)
        d = json.loads(r.text)
        print("dupClient:", d)
        try:
            if d['targetExists']:
                return d['targetStatus']['params']
            else:
                return 'empty'
        except:
            return 'empty'

    def confirm(self, dupclient_url, channel, url, params="0"):
        return
        d = {}
        d["channel"] = channel
        d["expire"] = 0
        d["target"] = url
        d["params"] = params
        r = self.client.put(dupclient_url + '/golaxy/wde/crawler/deduplication/v1', data=json.dumps(d),
                       headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                'Connection': 'keep-alive'}, timeout=5000)

    #        print r.text

    def delete(self, dupclient_url, channel, url):
        '''
        d = {}
        d["channel"] = channel
        d["expire"] = 0
        d["target"] = base64.b64encode(url)
        '''
        print("delete_url:",url)
        url = dupclient_url + "/golaxy/wde/crawler/deduplication/v1/" + channel + "/" + base64.b64encode(url)
        # r = requests.delete(url, data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
        r = self.client.delete(url, headers={'Accept': 'application/json', 'Content-Type': 'application/json',
                                        'Connection': 'keep-alive'}, timeout=5000)


proxies_list = [{'http': 'http://192.168.1.44:1081', 'https': 'https://192.168.1.44:1081'}]

if __name__ == '__main__':
    # print(golaxy_translate("English"))
    # # javascript:
    # print(domain_extraction1("javascript;"))

    print(blacklist_url("https://www.runoob.com/python3/python-quicksort.html"))
