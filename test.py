# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28
import re
import eventlet,time
url = "https://www.jianshu;.com/p/5a020c46142e"
regex = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
print(regex.findall(url))

proxy_enabled = 1
js_enabled = 0
media_name = "sdas"
board_name = "3223"
media_id = 2
entry_url ="www.baidu.com"
location = "其他"
extractor_config = "ppppp"

domain_url = "baidu.com"
a = """({board_name}, 4, {entry_url}, {domain_url}, {location}, 'ppp', {media_id}, {media_name}, 7, '2021-12-20 18:22:47.000', '2021-08-18 18:22:47.000', 'jss', NULL, 180, 0, {js_enabled}, 0, {proxy_enabled}, 0, {extractor_config}, 0, '', NULL, NULL, 0, 0, '{{jss}}', NULL, NULL, false, NULL, '', NULL, NULL, false, NULL, NULL);""".format(proxy_enabled=proxy_enabled,js_enabled=js_enabled,media_name=media_name,board_name=board_name,media_id=media_id,entry_url=entry_url,location=location,extractor_config=extractor_config,domain_url=domain_url)
print(a)