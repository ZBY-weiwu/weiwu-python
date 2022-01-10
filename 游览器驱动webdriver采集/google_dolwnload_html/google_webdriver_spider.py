# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin
import urllib
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
import time
import sys
from selenium.webdriver.support.select import Select
import os
import random
from golaxy_package import Get_md5


class GoogleSearch:
    def __init__(self):
        self.proxies_list = ["127.0.0.1:10809"]
        self.driver = webdriver.Chrome(chrome_options=self.chrome_Opthons())
        self.page_count = 1
        pass

    def chrome_Opthons(self):
        chrome_options = Options()
        chrome_options.add_argument("--window-size=1366,768")
        proxies =random.choice(self.proxies_list)
        path = r"C:\Users\BACK\AppData\Local\Google\Chrome\User Data"
        chrome_options.add_argument("--user-data-dir="+path)
        # chrome_options.add_argument("--proxy-server=http://{}".format(proxies))
        return chrome_options

    def read_keywords(self):
        f = open("./keysword.txt","r",encoding="utf-8")
        return f.readlines()

    # 跳转429
    # https://www.google.com/sorry/index?continue=https://www.google.com/search%3Fq%3DAnhui%2BNew%2BMaterials%26rlz%3D1C1CHWL_zh-CNUS967US967%26oq%3DAnhui%2BNew%2BMaterials%26aqs%3Dchrome..69i57j69i59j0i8i30l3j0i8i10i30j0i8i30l3j0i8i10i30.901j0j7%26sourceid%3Dchrome%26ie%3DUTF-8&q=EgQBqigHGOeygY0GIhAYctydJzLI9-4qMmH4L2JzMgFy
    def code_429(self,response)->bool:
        resp = "".join(re.findall("此网页用于确认这些请求是由您而不是自动程序发出的",response))
        print("response",resp)
        if len(resp)>10:
            return True
        else:
            return False

    def onclick_429(self,wait):
        # https://google.com/recaptcha/api2/demo
        url = "https://www.google.com/search?q=Anhui%20Cell%0A&amp;tbm=nws&amp;start=0"
        self.driver.get(url)
        time.sleep(2)
        click_429 = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]')))
        click_429.click()
        # var q=document.getElementById('recaptcha-anchor-label').click()
        js2 = "var q=document.getElementById('recaptcha-anchor').click()"
        self.driver.execute_script(js2)
        time.sleep(3)
    def onclick2_429(self,wait):
        # time.sleep(4)
        print(1)
        oncklik = self.driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]')
        print(2,oncklik)
        # # var q=document.getElementById('recaptcha-anchor-label').click()
        # js2 = "var q=document.getElementById('recaptcha-anchor').click()"
        # self.driver.execute_script(js2)
        # time.sleep(3)


    def write_file(self,file_name,html):
        f = open("./all_HTML/"+file_name+".html","w+",encoding="utf-8")
        f.write(html)

    # 检查下一页是否存在
    def next_page_really(self,page_html)->bool:
        html_data = etree.HTML(page_html)
        next_page = "".join(html_data.xpath('//*[@id="pnnext"]//text()'))
        if next_page == "下一页":
            return True
        else:
            return False

    # 循环点击下一页解析
    def Next_Pgae_Callback(self,page_count,KeyWrod,wait):
        page_count +=1
        html_data = etree.HTML(self.driver.page_source)
        if self.next_page_really(self.driver.page_source):
            """点击第一种方法"""
            # next_page_click = wait.until(
            #     EC.presence_of_element_located((By.XPATH, '//*[@id="pnnext"]')))
            # next_page_click.click()
            """第二种点击事件触发方法"""
            js2 = "var q=document.getElementById('pnnext').click()"
            self.driver.execute_script(js2)
            print("点击下一页")
            self.down_html(html_data, KeyWrod,page_count)
            self.Next_Pgae_Callback(page_count,KeyWrod,wait)

    # 下载html
    def down_html(self,html_data,KeyWrod,page_count):
        link_list = html_data.xpath('//*[@id="rso"]/div/g-card/div/div/a/@href')
        if len(link_list) > 0:
            print("KeyWrod:", KeyWrod)
            time.sleep(3)
            file_name = Get_md5(KeyWrod)+"_"+str(page_count)
            self.write_file(file_name, self.driver.page_source)

    # 判断关键词关系：relation
    def user_search_Keyword(self,KeyWrod=None,relation="and",Search_method="intext:"):
        wait = WebDriverWait(self.driver, 10)
        keyword_list = self.read_keywords()

        for KeyWrod in keyword_list:
            if relation=="and":
                KeyWrod = KeyWrod.replace(" "," AND ")
            elif relation=="or":
                KeyWrod = KeyWrod.replace(" ", " OR ")
            Keywrod = Search_method+urllib.parse.quote(KeyWrod)
            time.sleep(10)
            try:
                self.driver.get("https://www.google.com/search?q={}&tbm=nws&start=0".format(Keywrod))
                if self.code_429(self.driver.page_source):
                    print("网页code：429")
                    sys.exit()
                    self.onclick_429(wait)
                    # self.onclick2_429(wait)
            except:
                print("error->keyword{}".format(KeyWrod))
                continue

            html_data = etree.HTML(self.driver.page_source)
            self.down_html(html_data, KeyWrod,self.page_count)
            if self.next_page_really(self.driver.page_source):
                self.Next_Pgae_Callback(self.page_count,KeyWrod,wait)
        self.driver.quit()

if __name__ == '__main__':
    GoogleSearch().user_search_Keyword()