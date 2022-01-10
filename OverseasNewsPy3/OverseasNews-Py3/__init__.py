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


class QlineEditMask(QWidget):
    def __init__(self):
        super(QlineEditMask, self).__init__()
        self.initUI()
