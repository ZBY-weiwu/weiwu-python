# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import UserRelationshipItem
from .core.golaxy.spider import items as goalxy_item
from .core.golaxy.spider import persistor
import requests,json,time

KAFKA_RELATIONSHIP_VALUE_SCHEMA='{"type":"record", "name":"avro", "fields":[{"name":"_ch","type":"int"},{"name":"id","type":"string"},{"name":"owner_uid","type":"string"},{"name":"owner_name","type":"string"},{"name":"owner_screen_name","type":["string","null"]},{"name":"uid","type":"string"},{"name":"name","type":"string"},{"name":"screen_name","type":["string","null"]},{"name":"media_id","type":["string","null"]},{"name":"media_name","type":"string"},{"name":"profile_image_url","type":["string","null"]},{"name":"description","type":["string","null"]},{"name":"register_time","type":["long","null"]},{"name":"register_location","type":["string","null"]},{"name":"bi_followers_count","type":["int","null"]},{"name":"followers_count","type":["int","null"]},{"name":"friends_count","type":["int","null"]},{"name":"statuses_count","type":["int","null"]},{"name":"relationship_type","type":"string"},{"name":"update_time","type":"long"},{"name":"gather_time","type":"long"},{"name":"insert_time","type":"long"}], "description":"avroschema"}'
KAFKA_KEY_SCHEMA = '{"name":"_id" ,"type": "string"}'
KAFKA_HEADERS = {"Content-Type": "application/vnd.kafka.avro.v2+json","Accept": "application/vnd.kafka.v2+json"}
KAFKA_RELATIONSHIP_URL = 'http://10.20.18.6:8082/topics/relationship_tmp1'



class UserRelationship:
    def process_item(self, item, spider):

        if isinstance(item, UserRelationshipItem):
            d=goalxy_item.GolaxyUserRelationShip()
            d['id'] = "11" + str(item["id"])
            d['_ch'] = 11
            d['owner_uid'] = item["owner_uid"]
            d['owner_name'] = item["owner_name"]
            d['owner_screen_name'] = item["owner_screen_name"]
            d['uid'] = item["user_id"]
            d['name'] = item["user_name"]
            d['screen_name'] = item["screen_name"]
            d['media_id'] = str(item["media_id"])
            d['media_name'] = item["media_name"]
            d['profile_image_url'] = item["profile_image_url"]
            d['description'] = item["description"]
            d['register_time'] = item["register_time"]
            d['register_location'] = item["register_location"]
            d['bi_followers_count'] = item["bi_followers_count"]
            d['followers_count'] = item["followers_count"]
            d['friends_count'] = item["friends_count"]
            d['statuses_count'] = item["statuses_count"]
            d['relationship_type'] = item["relationship_type"]
            d['gather_time'] = int(time.time())*1000
            d['update_time'] = d['gather_time']
            d['insert_time'] = d['gather_time']

            # print("d_type:",d.item_type)
            # print("d_time:",json.dumps(d.item,ensure_ascii=False))
            persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item,d.item_type)