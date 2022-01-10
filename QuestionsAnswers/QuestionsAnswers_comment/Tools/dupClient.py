#!/usr/bin/env python    
# -*- coding: UTF-8 -*-
import sys    
import requests
import json
import base64
import urllib

from urllib import parse
parse.quote
client=requests.session()

class DUPClient:
    def __init__(self):
        pass

    #channel通道，同一个channel名称，会放到一块。
    #boardId暂时不用    
    #cacheDay缓存天数，为0，则永久缓存，其他值则为缓存天数。
    #url和isMD5两个参数。如果url不是md5值，isMD5设置为true，接口会将url转成md5再去重
    def findAndSet(self, dupclient_url,channel, expire, url):

        d = {}
        d["channel"] = channel
        d["expire"] = expire
        d["target"] = url
        r = client.post(dupclient_url+'/golaxy/wde/crawler/deduplication/v1', data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json','Connection': 'keep-alive'}, timeout = 5000)
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

    def getPara(self,dupclient_url, channel, url):
        r = client.get(url =dupclient_url+"/golaxy/wde/crawler/deduplication/v1?channel="+channel+"&target="+parse.quote(url,'') , headers = {'Accept': 'application/json'}, timeout = 5000)
        d = json.loads(r.text)
        print("dupClient:",d)
        try:
            if d['targetExists']:
                return d['targetStatus']['params']
            else:
                return 'empty'
        except:
            return 'empty'

    def confirm(self,dupclient_url, channel, url,params="0"):
        d = {}
        d["channel"] = channel
        d["expire"] = 0
        d["target"] = url
        d["params"] = params
        r = client.put(dupclient_url+'/golaxy/wde/crawler/deduplication/v1', data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json','Connection': 'keep-alive'}, timeout = 5000)
#        print r.text
    
    def delete(self,dupclient_url, channel, url):
        '''
        d = {}
        d["channel"] = channel
        d["expire"] = 0
        d["target"] = base64.b64encode(url)
        '''
        url = dupclient_url+"/golaxy/wde/crawler/deduplication/v1/"+channel+"/"+base64.b64encode(url) 
        #r = requests.delete(url, data = json.dumps(d), headers = {'Accept': 'application/json','Content-Type': 'application/json'}, timeout = 5000)
        r = client.delete(url, headers = {'Accept': 'application/json','Content-Type': 'application/json','Connection': 'keep-alive'}, timeout = 5000)
#        print r.text
        

if __name__ == "__main__":
    client1 = DUPClient()
    print (client1.findAndSet('http://10.20.18.100:8799','newscrawler', 1, 'http://istock.jrj.com.cn/article_13350882.html'))
    print (client1.getPara('http://10.20.18.100:8799','newscrawler',  'http://www.hj.cn/news/p/791732.html'))
