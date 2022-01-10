# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .core.golaxy.spider import items as goalxy_item
from .core.golaxy.spider import persistor
from .items import QuestionsanswersCommentItem



"""
    user_url = scrapy.Field()
    detail_id = scrapy.Field()
    publish_time = scrapy.Field()
    gather_time = scrapy.Field()
    user_img = scrapy.Field()
    user_name = scrapy.Field()
    user_id = scrapy.Field()
    comment_id = scrapy.Field()
    comment = scrapy.Field()
    likes_count = scrapy.Field()
    comments_count = scrapy.Field()"""

class QuestionsanswersCommentPipeline:
    def process_item(self, item, spider):

        if isinstance(item, QuestionsanswersCommentItem):
            print(item)
            d=goalxy_item.GolaxyWenDaDataItem()
            d['_key'] = item["comment_id"]
            d['_spec'] = "M-QA01-AI"
            d['_id'] = "41"+item["comment_id"]
            d['_ch'] = 41
            d['_dcm'] = "监控采集"
            d['_adp'] = "中科天机"
            d["board_id"] = "-1"
            d["message_type"] = 2
            d["board_name"] = item["board_name"]
            d["media_id"] = str(item["media_id"])
            d["media_name"] = item["media_name"]

            d["content"] = item["comment"]
            d["author_screen_name"] = item["user_name"]
            d["author_id"] = str(item["user_id"])
            d["title"] = ""
            d["url"] = ""
            d["comments_count"] = int(item["comments_count"])
            d["gather_time"] = item['gather_time']
            if len(str(item['publish_time']))==10:
                d['publish_time'] = item['publish_time']*1000
            elif len(str(item['publish_time']))==13:
                d['publish_time'] = item['publish_time']
            d["update_time"] = d['publish_time']
            d["insert_time"] = item['gather_time']
            d["likes_count"] = int(item['likes_count'])


            persistor.GolaxyRequestsKafkaDataPersistor.persist(d.item,d.item_type)