# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class overseanewsItem(scrapy.Item):
    detail_accurate_extraction = scrapy.Field()
    detail_abstract = scrapy.Field()
    detail_channel = scrapy.Field()
    detail_evidence_degree = scrapy.Field()
    detail_importance_degree = scrapy.Field()
    detail_is_homepage = scrapy.Field()
    detail_board_id = scrapy.Field()
    detail_board_name = scrapy.Field()
    detail_site_id = scrapy.Field()
    detail_site_name = scrapy.Field()
    detail_board_class_tag = scrapy.Field()
    detail_url = scrapy.Field()
    detail_page_url = scrapy.Field()
    detail_title = scrapy.Field()
    detail_gather_time = scrapy.Field()
    detail_id = scrapy.Field()
    detail_md5 = scrapy.Field()
    detail_sentiment = scrapy.Field()
    detail_author = scrapy.Field()
    detail_click_count = scrapy.Field()
    detail_reply_count = scrapy.Field()
    detail_snapshot = scrapy.Field()
    detail_old_doc = scrapy.Field()
    detail_keyword = scrapy.Field()
    detail_content_finger = scrapy.Field()
    detail_mpath = scrapy.Field()
    detail_picture_vector = scrapy.Field()
    detail_publish_time = scrapy.Field()
    detail_insert_time = scrapy.Field()
    detail_content_raw = scrapy.Field()
    detail_content = scrapy.Field()
    detail_raw_content = scrapy.Field()
    detail_img = scrapy.Field()
    detail_language = scrapy.Field()
    detail_video_vector = scrapy.Field()

    def Init(self):
        self['detail_abstract'] = ''
        self['detail_channel'] = 1
        self['detail_evidence_degree'] = 3
        self['detail_importance_degree'] = 3
        self['detail_is_homepage'] = 0
        self['detail_board_id'] = 0
        self['detail_board_name'] = ''
        self['detail_site_id'] = 0
        self['detail_site_name'] = ''
        self['detail_board_class_tag'] = []
        self['detail_url'] = ''
        self['detail_content_raw'] = ''
        self['detail_page_url'] = ''
        self['detail_title'] = ''
        self['detail_gather_time'] = 0
        self['detail_id'] = ''
        self['detail_md5'] = ''
        self["detail_img"]= []
        self['detail_sentiment'] = 0
        self['detail_author'] = ''
        self['detail_click_count'] = 0
        self['detail_reply_count'] = 0
        self['detail_snapshot'] = ''
        self['detail_old_doc'] = 0
        self['detail_keyword'] = ''
        self['detail_content_finger'] = ''
        self['detail_mpath'] = 'news_gather'
        self['detail_picture_vector'] = []
        self['detail_publish_time'] = 0
        self['detail_insert_time'] = 0
        self['detail_content'] = ''
        self['detail_raw_content'] = ''
        self['detail_language'] = ""
        self['detail_accurate_extraction'] = ''
        self['detail_video_vector'] = []

