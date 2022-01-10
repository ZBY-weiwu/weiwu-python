# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time


class WemediaCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    media_id = scrapy.Field()
    media_name = scrapy.Field()
    url = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    screen_name = scrapy.Field()
    publish_time = scrapy.Field()
    gather_time = scrapy.Field()
    comment_id = scrapy.Field()
    root_id = scrapy.Field()
    content = scrapy.Field()
    comments_count = scrapy.Field()
    likes_count = scrapy.Field()
    parent_id = scrapy.Field()


    def init(self):
        self["likes_count"] = 0
        self["user_name"] = ""
        self["screen_name"] = ""
        self["user_id"] = ""
        self["url"] = ""
        self["comments_count"] = 0
        self["gather_time"] = int(time.time())*1000
        self["publish_time"] = int(time.time())*1000
        self["comment_id"] = ""
        self["root_id"] = ""
        self["content"] = ""
        self["parent_id"] = ""


class ChildCommentItem(scrapy.Item):
    # define the fields for your item here like:
    media_id = scrapy.Field()
    media_name = scrapy.Field()
    url = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    screen_name = scrapy.Field()
    publish_time = scrapy.Field()
    gather_time = scrapy.Field()
    comment_id = scrapy.Field()
    root_id = scrapy.Field()
    content = scrapy.Field()
    parent_id = scrapy.Field()
    likes_count = scrapy.Field()


    def init(self):
        self["url"] = ""
        self["user_name"] = ""
        self["screen_name"] = ""
        self["user_id"] = ""
        self["gather_time"] = int(time.time())*1000
        self["publish_time"] = int(time.time())*1000
        self["comment_id"] = ""
        self["root_id"] = ""
        self["parent_id"] = ""
        self["content"] = ""
        self["likes_count"] = 0



