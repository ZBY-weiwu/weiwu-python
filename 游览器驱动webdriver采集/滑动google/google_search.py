# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
from selenium.webdriver.support.select import Select
import os
import random



class GoogleSearch:
    def __init__(self):
        self.user_data = {"user": "15731624659", "pwd": "qq1161081779"}
        self.proxies_list = ["127.0.0.1:10809"]
        self.driver = webdriver.Chrome(chrome_options=self.chrome_Opthons())
        pass

    def chrome_Opthons(self):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1366,768")
        proxies =random.choice(self.proxies_list)
        chrome_options.add_argument("--proxy-server=http://{}".format(proxies))
        return chrome_options

    def user_search_Keyword(self,KeyWrod):
        # driver = webdriver.Chrome(chrome_options=self.chrome_Opthons())
        self.driver.get("https://www.google.com/search?q={}&tbm=nws&start=100".format(KeyWrod))
        js = "var q=document.documentElement.scrollTop=100000"
        self.driver.execute_script(js)
        # time.sleep(3)
        print(self.driver.title)
        time.sleep(100)
        self.driver.quit()

    def get_track(self,distance):  # distance为传入的总距离
        # 移动轨迹
        track = []
        # 当前位移
        current = 0
        # 减速阈值
        mid = distance * 4 / 5
        # 计算间隔
        t = 0.1
        # 初速度
        v = 500

        while current < distance:
            if current < mid:
                # 加速度为2
                a = random.randint(2, 7)
            else:
                # 加速度为-2
                a = -3
            v0 = v
            # 当前速度
            v = v0 + a * t
            # 移动距离
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移
            current += move
            # 加入轨迹
            track.append(round(move))
        return track

    def move_to_gap(self,slider, tracks):  # slider是要移动的滑块,tracks是要传入的移动轨迹
        ActionChains(self.driver).click_and_hold(slider).perform()
        for x in tracks:
            ActionChains(self.driver).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.driver).release().perform()

    def huakuai(self,KeyWrod):
        self.driver.get("https://www.google.com/preferences")
        huakuai = self.driver.find_element_by_xpath('//div[@class="goog-slider-thumb"]')
        self.move_to_gap(huakuai,self.get_track(340))
        time.sleep(0.5)
        js = "var q=document.documentElement.scrollTop=100000"
        self.driver.execute_script(js)
        time.sleep(1.5)
        self.driver.find_element_by_xpath('//*[@id="form-buttons"]/div[1]').click()
        self.user_search_Keyword(KeyWrod)

if __name__ == '__main__':

    google_search = GoogleSearch()
    google_search.huakuai("浙江 and 德清")