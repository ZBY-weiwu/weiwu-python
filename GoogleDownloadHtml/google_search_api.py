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

from googlesearch import search
import pprint

list = search("高效码农",  num_results=100)
pprint.pprint(list)