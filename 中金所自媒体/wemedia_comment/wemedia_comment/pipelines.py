# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .core.golaxy.spider import items as goalxy_item
from .core.golaxy.spider import persistor
import requests,json
from .items import WemediaCommentItem,ChildCommentItem

class wemediaCommentPipeline:
    def process_item(self, item, spider):
        if isinstance(item, WemediaCommentItem):
            d=goalxy_item.GolaxyWeMediaCommentItem()
            d['_key'] = str(item["comment_id"])
            d['_spec'] = "M-APP02-A"
            d['_id'] = "11" + str(item["comment_id"])
            d['_ch'] = 11
            d['_dcm'] = "监控采集"
            d['_adp'] = "中科天机"
            d["message_type"] = 2
            d["media_id"] = str(item["media_id"])
            d["media_name"] = item["media_name"]
            d["content"] = item["content"]
            # 一级评论的评论数
            d["comments_count"] = item["comments_count"]
            d["author_id"] = str(item["user_id"])
            d["author_name"] = str(item["user_name"])
            d["author_screen_name"] = str(item["screen_name"])
            d["url"] = item["url"]
            d["root_id"] = str(item["root_id"])
            d["parent_id"] = str(item["parent_id"])
            d["gather_time"] = item['gather_time']
            if len(str(item['publish_time'])) == 10:
                d['publish_time'] = item['publish_time'] * 1000
            elif len(str(item['publish_time'])) == 13:
                d['publish_time'] = item['publish_time']
            elif len(str(item['publish_time'])) == 16:
                d['publish_time'] = item['publish_time']/1000

            d["update_time"] = item['gather_time']
            d["insert_time"] = item['gather_time']
            d["likes_count"] = int(item['likes_count'])
            # print("d_type:",d.item_type)
            # print("d_time:",json.dumps(d.item,ensure_ascii=False))
            persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item,d.item_type)


        elif isinstance(item, ChildCommentItem):

            d=goalxy_item.GolaxyWenDaDataItem()
            d['_key'] = str(item["comment_id"])
            d['_spec'] = "M-APP02-A"
            d['_id'] = "11" + str(item["comment_id"])
            d['_ch'] = 11
            d['_dcm'] = "监控采集"
            d['_adp'] = "中科天机"
            d["message_type"] = 2
            d["media_id"] = str(item["media_id"])
            d["media_name"] = item["media_name"]
            d["content"] = item["content"]
            d["author_id"] = item["user_id"]
            d["author_name"] = str(item["user_name"])
            d["author_screen_name"] = str(item["screen_name"])
            d["url"] = item["url"]
            d["root_id"] = str(item["root_id"])
            d["parent_id"] = str(item["parent_id"])
            d["gather_time"] = item['gather_time']
            if len(str(item['publish_time'])) == 10:
                d['publish_time'] = item['publish_time'] * 1000
            elif len(str(item['publish_time'])) == 13:
                d['publish_time'] = item['publish_time']
            elif len(str(item['publish_time'])) == 16:
                d['publish_time'] = item['publish_time']/1000
            d["update_time"] = item['gather_time']
            d["insert_time"] = item['gather_time']
            d["likes_count"] = int(item['likes_count'])
            # print("d_type:",d.item_type)
            # print("d_time:",json.dumps(d.item,ensure_ascii=False))
            persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item,d.item_type)

