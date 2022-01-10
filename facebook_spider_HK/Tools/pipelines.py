# -*- coding: utf-8 -*-
import json
import os,sys
import configparser
import elasticsearch  #版本 elasticsearch=7.8.1
import urllib3
import requests

parent_dir = os.path.dirname(os.path.abspath(__file__))
print(parent_dir)
urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
conf = configparser.ConfigParser()
conf.read(parent_dir+"/../config/config.ini",encoding="utf-8")

index = conf.get("es_config","_index")
es_url = conf.get("es_config","es_ip")
file_path=conf.get("StorageSwitch","download_path_file")



def pipelines_es(item,id):
    item = json.loads(item)

    try:
        es = elasticsearch.Elasticsearch([es_url])
        es.index(index=index, id=id, body=item)
    except:
        print("es->error")

def file_out(item):
    f = open(parent_dir+"/../"+file_path,"a+",encoding="utf-8")
    f.write(json.dumps(item,ensure_ascii=False)+"\n")
    f.close()
    
