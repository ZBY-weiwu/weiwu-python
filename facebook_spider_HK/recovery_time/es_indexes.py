from elasticsearch import Elasticsearch
import re
import urllib3
import requests
import json
from facebook_package import Get_pubtime
from facebook_package import format_pubtime


def updata_es(channel,_id,field,value):
    url = "http://192.168.1.20:8090/api/v2/web/browse/updateByChannelAndId?channel={}&id={}&field={}&value={}".format(channel,_id,field,value)
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","Accept": "application/json"}
    response = requests.get(url,headers)
    resp = json.loads(response.text)
    data = resp['data']
    return data


def es_lihkg_indexes():
     
    query_json ={ 
    "query": { 
    "bool" : { 
     "must_not" : { 
     "match" : { 
      "post_id" : -1
     } 
     } 
    } 
    }
} 
    return query_json

def es_indexes(query_json):
    es_url = "192.168.1.20:9200"
    es_index = "hk_facebook"
    es = Elasticsearch([es_url],sniff_on_start=True,sniff_on_connection_fail=True,sniffer_timeout=60,ignore=[400, 405, 502])  # 以列表的形式忽略多个状态码
    #es = Elasticsearch([es_url],ignore=[400, 405, 502])  # 以列表的形式忽略多个状态码

    page_num = 100  # 每次获取数据
    query = es.search(index=es_index, body=query_json, scroll='5m', size=page_num)

    results = query['hits']['hits']  # es查询出的结果第一页
    total = query['hits']['total']['value']  # es查询出的结果总量
    scroll_id = query['_scroll_id']  # 游标用于输出es查询出的所有结果
    every_num = int(total/page_num)  #
    alist = []
    a = 0
    for i in range(0, every_num+1):
        # scroll参数必须指定否则会报错
        query_scroll = es.scroll(scroll_id=scroll_id, scroll='5m')['hits']['hits']
        results += query_scroll
    for key in results:
        if isinstance(key,dict):
            a+=1
            _id = key['_id']
            _source = key["_source"]
            post_id = _source["post_id"]
            if post_id ==-1:
                continue
            pub_time = _source["pub_time"]
            gt = int(str(_source["gt"])[:-3])
            url = _source["url"]
            if pub_time==gt:
                print("post_id:[%s],pub_time:[%s],gt:[%s]"%(post_id,pub_time,gt))
            else:
                continue
            try:    
                now_pub_time = Get_pubtime(url)
            except:
                continue
            now_format_time = format_pubtime(now_pub_time)
            #print("now_pub_time:%d,now_format_time:%s"%(now_pub_time,now_format_time))
            updata_es(es_index,_id,"pub_time",now_pub_time)        
            updata_es(es_index,_id,"format_pubtime",now_format_time)
    print("___________________________________________")
    #print (key)
    return key
    

if __name__=="__main__":
    es_indexes(es_lihkg_indexes())
    
