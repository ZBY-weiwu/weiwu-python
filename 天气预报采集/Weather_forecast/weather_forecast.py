from requests_html import HTMLSession
from urllib.parse import urljoin
from urllib.parse import unquote
import requests
import re
from fake_useragent import UserAgent
# from .wemedia_parse import *
from tenacity import retry, stop_after_attempt
import sys
import logging
from lxml import etree
import json
logger = logging.getLogger(__name__)
url = "http://guba.eastmoney.com/interface/GetData.aspx"
from Weather_forecast.text_cody_v1 import by_requests as GolaxyDownload
#

ua = UserAgent(path='fake_useragent.json').random
print(ua)

class WeatherSpider:

    def __init__(self):
        # 地区
        self.RegionApi = "https://weather.cma.cn/api/dict/province/{}"
        # 天气
        self.WeatherApi = "https://weather.cma.cn/api/now/{}"

    def download_city(self):
        code_distinguish = GolaxyDownload(call_proxy=0)
        url = "https://weather.cma.cn/web/weather/58238.html"
        CD = code_distinguish.get(url)
        html = etree.HTML(CD)
        city_html_list = html.xpath("//*[@id=\"cityPosition\"]/div[3]/ul/li")

        for city_data in city_html_list:

            city_valud=city_data.xpath("./@data-value")[0]
            region_resp = code_distinguish.get(self.RegionApi.format(city_valud))
            region_info_obj = json.loads(region_resp)
            region_info_list=region_info_obj.get("data").split("|")
            for region in region_info_list:
                region_data_info = region.split(",")

                region_valud = region_data_info[0]
                region_name = region_data_info[1]
                tianqi_resp = code_distinguish.get(self.WeatherApi.format(region_valud))
                tianqi_obj = json.loads(tianqi_resp)
                tianqi_data = tianqi_obj.get("data")
                item= {}
                item["城市"] = tianqi_data.get("location").get("path").replace(", ","-")
                item["降水量"] = tianqi_data.get("now").get("precipitation")
                item["温度"] = tianqi_data.get("now").get("temperature")
                item["气压指数"] = tianqi_data.get("now").get("pressure")
                item["湿度指数"] = tianqi_data.get("now").get("humidity")
                item["风向"] = tianqi_data.get("now").get("windDirection")
                item["风向度"] = tianqi_data.get("now").get("humidity")
                item["风速"] = tianqi_data.get("now").get("windSpeed")
                item["风标"] = tianqi_data.get("now").get("windScale")
                item["天气预报更新时间"] = tianqi_data.get("lastUpdate")

                item_data= json.dumps(item,ensure_ascii=False)
                print(item_data)
                self.write_file(item_data)


    def write_file(self,item):
        f = open("./output/天气数据v1.json","a+",encoding="utf-8")
        f.write(item+"\n")
if __name__ == '__main__':
    weather_spider = WeatherSpider()
    weather_spider.download_city()
