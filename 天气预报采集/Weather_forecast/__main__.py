# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/9/28

from .weather_forecast import WeatherSpider
if __name__ == '__main__':
    weather_spider = WeatherSpider()
    weather_spider.download_city()

