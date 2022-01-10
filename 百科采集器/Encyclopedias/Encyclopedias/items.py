# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class EncyclopediasItem(scrapy.Item):
    media_name = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    keyword = scrapy.Field()
    desc = scrapy.Field()

    def init(self):
        self['media_name'] = ""
        self['url'] = ""
        self['title'] = ""
        self['content'] = ""
        self['keyword'] = ""
        self['desc'] = ""