#!/usr/bin/env python    
# -*- coding: UTF-8 -*-
import sys    
import requests
import json
import base64
import urllib
from scrapy.utils.project import get_project_settings


class DUPClient:
    def __init__(self):
        settings = get_project_settings()
        self.DistinctEntry= settings.get('DUP_URL')+"/golaxy/wde/crawler/deduplication/v1"

    #channel通道，同一个channel名称，会放到一块。
    #boardId暂时不用    
    #cacheDay缓存天数，为0，则永久缓存，其他值则为缓存天数。
    #url和isMD5两个参数。如果url不是md5值，isMD5设置为true，接口会将url转成md5再去重
    def findAndSet(self, channel, expire, url):
        return False
        d = {}
        d["channel"] = channel
        d["expire"] = expire
        d["target"] = url
        d["params"] = "0"
        r = requests.post(self.DistinctEntry, data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
        d = json.loads(r.text)
        if d['code'] == 0:
            try:
                if(d['message'] == 'SUCESS'):
                    return d['targetExists']
                else:
                    return True
            except:
                return True
        else:
            return True

    def getPara(self, channel, url):
        rurl = self.DistinctEntry+"?channel="+channel+"&target="+urllib.quote(url,'')
        r = requests.get(url = rurl, headers = {'Accept': 'application/json'}, timeout = 5000)
        d = json.loads(r.text)
        if d['targetExists']:
            return d['targetStatus']['params']
        else:
            return 0


    def confirm(self, channel, url, params='0'):
        return 
        d = {}
        d["channel"] = channel
        d["expire"] = 0
        d["target"] = url
        d["params"] = params
    #    print "url=",url
#        print "d=",d
        r = requests.put(self.DistinctEntry, data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
#        print "confirm=",r.text
	
    
    def delete(self, channel, url):
        '''
        d = {}
        d["channel"] = channel
        d["expire"] = 0
        d["target"] = base64.b64encode(url)
        '''
        #url = "http://192.168.200.230:8793/golaxy/wde/crawler/deduplication/v1/"+channel+"/"+base64.b64encode(url) 
        rurl = self.DistinctEntry+"?channel="+channel+"&target="+urllib.quote(url)
        #r = requests.delete(url, data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
        r = requests.delete(rurl, headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
#        print r.text
        

if __name__ == "__main__":
    client = DUPClient()
    print client.findAndSet('bbs', 60, 'http://istock.jrj.com.cn/article,600019,13350880.html')
    client.confirm('bbs', 'http://istock.jrj.com.cn/article,600019,13350880.html')
    client.delete('bbs', 'http://istock.jrj.com.cn/article,600019,13350880.html')
