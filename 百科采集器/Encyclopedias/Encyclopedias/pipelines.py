# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from .items import EncyclopediasItem

import time
import json
import requests
from .Tools.by_package import Get_md5
from scrapy.exporters import JsonLinesItemExporter

class JsonFilePipeline:
    def __init__(self):
        self.json_file = open('./output/baike.json', 'wb')
        self.json_exporter = JsonLinesItemExporter(self.json_file, ensure_ascii=False, encoding='UTF-8')
        self.json_exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, EncyclopediasItem):
            self.json_exporter.export_item(item)
            return item

    def close_spider(self, spider):
        self.json_exporter.finish_exporting()
        self.json_file.close()


class KafkaPipeline:

    def __init__(self, host, topic, fm='avro'):
        self.host = host
        self.topic = topic
        self.fm = fm

    def insertKafka(self, data):

        url = self.host + "/topics/" + self.topic
        print("Topic_url:",url)
        headers = {"Content-Type":"application/vnd.kafka."+self.fm+".v2+json", "Accept":"application/vnd.kafka.v2+json"}
        #print "header=",headers
        r = requests.post(url, headers=headers, data=data)
        print ("data:",data)
        print("kafkaresponse:",r.text)


    @classmethod
    def from_crawler(cls, crawler):
        DUPClient_CHANNEL = crawler.settings.get('DUPClient_CHANNEL')
        return cls(
            host = crawler.settings.get('KAFKA_HOST'),
            topic = crawler.settings.get('KAFKA_TOPIC'),
            fm = crawler.settings.get('KAFKA_FORMAT')
        )

    def process_item(self, item, spider):
        if isinstance(item, EncyclopediasItem):
            d = {}
            d["url"] = item["url"]
            d['_key'] = Get_md5(d['url'])
            d["desc"] = item["desc"]
            d['_id'] = "34" + d['_key']
            d['_ch'] = 34
            d['keyword'] = item["keyword"]
            d['_adp'] = "中科天机"
            d["i_sn"] = item["media_name"]
            d["title"] = item["title"]
            d["content"] = item["content"]
            d["content"] = ""
            d["tags"] = []
            d["gt"] = int(time.time())*1000
            d["ut"] = d["gt"]
            d["it"] = d["gt"]
            key_schema = '{"name":"_key" ,"type": "string"}'
            value_schema = '{"type":"record","name":"evchk_doc","fields": [{"name":"_id","type":"string"},{"name":"_ch","type":"long"},{"name":"desc","type":"string"},{"name":"title","type":"string"},{"name":"_key","type":"string"},{"name":"keyword","type":"string"},{"name":"content","type":"string"},{"name":"url","type":"string"},{ "name":"tags","type":{"type":"array","items":"string"}},{"name":"it","type":{"type":"long","logicalType":"timestamp-millis"}},{"name":"ut","type":{"type":"long","logicalType":"timestamp-millis"}},{"name":"gt","type":{"type":"long","logicalType":"timestamp-millis"}},{"name":"i_sn","type":"string"}]}'
            data = {'key': d['_key'], 'value': d}
            records = []
            records.append(data)
            root = {'key_schema': key_schema, 'value_schema': value_schema, 'records': records}
            # print json.dumps(root)
            self.insertKafka(json.dumps(root))
        return item