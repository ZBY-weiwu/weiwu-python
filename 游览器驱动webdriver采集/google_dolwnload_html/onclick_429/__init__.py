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

from PyQt5.QtWidgets import *
import sys


def onclick_429(self, wait):
    time.sleep(4)
    click_429 = wait.until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]')))
    click_429.click()
    # var q=document.getElementById('recaptcha-anchor-label').click()
    js2 = "var q=document.getElementById('recaptcha-anchor').click()"
    self.driver.execute_script(js2)
    time.sleep(3)