#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import os,re
import chardet
from fake_useragent import UserAgent
import json
import logging
from lihkg.items import DetailItem
from lihkg.items import reply_Item
import copy
import urllib3
import urllib
import time
import sys
from util.langconv import *
from util.MD5 import MD5
from util.tool import *
from util.nlp_server import NLP_server
from util.spiderCFG import *
ua = UserAgent()
md5 = MD5()
logger = logging.getLogger("LIHKG_spider")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def Traditional2Simplified(sentence):
    sentence = Converter('zh-hans').convert(sentence)
    return sentence

class Lihkg_Spider(scrapy.Spider):
    name = 'lihkg_spider'
    def __init__(self,cfg):
        self.cfg_list = []
        self.headers = {"User-Agent": ua.chrome,"referer":"https://lihkg.com"}
        self.readTaskFromJson("seed/"+cfg+".txt")
        filehandler = logging.handlers.TimedRotatingFileHandler("logs/"+cfg+".log", when='H', interval=1, backupCount=7)
        filehandler.suffix = "%Y-%m-%d_%H-%M-%S"
        FORMAT="%(asctime)s %(levelname)s %(pathname)s:%(lineno)d [appnewsarticles]:%(message)s"
        filehandler.setFormatter(logging.Formatter(FORMAT))
        logger.addHandler(filehandler)

    def readTaskFromJson(self, filename):
        f = open(filename)
        seedcontent = f.read()
        configlist = json.loads(seedcontent)
        for sub in configlist:
            cfg = spiderCFG()
            tasktext = sub
            cfg.site_id = tasktext['site_id']
            cfg.board_id = tasktext['board_id']
            cfg.entry_url = tasktext['entry_url']
            cfg.board_name = tasktext['board_name']
            cfg.site_name = tasktext['site_name']
            self.cfg_list.append(cfg)
    def start_requests(self):
        for cfg in self.cfg_list:
            cfg.nextpage = 1
            tmp_url = cfg.entry_url % (cfg.nextpage)
            logger.info("board_id=%s,entry_url=%s" % (cfg.board_id, tmp_url))
            request = scrapy.Request(tmp_url,headers=self.headers,callback=self.parse,meta={'proxy':'http://192.168.1.10:1081'})
            request.meta['cfg'] = copy.deepcopy(cfg)
            yield request

    def parse(self, response):
        json_data = json.loads(response.body)
        cfg = response.meta['cfg']
        data_item = json_data["response"] 
        list_item = data_item.get("items")
        for cnlist in list_item:
            item = DetailItem()
            item.Init()
            gt =  int(time.time())*1000
            url_id = cnlist.get("thread_id")
            reply_total_page = cnlist.get("total_page")
            reply_total_page += 1
            item['site_id'] = cfg.site_id
            item['site_name'] = cfg.site_name
            item['board_id'] = cfg.board_id
            item['board_name'] = cfg.board_name
            item['title'] = cnlist.get("title")
            item['title_zh'] = Traditional2Simplified(cnlist.get("title"))
            item['thread_id'] = cnlist.get("thread_id")
            item['publish_time'] = int(cnlist.get("create_time"))
            timeArray = time.localtime(item['publish_time'])
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            item['publish_time_format'] = otherStyleTime
            item['gather_time'] = int(time.time())*1000
            item['u_id'] = cnlist.get("user_id")
            item['u_name'] = cnlist.get("user_nickname")
            item['url'] = "https://lihkg.com/thread/{}".format(url_id)
            item['match_key'] = md5.getMD5(item['url']) 
            item['like_count'] = int(cnlist.get("like_count"))
            item['dislike_count'] = int(cnlist.get("dislike_count"))
            item['reply_like_count'] = int(cnlist.get("reply_like_count"))
            item['reply_dislike_count'] = int(cnlist.get("reply_dislike_count"))
            yield item
            
            for cont_page in range(int(reply_total_page)):
                if cont_page ==0:
                    continue
                reply_url = "https://lihkg.com/api_v2/thread/{}/page/{}?order=reply_time".format(url_id,cont_page)
                request_reply = scrapy.Request(reply_url,headers=self.headers,callback=self.reply_parse,meta={'proxy':'http://192.168.1.10:1081'})
                request_reply.meta['item'] = copy.deepcopy(item)
                yield request_reply
        if cfg.nextpage<50:
            cfg.nextpage+=1
            tmp_url = cfg.entry_url % (cfg.nextpage)
            logger.info("board_id=%s,entry_url=%s" % (cfg.board_id, tmp_url))
            request = scrapy.Request(tmp_url,headers=self.headers,callback=self.parse,meta={'proxy':'http://192.168.1.10:1081'})
            request.meta['cfg'] = deepcopy(cfg)
            yield request
        
    def reply_parse(self, response):    
        json_data = json.loads(response.body)
        cfg = response.meta['item']
        if "response" not in json_data:
             return
        data_item = json_data["response"]
        content_item = data_item.get("item_data")
        for cntdata in content_item:
            reply_item = reply_Item()
            reply_item.Init()
            img_list = []
            user_data = cntdata.get("user")
            reply_url            = response.url
            reply_url            = re.sub('api_v2/', "", reply_url, 0, re.S|re.M|re.I) 
            reply_url            = reply_url.split("?")[0]
            reply_content        = cntdata.get('msg','')
            reply_match_key            = md5.getMD5(reply_url+reply_content)
            content              = cntdata.get("msg")
            reply_content = re.sub(r'<img src=.*?>', "{img}", content, 0, re.S|re.M|re.I)
            reply_content = re.sub('<a.*?>.*?</a>', "", reply_content, 0, re.S|re.M|re.I)
            reply_content = replace_by_img_tag(reply_content)
            img_all = re.findall("<img src=\"(.*?)\" class.*?>",content)
            for img in img_all:
                if len(img)==0:
                    continue
                if "http" not in img:  
                   url_data = "https://lihkg.com/"
                   img = urllib.parse.urljoin(url_data,img) 
                else:
                   img = img
                img_list.append(img)
            reply_item['reply_content']   = reply_content 
            reply_item['reply_content_zh']= Traditional2Simplified(reply_content)
            nlp_json = NLP_server(reply_item['reply_content_zh'])
            if nlp_json.index() == "True":
                return
            nlp_data = json.loads(nlp_json.index())
            reply_item['sent'] = nlp_data['sent']
            reply_item['sent_num'] = nlp_data['sent_num']
            reply_item['images']          = img_list 
            reply_item['match_key']       = cfg.get("match_key")
            reply_item['reply_match_key'] = reply_match_key 
            reply_item['like_count']      = int(cntdata.get("like_count"))
            reply_item['dislike_count']   = int(cntdata.get("dislike_count"))
            reply_item['title']           = cfg.get("title")
            reply_item['title_zh']        = Traditional2Simplified(cfg.get("title"))
            reply_item['user_id']         = user_data.get("user_id")
            reply_item['reply_user']      = cntdata.get("user_nickname")
            reply_item['reply_pt']        = cntdata.get("reply_time")
            timeArray = time.localtime(reply_item['reply_pt'])
            otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
            reply_item['reply_pt_format'] = otherStyleTime
            reply_item['msg_num']         = int(cntdata.get("msg_num"))
            reply_item['reply_url']       = reply_url
            logger.info("reply_url=%s,reply_md5=%s" % (reply_url,reply_match_key))
            yield reply_item

