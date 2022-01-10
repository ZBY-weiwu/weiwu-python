# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy



class Questionsanswers_searchItem(scrapy.Item):

    # detail_channel = scrapy.Field()
    board_id = scrapy.Field()
    board_name = scrapy.Field()
    media_id = scrapy.Field()
    media_name = scrapy.Field()
    tags = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    gather_time = scrapy.Field()
    publish_time = scrapy.Field()
    update_time = scrapy.Field()
    md5 = scrapy.Field()
    author = scrapy.Field()
    comments_count = scrapy.Field()
    picture_urls = scrapy.Field()
    # detail_reward_number = scrapy.Field()
    extra_info = scrapy.Field()
    keyword = scrapy.Field()
    views_count = scrapy.Field()
    root_id = scrapy.Field()

    author_img = scrapy.Field()
    author_screen_name = scrapy.Field()
    author_id = scrapy.Field()
    author_name = scrapy.Field()
    favourites_count = scrapy.Field()
    reward_number = scrapy.Field()

    def init(self):
        self['views_count'] = 0
        self['tags'] = []
        self['author_name'] = ""
        self['author_id'] = ""
        self['author_img'] = ""
        self["author_screen_name"] = ""
        self["favourites_count"] = 0
        self["reward_number"] = 0