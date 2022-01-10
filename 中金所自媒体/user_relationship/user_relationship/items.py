# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time


class UserRelationshipItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    media_name = scrapy.Field()
    media_id = scrapy.Field()
    relationship_type = scrapy.Field()
    owner_uid = scrapy.Field()
    owner_name = scrapy.Field()
    owner_screen_name = scrapy.Field()
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    screen_name = scrapy.Field()
    friends_count = scrapy.Field()
    followers_count = scrapy.Field()
    description = scrapy.Field()
    register_time = scrapy.Field()
    statuses_count = scrapy.Field()
    profile_image_url = scrapy.Field()
    register_location = scrapy.Field()
    bi_followers_count = scrapy.Field()


    def init(self):
        self["owner_screen_name"] = ""
        self["user_id"] = ""
        self["user_name"] = ""
        self["screen_name"] = None
        self["friends_count"] = None
        self["followers_count"] = None
        self["description"] = ""
        self["profile_image_url"] = ""
        self["register_location"] = None
        self["bi_followers_count"] = None
        self["register_time"] = int(time.time()*1000)
        self["statuses_count"] = None
