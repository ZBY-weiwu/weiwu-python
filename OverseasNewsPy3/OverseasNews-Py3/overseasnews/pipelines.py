# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from overseasnews.items import overseanewsItem
from overseasnews.core.golaxy.spider import items as goalxy_item
from overseasnews.core.golaxy.spider.items import new2old
from overseasnews.core.golaxy.spider import persistor
import requests,json,time

KAFKA_RELATIONSHIP_VALUE_SCHEMA='{"type":"record", "name":"avro", "fields":[{"name":"_ch","type":"int"},{"name":"id","type":"string"},{"name":"owner_uid","type":"string"},{"name":"owner_name","type":"string"},{"name":"owner_screen_name","type":["string","null"]},{"name":"uid","type":"string"},{"name":"name","type":"string"},{"name":"screen_name","type":["string","null"]},{"name":"media_id","type":["string","null"]},{"name":"media_name","type":"string"},{"name":"profile_image_url","type":["string","null"]},{"name":"description","type":["string","null"]},{"name":"register_time","type":["long","null"]},{"name":"register_location","type":["string","null"]},{"name":"bi_followers_count","type":["int","null"]},{"name":"followers_count","type":["int","null"]},{"name":"friends_count","type":["int","null"]},{"name":"statuses_count","type":["int","null"]},{"name":"relationship_type","type":"string"},{"name":"update_time","type":"long"},{"name":"gather_time","type":"long"},{"name":"insert_time","type":"long"}], "description":"avroschema"}'
KAFKA_KEY_SCHEMA = '{"name":"_id" ,"type": "string"}'
KAFKA_HEADERS = {"Content-Type": "application/vnd.kafka.avro.v2+json","Accept": "application/vnd.kafka.v2+json"}
KAFKA_RELATIONSHIP_URL = 'http://10.20.18.6:8082/topics/relationship_tmp1'



class OverseasnewsKafka:
    def process_item(self, item, spider):

        if isinstance(item, overseanewsItem):
            d=goalxy_item.GolaxyOverseaNewsDataItem()
            d['id'] = "04" + str(item["detail_md5"])
            d['_ch'] = 4
            d['_key'] = item["detail_md5"]
            d['_spec'] = "M-JW01-AI"
            d['_dcm'] = "监控采集"
            d['_adp'] = "中科天机"
            d["lang"] = item["detail_language"]
            d['title'] = item["detail_title"]
            d['content'] = item["detail_content"]
            d['abstract'] = item["detail_abstract"]
            d["content_raw"] = item["detail_content_raw"]
            d["publish_time"] = item["detail_publish_time"]
            d["picture_urls"] = item["detail_picture_vector"]
            d["media_id"] = str(item["detail_site_id"])
            d["media_name"] = item["detail_site_name"]
            d["board_id"] = str(item["detail_board_id"])
            d["board_name"] = str(item["detail_site_name"])
            d["media_location"] = ["其他"]
            d["url"] = item["detail_url"]
            d["author_name"] = item["detail_author"]
            if d.item_type=="oversea_news":
                old_item = new2old(d)
                persistor.GolaxyRequestsKafkaDataPersistor.persist(old_item.item,old_item.item_type)