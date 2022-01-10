# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time
from lihkg_search.models.es_types import ArticleType
from lihkg_search.models.es_reply import Article_reply


class DetailItem(scrapy.Item):
    match_key           = scrapy.Field() #
    key_word            = scrapy.Field() #
    board_id            = scrapy.Field() #
    thread_id           = scrapy.Field() #
    url                 = scrapy.Field() #
    like_count          = scrapy.Field()
    dislike_count       = scrapy.Field()
    publish_time        = scrapy.Field() #
    publish_time_format = scrapy.Field()
    u_id                = scrapy.Field() #
    u_name              = scrapy.Field() #
    reply_like_count    = scrapy.Field() #
    reply_dislike_count = scrapy.Field() #
    title               = scrapy.Field() #
    title_zh            = scrapy.Field() #
    gather_time         = scrapy.Field() #
    reply_user          = scrapy.Field()
    lang                = scrapy.Field()
    reply_url           = scrapy.Field()
    def Init(self):
        self['match_key']        = ""
        self['title']            = ""
        self['key_word']         = ""
        self['title_zh']         = ""
        self['u_id']             = ""
        self['u_name']           = ""
        self['thread_id']        = ''
        self['url']              = ''
        self['reply_url']        = ''
        self['publish_time']     = 0
        self['gather_time']      = 0 
        self['reply_like_count'] = 0
        self['reply_dislike_count'] = 0
        self['publish_time_format'] = ""
        self['lang']             = 'zh'
    
    def save_to_es(self):
        search = ArticleType()
        search.match_key = self['match_key']
        search.thread_id = self['thread_id']
        search.like_count = self['like_count']
        search.key_word = self['key_word']
        search.dislike_count = self['dislike_count']
        search.url = self['url']
        search.publish_time = self['publish_time']
        search.publish_time_format = self['publish_time_format']
        search.u_id = self['u_id']
        search.reply_like_count = self['reply_like_count']
        search.reply_dislike_count = self['reply_dislike_count']
        search.title = self['title']
        search.title_zh = self['title_zh']
        search.gather_time = self['gather_time']
        search.lang = self['lang']
        search.meta.id = self['match_key']
        try:
            search.save()
        except:
            pass
        return

class reply_Item(scrapy.Item):
    match_key        = scrapy.Field()
    key_word         = scrapy.Field()
    reply_match_key  = scrapy.Field()
    like_count       = scrapy.Field() #
    user_id          = scrapy.Field() #
    images           = scrapy.Field() #
    dislike_count    = scrapy.Field() #
    title            = scrapy.Field() #
    title_zh         = scrapy.Field() #
    reply_content    = scrapy.Field()
    reply_content_zh = scrapy.Field()
    reply_user       = scrapy.Field()
    reply_pt         = scrapy.Field()
    reply_pt_format  = scrapy.Field()
    msg_num          = scrapy.Field()
    reply_url        = scrapy.Field()
    
    def Init(self):
        self['match_key']       = ""
        self['key_word']       = ""
        self['reply_match_key'] = ""
        self['title']           = ""
        self['title_zh']        = ""
        self['user_id']         = ""
        self['reply_content']   = ""
        self['reply_content_zh'] = ""
        self['reply_url'] = ""
        self['images'] = []
        self['like_count']      = 0
        self['dislike_count']   = 0
        self['reply_user']      = 0
        self['reply_pt']        = 0
        self['reply_pt_format'] = ""
        self['msg_num']         = 0#评论楼层
    
    def save_to_es(self):
        search = Article_reply()
        search.match_key = self['match_key']
        search.reply_match_key = self['reply_match_key']
        search.like_count = self['like_count']
        search.dislike_count = self['dislike_count']
        search.user_id = self['user_id']
        search.images = self['images']
        search.reply_pt = self['reply_pt']
        search.reply_pt_format = self['reply_pt_format']
        search.user_id = self['user_id']
        search.reply_user = self['reply_user']
        search.reply_url = self['reply_url']
        search.title = self['title']
        search.title_zh = self['title_zh']
        search.reply_content = self['reply_content']
        search.reply_content_zh = self['reply_content_zh']
        search.msg_num = self['msg_num']
        search.meta.id = self['reply_match_key']
        try:
            search.save()
        except:
            pass
        return
