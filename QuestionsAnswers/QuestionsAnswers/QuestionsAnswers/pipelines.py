# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import requests
from .items import QuestionsanswersItem
from .core.golaxy.spider import items as goalxy_item
from .core.golaxy.spider import persistor

# class QuestionsanswersPipeline:
#     def process_item(self, item, spider):
#         return item
#


"""
    root_id= scrapy.Field()
    favourites_count = scrapy.Field()
    reward_number = scrapy.Field()
        extra_info = scrapy.Field()
"""
class QuestionsanswersPipeline(object):

    def process_item(self, item, spider):

        if isinstance(item, QuestionsanswersItem):
            # print(item)
            d = goalxy_item.GolaxyWenDaDataItem()
            d['_key'] = item["root_id"]
            d['_spec'] = "M-QA01-AI"
            d['_id'] = "41"+d['_key']
            d['_ch'] = 41
            d['_dcm'] = "监控采集"
            d['_adp'] = "中科天机"
            d["message_type"] = 1
            d["board_id"] = str(item["board_id"])
            d["board_name"] = item["board_name"]
            d["media_id"] = str(item["media_id"])
            d["media_name"] = item["media_name"]
            d["tags"] = item["tags"]

            d["url"] = item["url"]
            d["title"] = item["title"]
            d["content"] = item["content"]
            d["author_screen_name"] = item["author_screen_name"]
            d["author_id"] = str(item["author_id"])
            d["author_name"] = item["author_name"]
            try:
                d["comments_count"] = int(item["comments_count"])
            except:
                d["comments_count"] = 0
            d["picture_urls"] = item["picture_urls"]
            d["views_count"] = item["views_count"]

            d["gather_time"] = item['gather_time']
            d['publish_time'] = item['publish_time']
            d["update_time"] = item['publish_time']
            d["insert_time"] = item['gather_time']
            d["favourites_count"] = item['favourites_count']
            d["extra_info"] = item["extra_info"]

            persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item,d.item_type)
