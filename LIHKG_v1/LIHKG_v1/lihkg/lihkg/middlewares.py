# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import random
from lihkg.settings import IPPOOL
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
ua = UserAgent()

class RotateUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        self.user_agent = user_agent

    def process_request(self, request, spider):
        #print ('-----:',ua.chrome)
        request.headers.setdefault('User-Agent', ua.chrome)


class proxMiddleware(object):
    proxy_list=["https://192.168.1.10:1081","https://192.168.1.10:1081"]
    def process_request(self,request,spider):
        # if not request.meta['proxies']:
        ip = random.choice(self.proxy_list)
        print (ip)
        request.meta['proxy'] = ip

class MyproxiesSpiderMiddleware(object):

    def __init__(self,ip=''):
        self.ip=ip

    def process_request(self, request, spider):
        thisip=random.choice(IPPOOL)
        request.meta["proxy"]=thisip["ipaddr"]
