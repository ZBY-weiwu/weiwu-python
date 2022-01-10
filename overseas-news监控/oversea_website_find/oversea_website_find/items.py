# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OverseaWebsiteFindItem(scrapy.Item):
    # define the fields for your item here like:
    site_name = scrapy.Field()
    site_url = scrapy.Field()
    country = scrapy.Field()

    def init(self):
        self['site_name'] = ""
        self['site_url'] = ""
        self['country'] = ""

