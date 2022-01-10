# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28
import re
import time, datetime
import dateutil.parser
import requests
import json
import tldextract


def domain_extraction1(url):
    val = tldextract.extract(url)
    return val.domain

def parse_publish_time(pubtime, pubtime_xpath=None)->int:

    if pubtime_xpath:
        pubtime = golaxy_translate(pubtime_xpath)
    else:
        pubtime = pubtime.replace("T", " ")
        pubtime = pubtime.replace("+", " ")
    pubtime = str_to_timestamp(pubtime)

    return pubtime
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