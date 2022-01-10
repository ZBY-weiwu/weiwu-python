# -*- coding: utf-8 -*-
import time
import re
import requests
import sys
import datetime
from fake_useragent import UserAgent
import dateutil.parser
ua = UserAgent()

def date_to_timestamp(date, format_string="%Y-%m-%d %H:%M:%S"):
    time_array = time.strptime(date, format_string)
    time_stamp = int(time.mktime(time_array))
    return time_stamp


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
    m = None
    if not isParse:
        m = re.search(r'(\d+)\s*秒前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))
    if not isParse:
        m = re.search(r'(\d+)\s*分钟前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60
    if not isParse:
        m = re.search(r'(\d+)\s*小时前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60
    if not isParse:
        m = re.search(r'(\d+)\s*天前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60*24
    if not isParse:
        m = re.search(r'(\d+)\s*个月前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60*24*30
    if not isParse:
        m = re.search(r'今天\s*(\d+):(\d+)', date, re.M|re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                hour = m.group(1)
            if m.group(2):
                minute = m.group(2)
            s = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
            d =  dateutil.parser.parse(s,fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search(r'(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?', date, re.M|re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                year = m.group(1)
                if len(str(year))==2:
                    year = "20"+year
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
            s = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
            d =  dateutil.parser.parse(s,fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search( r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2}\w\d{1,2}:\d{1,2}:\d{1,2})', date, re.M|re.I)
        if m:
            isParse = True
            date = m.group()
            d =  dateutil.parser.parse(date,fuzzy=True)
            t = int(time.mktime(d.timetuple()))
            if t < now:
                now = t
    return now

def requests_parse(url,headers={"User-Agent": ua.chrome}):
    req = requests.get(url=url,headers =headers,timeout=10)
    try:
        if req.status_code == 200:
            #req.encoding = "utf-8"
            response = req.text
            page = tran2UTF8(response)
            return response
    except:
        return

def B_request(xpath_content,resp):
     #try:
     if True:
         #html = etree.HTML(resp,parser=etree.HTMLParser(encoding='utf-8'))
         html = etree.HTML(resp)
         content = html.xpath(xpath_content+"//text()")
         content = "".join(content).encode('utf-8')
         return content

def replace_by_img_tag(txt):
    begin = 0 
    end = 0 
    i = 1 
    while True:
        end = txt.find('{img}', begin)
        if end == -1: 
            break
        new = '\n{IMG:'+str(i)+'}\n'
        txt = txt.replace('{img}', new, 1)
        begin = end + len(new)
        i = i + 1 
    return txt

def replace_by_video_tag(txt):
    begin = 0
    end = 0
    i = 1
    while True:
        end = txt.find('{video}', begin)
        if end == -1:
            break
        new = '\n{VIDEO:'+str(i)+'}\n'
        txt = txt.replace('{video}', new, 1)
        begin = end + len(new)
        i = i + 1
    return txt

#print str_to_timestamp('2018-08-29T05:09:00Z')
def str2int(s):
    #s = 13.4w
    s=s.strip()
    if len(s) == 0:
        return 0
    i = 0 
    pos = s.find('w')
    if pos != -1: 
        i = int( float(s[0:pos])*10000 )
    else:
        i = int(s)
    return i

