# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class QuestionsanswersCommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    board_id = scrapy.Field()
    board_name = scrapy.Field()
    media_id = scrapy.Field()
    media_name = scrapy.Field()
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
    comments_count = scrapy.Field()
    def init(self):
        self["likes_count"] = 0
        self["comments_count"] = 0

