# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28


import re
import random
import json
import time, datetime
import logging  # 引入logging模块
import os.path
import time
import configparser
import urllib3, requests
import dateutil.parser
import warnings



def Get_md5(url):
    import hashlib
    a = hashlib.md5(url.encode())
    md5_str = a.hexdigest()
    return md5_str

if __name__ == '__main__':
    pass
