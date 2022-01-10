#!/usr/bin/python
# -*- coding: UTF-8 -*-
import langid
import sys
import json
import requests
import logging
import re


def getnamedEntityRecognitions(detail):
    jsonArray=detail["namedEntityRecognitions"]
    person={}
    location={}
    organization={}
    map={}
    map["vpers"] = []
    map["vrgn"]=[]
    map["vorg"]=[]
    if jsonArray==None:
        return map
    for i in jsonArray:
        entityType=i["entityType"]
        if entityType=="person":
            personS=i["entity"]
            person=getmap(person,personS)
        elif entityType=="location":
            locationS=i["entity"]
            location=getmap(location,locationS)
        else:
            organizationS=i["entity"]
            organization=getmap(organization,organizationS);
    map["vpers"] = getjson(person)
    map["vrgn"]=getjson(location)
    map["vorg"]=getjson(organization)
    return map
    
#统计固定格式的map，key出现的次数
def getmap(map,key):
    if key in map:
        map[key]=map[key]+1
    else:
        map[key]=1
    return map
    
#map转换成固定格式的json
def getjson(map):
    list=[]
    for key in map:
        avro={}
        value=map[key]
        avro["v"]=key
        avro["w"]=value
        list.append(avro)
    return list
#获取关键字，只要前五行
def getkeywords(detail):
    list=[]
    keywords=detail["keywords"]
    if keywords == None:
        return list
    if len(keywords)>=5:
        i=0
        for keyword in keywords:
            if i==5:
                return list
            list.append(keyword["keyword"])
            i=i+1
    else:
        wordmap={}
        wordmap=countword2(detail)
        i=0
        for key in wordmap:        
            if i==5:
                return list
            list.append(key[0]);
            i=i+1
    return list
    
#获取分词前100个
def getwordSegmentations(detail):
    wordmap=countword(detail)
    list=[]
    num=0
    for key in wordmap:
        avro={}
        avro["v"]=key[0]
        avro["w"]=key[1]
        list.append(avro)
        num=num+1
        if num    >= 100:
            break
    return list
    
#统计分词频次
def countword(detail):
    wordmap={}
    wordSegmentations=detail["wordSegmentations"]
    for jo in wordSegmentations:
        word=jo["word"]
        if len(word)>1:
            if word in wordmap==True:
                sum1=wordmap[word]+1
                wordmap[word]=sum1
            else:
                wordmap[word]=1
    return sorted(wordmap.items(),key=lambda    item:item[1],reverse=True)
    
    #当关键词数量小于5，统计分词
def countword2(detail):
    wordmap={}
    wordSegmentations=detail["wordSegmentations"]
    for jo in wordSegmentations:
        word=jo["word"]
        wordType=jo["wordType"]
        if wordType in ["n","nr","ns","nz","nrt","a"]:
            if len(word)>1:
                if word in wordmap==True:
                    sum1=wordmap[word]+1
                    wordmap[word]=sum1
                else:
                    wordmap[word]=1
    return sorted(wordmap.items(),key=lambda    item:item[1],reverse=True)
    

def remove_emoji(cont):
    emoji_pattern=re.compile(
                u"(\ud83d[\ude00-\ude4f])|"    
                u"(\ud83c[\udf00-\uffff])|"
                u"(\ud83d[\u0000-\uddff])|"
                u"(\ud83d[\ude80-\udeff])|"
                u"(\ud83c[\udde0-\uddff])"    
                "+",    flags=re.UNICODE)
    return emoji_pattern.sub(r'',    cont)
def remove_emoji2(cont):
    try:
        highpoints=re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints=re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return highpoints.sub(u'',cont)
def nlp_deal(cont):
    jarray=[]
    jarray.append(cont)
    #url="http://192.168.99.16:8085/golaxy/nlp/synthesisBasic/chinese/v1"
    #url="http://10.0.121.13:8085/golaxy/nlp/synthesisBasic/chinese/v1"
    if 'zh' in langid.classify(cont):
        #url = 'http://nlp-api.golaxy.local:80/golaxy/nlp/synthesisBasic/chinese/v1'
        url = 'http://192.168.1.20:40011/golaxy/nlp/synthesisBasic/chinese/v1'
    else:
        #url = 'http://nlp-api.golaxy.local:80/golaxy/nlp/synthesisBasic/english/v1'
        url = 'http://192.168.1.20:40011/golaxy/nlp/synthesisBasic/english/v1'
    headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    #try:
    req = requests.post(url, data=json.dumps(jarray), headers=headers,stream=True,timeout=10)
    result=json.loads(req.text)
    #except:
    #    print "nlp_api>>>>>error"
    #    return 'True'
    record={}
    if result['message']=="success" and result['code']==0:
        jsonArray=result["synthesisBasicResults"]
        for detail in jsonArray:
            if not detail:
                rs={'error':'ok','ignore':False,'value':record}
                continue
            if True:
                abstr=detail["summary"]
                record["abstr"]=abstr
        
                sent=(detail["sentiment"]+1)/2*100;
                if sent>=45 and sent<=55:
                    sent=50;
                record["sent"]=sent
                #record["sent"]=long(sent)
    
                record["vkey"]=getwordSegmentations(detail)
        
                record["lkey"]=getkeywords(detail)
            
                namedEntityRecognitions=getnamedEntityRecognitions(detail)
                record["vpers"]=namedEntityRecognitions["vpers"]
                record["vorg"]=namedEntityRecognitions["vorg"]
                record["vrgn"]=namedEntityRecognitions["vrgn"]
            rs={'error':'ok','ignore':False,'value':record}
    else:
        plpy.log('****err****',json.dumps(rs,ensure_ascii=False));
        rs={'error':'自然语言处理返回状态：'+json.dumps(result,ensure_ascii=False),'ignore':True,'value':{}}
    
    return json.dumps(rs,ensure_ascii=False)

if __name__=="__main__":

    a='''（记者马曹冉、杜潇逸）22日晚，2019赛季亚冠联赛小组赛E组展开最后一轮的争夺，山东鲁能泰山队客场1:2负于鹿岛鹿角队。上半场山东鲁能的费莱尼率先破门，下半场替补出场的鹿岛鹿角队伊藤翔在两分钟内连入两球实现逆转。
      上一轮之后，山东鲁能泰山队已经锁定小组第一，提前出线。本轮战后，鹿岛鹿角队列小组第二，与鲁能携手晋级十六强。
      开场后，山东鲁能反客为主，通过连续进攻不断威胁对方禁区。第11分钟，山东鲁能队获得角球，费莱尼抓住机会头球破门，鲁能1:0领先。这也是费莱尼本赛季的第三个亚冠进球。失球之后，鹿岛鹿角开始大举反击。山东鲁能门将韩镕泽表现神勇，多次化解险情。
      下半场，鹿岛鹿角进一步加大进攻力度，在山东鲁能门前频频制造杀机。第63分钟，鹿岛鹿角用伊藤翔换下中村充孝，此举取得奇效，5分钟后，伊藤翔禁区混乱中抢点破门。仅仅2分钟后，伊藤翔接塞尔吉尼奥传球单刀推射得分，再度建功。这是他本赛季的第四个亚冠进球。鹿岛鹿角2:1完成逆转。'''
    #record=json.loads(a)
    print (nlp_deal(a))
