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
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

class Google_Spider(object):
    def __init__(self):
        pass
    def chrome_Opthons(self):
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--window-size=1366,768")

        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        # proxy = "127.0.0.1:10809"
        # chrome_options.add_argument("--proxy-server=%s" %proxy)
        return chrome_options

    def Download_HTML(self,Keyword):
        # driver = webdriver.Chrome(chrome_options=self.chrome_Opthons())
        driver = webdriver.Chrome(chrome_options=self.chrome_Opthons())

        driver.get("https://www.google.com/search?rlz=1C1CHWL_zh-CNUS967US967&tbm=nws&q={}".format(quote(Keyword)))
        wait = WebDriverWait(driver,10)
        input_keyword = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="input"]')))

        input_keyword.clear()

        login_click = wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="mKlEF"]')))
        login_click.click()
        print(driver.title)
        time.sleep(5)
        driver.quit()
google_spider = Google_Spider()
google_spider.Download_HTML("主力军")