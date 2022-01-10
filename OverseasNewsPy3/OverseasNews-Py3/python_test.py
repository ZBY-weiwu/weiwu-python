# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28
import json
import langid


from overseasnews.Tools.golaxy_gne import GeneralNewsExtractor
from overseasnews.Tools.golaxy_gne.Downloader.GolaxyRequests import GolaxyRequests
# title_xpath = "//h1/text()"
# content_xpath = "//div[@class=\"artcile\"]//div[@class=\"article_cont\"]"
# publish_time_xpath = "//div[@class=\"topcont clearfix\"]/span[3]//text()"
# with open("./html_test/缅华网.html","r+",encoding="utf-8") as f:
#     html = f.read()
# # body_xpath=content_xpath,
# data_obj = GeneralNewsExtractor().extract(html, title_xpath=title_xpath,body_xpath=content_xpath,
#                                           publish_time_xpath=publish_time_xpath)
# print(data_obj)


# import urllib
#
# fopen1 = urllib.urlopen('http://www.baidu.com').info()
# print (fopen1.getparam('charset'))

url = "https://www.washingtoninformer.com/elijah-cummings-mural-dedicated-in-baltimore/"
resp = GolaxyRequests.get(url)
html = resp.text
data_obj = GeneralNewsExtractor().extract(html,with_body_html=True)
data = (json.dumps(data_obj,ensure_ascii=False))
data_obj["publish_time"] = data_obj["publish_time"].replace("T"," ")
data_obj["publish_time"] = data_obj["publish_time"].replace("+"," ")
print(data)
print(data_obj["publish_time"])
lang_a = langid.classify(data_obj["publish_time"])
print(lang_a[0])
