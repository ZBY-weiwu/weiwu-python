# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time
from lihkg.models.es_types import ArticleType
from lihkg.models.es_reply import Article_reply 

class DetailItem(scrapy.Item):
    match_key           = scrapy.Field() #
    board_id            = scrapy.Field() #
    board_name          = scrapy.Field() #
    site_id             = scrapy.Field() #
    site_name           = scrapy.Field() #
    thread_id           = scrapy.Field() #
    url                 = scrapy.Field() #
    like_count          = scrapy.Field()
    dislike_count       = scrapy.Field()
    publish_time        = scrapy.Field() #
    publish_time_format = scrapy.Field() #
    u_id                = scrapy.Field() #
    u_name              = scrapy.Field() #
    reply_like_count    = scrapy.Field() #
    reply_dislike_count = scrapy.Field() #
    title               = scrapy.Field() #
    title_zh            = scrapy.Field() #
    gather_time         = scrapy.Field() #
    lang                = scrapy.Field()
    reply_url           = scrapy.Field()
    def Init(self):
        self['match_key']        = ""
        self['title']            = ""
        self['title_zh']         = ""
        self['u_id']             = ""
        self['u_name']           = ""
        self['board_id']         = 0
        self['board_name']       = ''
        self['site_id']          = 0
        self['site_name']        = 'LIHKG'
        self['thread_id']        = ''
        self['url']              = ''
        self['reply_url']        = ''
        self['publish_time']     = 0
        self['publish_time_format'] = ""
        self['gather_time']      = 0 
        self['reply_like_count'] = 0
        self['reply_dislike_count'] = 0
        self['lang']             = 'zh'



    def save_to_es(self):
        article = ArticleType()
        article.match_key = self['match_key']
        article.board_id = self['board_id']
        article.board_name = self['board_name']
        article.site_id = self['site_id']
        article.site_name = self['site_name']
        article.thread_id = self['thread_id']
        article.like_count = self['like_count']
        article.dislike_count = self['dislike_count']
        article.url = self['url']
        article.publish_time = self['publish_time']
        article.publish_time_format = self['publish_time_format']
        article.u_id = self['u_id']
        article.reply_like_count = self['reply_like_count']
        article.reply_dislike_count = self['reply_dislike_count']
        article.title = self['title']
        article.title_zh = self['title_zh']
        article.gather_time = self['gather_time']
        article.lang = self['lang']
        #article.reply_url = self['reply_url']
        article.meta.id = self['match_key']
        try:
            article.save()
        except:
            pass
        return

class reply_Item(scrapy.Item):
    match_key        = scrapy.Field()
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
    sent             = scrapy.Field()
    sent_num         = scrapy.Field()
    
    def Init(self):
        self['match_key']       = ""
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
        self['reply_pt_format'] = ''
        self['msg_num']         = 0#评论楼层
        self['sent']            = 0
        self['sent_num']        = 0
    def save_to_es(self):
        article = Article_reply()
        article.match_key = self['match_key']
        article.match_key = self['match_key']
        article.reply_match_key = self['reply_match_key']
        article.like_count = self['like_count']
        article.dislike_count = self['dislike_count']
        article.user_id = self['user_id']
        article.images = self['images']
        article.reply_pt = self['reply_pt']
        article.reply_pt_format = self['reply_pt_format']
        article.user_id = self['user_id']
        article.reply_user = self['reply_user']
        article.reply_url = self['reply_url']
        article.title = self['title']
        article.title_zh = self['title_zh']
        article.reply_content = self['reply_content']
        article.reply_content_zh = self['reply_content_zh']
        article.sent = self['sent']
        article.sent_num = self['sent_num']
        article.msg_num = self['msg_num']
        article.meta.id = self['reply_match_key']
        try:
            article.save()
        except:
            pass
        return
