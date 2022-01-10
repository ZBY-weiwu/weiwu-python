#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/4/7
import copy
import json
import time

from core.origin.common import base
from core.origin.common import mix
from core.origin.common import security

#
# class GolaxyDataItem(object):
#     ITEM_TYPE = 'golaxy_data_item'
#
#     def __init__(self, **kwargs):
#         self._id = None
#         self._key = None
#         self._ch = None
#         self._spec = None
#         self.lang = 'zh'
#         self.url = None
#
#         self.now = time.time()  # 非提交数据
#         self.__dict__.update(**kwargs)
#
#     def _clean_key(self):
#         if not self.url:
#             self._clean_url()
#         self._key = security.EncryptUtils.md5(self.url)
#
#     def _clean_id(self):
#         if not self._key:
#             self._clean_key()
#         if not self._ch:
#             self._clean_ch()
#         ch = self._ch
#         if ch < 10:
#             ch = '0%s' % ch
#         self._id = '%s%s' % (ch, self._key)
#
#     def _clean_ch(self):
#         if not self._ch:
#             raise Exception('The _ch of item is not None')
#
#     def _clean_url(self):
#         if not self.url:
#             raise Exception('The url of item is not None')
#
#     def _clean_spec(self):
#         if not self._spec:
#             raise Exception('The _spec of item is not None')
#
#     @property
#     def item(self):
#         return self.__dict__
#
#     @property
#     def item_type(self):
#         return self.ITEM_TYPE
#
#     def confirm(self):
#         getattr(self, 'start_clean')()
#         for field in list(self.__dict__.keys()):
#             if not field.startswith('_'):
#                 field = '_%s' % field
#             clean_field_method = '_clean%s' % field
#             if hasattr(self, clean_field_method):
#                 getattr(self, clean_field_method)()
#         getattr(self, 'end_clean')()
#
#     def start_clean(self):
#         pass
#
#     def end_clean(self):
#         del self.now
#
#     def __setitem__(self, key, value):
#         if value is not None:
#             self.__dict__[key] = value
#
#     def __getitem__(self, item):
#         return self.__dict__[item]
#
#     def __str__(self):
#         return self.__repr__()
#
#     def __repr__(self):
#         return json.dumps(self.item, ensure_ascii=False)
#
#
# class GolaxyNewsDataItem(GolaxyDataItem):
#     pass
#
#
# class GolaxyAppNewsDataItem(GolaxyNewsDataItem):
#     ITEM_TYPE = 'golaxy_app_news_data_item'
#
#     def __init__(self, **kwargs):
#         self.pt = None  # 发布时间，13位int
#         self.title = ''  # 标题,int
#         self.cont = ''  # 去标签正文,str
#         self.author = ''  # 作者,str
#         self.i_bid = None  # 板块id，int
#         self.i_bn = None  # 板块名称,str
#         self.i_sid = None  # 网站id,int
#         self.i_sn = None  # 网站名称,str
#         self.loc = '中国,北京'  # 地区,str
#         self._ex = 0
#         self.gt = None
#         self.it = None
#         self.ut = None
#         self.abstr = ''
#         self.lpic = list()
#         self.lvideo = list()
#         self.lkey = list()
#         self.vkey = list()
#         self.vpers = list()
#         self.vorg = list()
#         self.vrgn = list()
#         self.sent = 0
#         self.adp = '中科天玑'
#         self.nrd = 0
#         self.nrply = 0
#         self.purl = None
#         super(GolaxyAppNewsDataItem, self).__init__(**kwargs)
#
#     def _clean_purl(self):
#         if not self.purl:
#             self.purl = self.url
#
#     def _clean_ut(self):
#         if not self.ut:
#             self.ut = self.gt
#
#     def _clean_it(self):
#         if not self.it:
#             self.it = self.gt
#
#     def _clean_gt(self):
#         if not self.gt:
#             self.gt = mix.DateTimeUtils.unify_time_stamp(self.now)
#
#     def _clean_i_sn(self):
#         if not self.i_sn:
#             raise Exception('The i_sn of item is not None')
#
#     def _clean_i_sid(self):
#         if not self.i_sid:
#             raise Exception('The i_sid of item is not None')
#
#     def _clean_i_bn(self):
#         if not self.i_bn:
#             raise Exception('The i_bn of item is not None')
#
#     def _clean_pt(self):
#         if not self.pt:
#             self.pt = self.now
#         self.pt = mix.DateTimeUtils.unify_time_stamp(self.pt)
#
#     def _clean_title(self):
#         if not self.title:
#             raise Exception('The title of item is not None')
#         if len(self.title) > 25:
#             self.title = self.title[:25]
#
#     def _clean_cont(self):
#         if not self.cont:
#             raise Exception('The cont of item is not None')
#
#     def _clean_lang(self):
#         if not self.lang:
#             raise Exception('The lang of item is not None')
#
#     def _clean_i_bid(self):
#         if not self.i_bid:
#             raise Exception('The i_bid of item is not None')
#
#
# class GolaxyWebNewsDataItem(GolaxyAppNewsDataItem):
#     ITEM_TYPE = 'golaxy_web_news_data_item'
#
#     def __init__(self, **kwargs):
#         self.raw_cont = ''
#         self.source = ''
#         super(GolaxyWebNewsDataItem, self).__init__(**kwargs)
#
#     def _clean_source(self):
#         if not self.source:
#             self.source = self.author
#
#
# class GolaxyWemediaNewsDataItem(GolaxyWebNewsDataItem):
#     ITEM_TYPE = 'golaxy_wemedia_news_data_item'
#
#     def _clean_author(self):
#         if not self.author:
#             raise Exception('The i_author of item is not None')
#
#
# class GolaxyWemediaAppNewsDataItem(GolaxyAppNewsDataItem):
#     ITEM_TYPE = 'golaxy_wemedia_app_news_data_item'
#
#     def _clean_author(self):
#         if not self.author:
#             raise Exception('The i_author of item is not None')
#
#
# class GolaxyRecruitWebDataItem(GolaxyDataItem):
#     ITEM_TYPE = 'golaxy_recruit_web_data_item'
#
#     def __init__(self, **kwargs):
#         self._dcm = None
#         self._adp = '中科天玑'
#         self.tags = []
#         self.gather_time = None
#         self.update_time = None
#         self.insert_time = None
#         self.publish_time = None
#         self.site_id = None
#         self.site_name = None
#         self.job_name = ''
#         self.job_salary = ''
#         self.job_education = ''
#         self.job_number = ''
#         self.job_date_range = ''
#         self.job_description = ''
#         self.job_description_raw = ''
#         self.job_department = ''
#         self.job_address = ''
#         self.job_experience = ''
#         self.job_recruiter = ''
#         self.job_recruiter_position = ''
#         self.job_advantage = ''
#         self.company_name = ''
#         self.company_home_url = ''
#         self.company_logo = ''
#         self.company_industry = ''
#         self.company_development_stage = ''
#         self.company_scale = ''
#         self.company_description = ''
#         self.company_business_info = {
#             'company_name': '',
#             'legal_representative': '',
#             'registered_capital': '',
#             'foundation_date': '',
#             'business_type': '',
#             'business_status': '',
#             'registered_address': '',
#             'uniform_code': '',
#             'business_scope': '',
#             'extra_info': '',
#         }
#         self.extra_info = ''
#         super(GolaxyRecruitWebDataItem, self).__init__(**kwargs)
#
#     def _clean_company_name(self):
#         if not self.company_name:
#             raise Exception('The company_name of item is not None')
#
#     def _clean_site_name(self):
#         if not self.site_name:
#             raise Exception('The site_name of item is not None')
#
#     def _clean_site_id(self):
#         if not self.site_id:
#             raise Exception('The site_id of item is not None')
#
#     def _clean_update_time(self):
#         if not self.update_time:
#             self.update_time = self.gather_time
#
#     def _clean_insert_time(self):
#         if not self.insert_time:
#             self.insert_time = self.gather_time
#
#     def _clean_gather_time(self):
#         if not self.gather_time:
#             self.gather_time = mix.DateTimeUtils.unify_time_stamp(self.now)
#
#     def _clean_publish_time(self):
#         if not self.publish_time:
#             self.publish_time = self.gather_time
#         self.publish_time = mix.DateTimeUtils.unify_time_stamp(self.publish_time)
#

# class GolaxyZhiKuDataItem(GolaxyNewDataItem):
#     ITEM_TYPE = 'golaxy_zhiku_data_item'

GolaxyWemediaNewsDataItem = None
GolaxyWemediaAppNewsDataItem = None
GolaxyRecruitWebDataItem = None
GolaxyWebNewsDataItem = None


# 新标准
class DataTypeException(Exception):
    pass


class DataCheckException(Exception):
    pass


class TypeFiled(object):
    """
    字段规范
    """
    TYPE = ''

    def __init__(self, value=None, null=True, name=''):
        self._value = value
        self.null = null
        self.name = name

    @property
    def value(self):
        if self.null:
            if self._value is None:
                return None
            return {
                self.TYPE: self._value
            }
        if self._value is None:
            raise DataCheckException('The Filed %s must have value!' % self.name)
        return self._value

    @property
    def base_value(self):
        return self._value

    def type_check(self, key, value):
        raise NotImplemented

    def __setitem__(self, key, value):
        self.__dict__[key] = self.type_check(key, value)

    def __getitem__(self, item):
        return self.__dict__[item]


class IntTypeFiled(TypeFiled):
    TYPE = 'int'

    def type_check(self, key, value):
        if isinstance(value, int):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be int!' % self.name)


class LongTypeFiled(IntTypeFiled):
    TYPE = 'long'


class StringTypeFiled(TypeFiled):
    TYPE = 'string'

    def type_check(self, key, value):
        if isinstance(value, str):
            if self.null and not value:
                return None
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be str!' % self.name)


class ArrayTypeFiled(TypeFiled):
    TYPE = 'array'

    def type_check(self, key, value):
        if isinstance(value, list):
            if not value:
                return None
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be list!' % self.name)


class ObjectArrayTypeFiled(ArrayTypeFiled):
    pass


class BooleanTypeFiled(TypeFiled):
    TYPE = 'boolean'

    def type_check(self, key, value):
        if isinstance(value, bool):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be bool!' % self.name)


class ObjectTypeFiled(TypeFiled):
    def __setitem__(self, key, value):
        if len(value) == 1:
            items = list(value.items())[0]
        else:
            items = value
        self.__dict__['TYPE'], self.__dict__[key] = self.type_check(key, items)

    def type_check(self, key, value):
        if isinstance(value, dict):
            return None, value
        if isinstance(value[1], dict):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be dict!' % self.name)



class Item(object):
    """
    数据类
    """
    NAME = ''  # 该字段确定返回{}或{NAME: {}}
    ITEM_TYPE = ''  # 确定item的类型，最后入库进行区分

    @property
    def item(self):
        self.start_check()
        d = {}
        for key, value in self.__dict__.items():
            check_func_name = key
            if not check_func_name.startswith('_'):
                check_func_name = '_%s' % check_func_name
            check_func_name = 'check%s' % check_func_name
            if hasattr(self, check_func_name):
                getattr(self, check_func_name)()
            d[key] = value.value
        self.end_check(d)
        if self.NAME:
            return {self.NAME.lower(): d}
        return d

    @property
    def base_item(self, ):
        self.start_check()
        d = {}
        for key, value in self.__dict__.items():
            check_func_name = key
            if not check_func_name.startswith('_'):
                check_func_name = '_%s' % check_func_name
            check_func_name = 'check%s' % check_func_name
            if hasattr(self, check_func_name):
                getattr(self, check_func_name)()
            d[key] = value.base_value
        self.end_check(d)
        if self.NAME:
            return {self.NAME.lower(): d}
        return d

    def start_check(self):
        pass

    def end_check(self, d):
        pass

    @property
    def fields(self):
        return self.__dict__.keys()

    @property
    def item_type(self):
        return self.ITEM_TYPE

    def __setitem__(self, key, value):
        self.__dict__[key]['_value'] = value

    def __getitem__(self, item):
        check_func_name = item
        if not check_func_name.startswith('_'):
            check_func_name = '_%s' % check_func_name
        check_func_name = 'check%s' % check_func_name
        if hasattr(self, check_func_name):
            getattr(self, check_func_name)()
        return self.__dict__[item].value


class RetweetedStatus(Item):
    NAME = 'retweeted_status'

    def __init__(self):
        self.id = StringTypeFiled(name='id')
        self._key = StringTypeFiled(name='_key')
        self.title = StringTypeFiled(name='title')
        self.content = StringTypeFiled(name='content')
        self.title_CN = StringTypeFiled(name='name')
        self.content_CN = StringTypeFiled(name='name')
        self.publish_time = LongTypeFiled(name='publish_time')
        self.url = StringTypeFiled(name='url')
        self.picture_urls = ArrayTypeFiled(name='picture_urls')
        self.author_id = StringTypeFiled(name='author_id')
        self.author_name = StringTypeFiled(name='author_name')


class QuotedStatus(RetweetedStatus):
    NAME = 'quoted_status'


class Vector(Item):
    def __init__(self):
        self.v = StringTypeFiled(null=False, name='v')
        self.w = IntTypeFiled(null=False, name='w')


class Member(Item):
    def __init__(self):
        self.id = StringTypeFiled(null=False, name='id')
        self.name = StringTypeFiled(null=False, name='name')


class Groups(Item):
    NAME = 'groups'

    def __init__(self):
        self.group_id = StringTypeFiled(null=False, name='group_id')
        self.group_name = StringTypeFiled(null=False, name='group_name')
        self.group_description = StringTypeFiled(name='group_description')
        self.group_owner = StringTypeFiled(null=False, name='group_owner')
        self.group_members = IntTypeFiled(null=False, name='group_members')
        self.members = ArrayTypeFiled(name='members')
        self.extra_info = StringTypeFiled(name='extra_info')

class GolaxyUserInformation(Item):
    ITEM_TYPE = 'user_information'
    "用户"
    def __init__(self):
        self.id = StringTypeFiled(null=False, name='id')
        self._ch = IntTypeFiled(null=False, name='_ch')
        self.media_id = StringTypeFiled(name='media_id')
        self.media_name = StringTypeFiled(null=False, name='media_name')
        self.uid = StringTypeFiled(null=False, name='uid')
        self.name = StringTypeFiled(null=False, name='name')
        self.screen_name = StringTypeFiled(name='screen_name')
        self.description = StringTypeFiled(name='description')
        self.realname = StringTypeFiled(name='realname')
        self.emails = ArrayTypeFiled(name='emails')
        self.phonenumbers = ArrayTypeFiled(name='phonenumbers')
        self.gender = IntTypeFiled(value=-1, name='gender')
        self.birthday = StringTypeFiled(name='birthday')
        self.profile_url = StringTypeFiled(name='profile_url')
        self.profile_image_url = StringTypeFiled(name='profile_image_url')
        self.cover_image = StringTypeFiled(name='cover_image')
        self.friends_count = IntTypeFiled(name='friends_count')
        self.bi_followers_count = IntTypeFiled(name='bi_followers_count')
        self.favourites_count = IntTypeFiled(name='favourites_count')
        self.followers_count = IntTypeFiled(name='followers_count')
        self.statuses_count = IntTypeFiled(name='statuses_count')
        self.listed_count = IntTypeFiled(name='listed_count')
        self.accounts_status = IntTypeFiled(name='accounts_status')
        self.tags = ArrayTypeFiled(name='tags')
        # self.verified = BooleanTypeFiled(value=False, name='verified')
        self.verified = BooleanTypeFiled(value=False,null=False, name='verified')
        self.verified_type = IntTypeFiled(value=-1, name='verified')
        self.verified_reason = StringTypeFiled(name='verified_reason')
        # self.is_vip = BooleanTypeFiled(value=False, name='is_vip')
        self.is_vip = BooleanTypeFiled(value=False,null=False, name='is_vip')
        self.register_time = LongTypeFiled(name='register_time')
        self.register_location = StringTypeFiled(name='register_location')
        self.register_organization = StringTypeFiled(name='register_organization')
        self.in_organizations = ArrayTypeFiled(name='in_organizations')
        self.update_time = LongTypeFiled(null=False, name='update_time')
        self.gather_time = LongTypeFiled(null=False, name='gather_time')
        self.insert_time = LongTypeFiled(null=False, name='insert_time')
        self.groups = ArrayTypeFiled(name='groups')
        self.extra_info = StringTypeFiled(name='extra_info')


class AuthorFullInfo(Item):
    NAME = 'author_full_info'

    def __init__(self):
        self.uid = StringTypeFiled(null=False, name='uid')
        self.name = StringTypeFiled(name='name')
        self.screen_name = StringTypeFiled(name='screen_name')
        self.description = StringTypeFiled(name='description')
        self.realname = StringTypeFiled(name='realname')
        self.emails = ArrayTypeFiled(name='emails')
        self.phonenumbers = ArrayTypeFiled(name='phonenumbers')
        self.gender = IntTypeFiled(null=False, name='gender')
        self.birthday = StringTypeFiled(name='birthday')
        self.profile_url = StringTypeFiled(name='profile_url')
        self.profile_image_url = StringTypeFiled(name='profile_image_url')
        self.cover_image = StringTypeFiled(name='cover_image')
        self.friends_count = IntTypeFiled(name='friends_count')
        self.bi_followers_count = IntTypeFiled(name='bi_followers_count')
        self.favourites_count = IntTypeFiled(name='favourites_count')
        self.followers_count = IntTypeFiled(name='followers_count')
        self.statuses_count = IntTypeFiled(name='statuses_count')
        self.listed_count = IntTypeFiled(name='listed_count')
        self.accounts_status = IntTypeFiled(name='accounts_status')
        self.tags = ArrayTypeFiled(name='tags')
        self.verified = BooleanTypeFiled(False, null=False, name='verified')
        self.verified_type = IntTypeFiled(1, null=False, name='verified_type')
        self.verified_reason = StringTypeFiled(name='verified_reason')
        self.is_vip = BooleanTypeFiled(False, null=False, name='is_vip')
        self.register_time = LongTypeFiled(name='register_time')
        self.register_location = StringTypeFiled(name='register_location')
        self.register_organization = StringTypeFiled(name='register_organization')
        self.in_organizations = ArrayTypeFiled(name='in_organizations')
        self.groups = ObjectTypeFiled(name='groups')
        self.extra_info = StringTypeFiled(name='extra_info')


class GolaxyDataItem(Item):
    def __init__(self):
        self.id = StringTypeFiled(null=False, name='id')
        self._ch = IntTypeFiled(null=False, name='_ch')
        self._key = StringTypeFiled(null=False, name='_key')
        self._spec = StringTypeFiled(null=False, name='_spec')
        self._dcm = StringTypeFiled(null=False, name='_dcm', value="监控采集")
        self._adp = StringTypeFiled('中科天玑', null=False, name='_adp')
        self.lang = StringTypeFiled('zh', name='lang')
        self.title = StringTypeFiled(name='title')
        self.content = StringTypeFiled(name='content')
        self.abstract = StringTypeFiled(name='abstract')
        self.content_raw = StringTypeFiled(name='content_raw')
        self.title_CN = StringTypeFiled(name='title_CN')
        self.content_CN = StringTypeFiled(name='content_CN')
        self.abstract_CN = StringTypeFiled(name='abstract_CN')
        self.tags = ArrayTypeFiled(name='tags')
        self.source = StringTypeFiled(name='source')
        self.update_time = LongTypeFiled(null=False, name='update_time')
        self.gather_time = LongTypeFiled(null=False, name='gather_time')
        self.insert_time = LongTypeFiled(null=False, name='insert_time')
        self.publish_time = LongTypeFiled(null=False, name='publish_time')
        self.cover_image_urls = ArrayTypeFiled(name='cover_image_urls')
        self.picture_urls = ArrayTypeFiled(name='picture_urls')
        self.audio_urls = ArrayTypeFiled(name='audio_urls')
        self.video_urls = ArrayTypeFiled(name='video_urls')
        self.file_urls = ArrayTypeFiled(name='file_urls')
        self.picture_paths = ArrayTypeFiled(name='picture_paths')
        self.audio_paths = ArrayTypeFiled(name='audio_paths')
        self.video_paths = ArrayTypeFiled(name='video_paths')
        self.file_paths = ArrayTypeFiled(name='file_paths')
        self.picture_contents = ArrayTypeFiled(name='picture_contents')
        self.audio_contents = ArrayTypeFiled(name='audio_contents')
        self.video_contents = ArrayTypeFiled(name='video_contents')
        self.media_id = StringTypeFiled(name='media_id')
        self.media_name = StringTypeFiled(null=False, name='media_name')
        self.media_url = StringTypeFiled(name='media_url')
        self.media_location = ArrayTypeFiled(name='media_location')
        self.board_id = StringTypeFiled(name='board_id')
        self.board_name = StringTypeFiled(name='board_name')
        self.board_url = StringTypeFiled(name='board_url')
        self.board_name_full = ArrayTypeFiled(name='board_name_full')
        self.url = StringTypeFiled(name='url')
        self.reposts_count = IntTypeFiled(name='reposts_count')
        self.likes_count = IntTypeFiled(name='likes_count')
        self.dislikes_count = IntTypeFiled(name='dislikes_count')
        self.views_count = IntTypeFiled(name='views_count')
        self.comments_count = IntTypeFiled(name='comments_count')
        self.attitudes_count = IntTypeFiled(name='attitudes_count')
        self.favourites_count = IntTypeFiled(name='favourites_count')
        self.quoted_count = IntTypeFiled(name='quoted_count')
        self.viewing_count = IntTypeFiled(name='viewing_count')
        self.play_count = IntTypeFiled(name='play_count')
        self.share_count = IntTypeFiled(name='share_count')
        self.danmaku_count = IntTypeFiled(name='danmaku_count')
        self.keywords = ArrayTypeFiled(name='keywords')
        self.keywords_vector = ObjectArrayTypeFiled(name='keywords_vector')
        self.persons_vector = ObjectArrayTypeFiled(name='persons_vector')
        self.organizations_vector = ObjectArrayTypeFiled(name='organizations_vector')
        self.regions_vector = ObjectArrayTypeFiled(name='regions_vector')
        self.message_type = IntTypeFiled(1, null=False, name='message_type')
        self.mention_list = ArrayTypeFiled(name='mention_list')
        self.topic_list = ArrayTypeFiled(name='topic_list')
        self.post_location = ArrayTypeFiled(name='post_location')
        self.post_location_geo = ArrayTypeFiled(name='post_location_geo')
        self.root_id = StringTypeFiled(name='root_id')
        self.parent_id = StringTypeFiled(name='parent_id')
        self.retweeted_status = ObjectTypeFiled(name='retweeted_status')
        self.quoted_status = ObjectTypeFiled(name='quoted_status')
        self.sentiment = IntTypeFiled(0, null=False, name='sentiment')
        self.similar_id = StringTypeFiled(name='similar_id')
        self.is_public = IntTypeFiled(1, null=False, name='is_public')
        self.author_id = StringTypeFiled(name='author_id')
        self.author_name = StringTypeFiled(name='author_name')
        self.author_screen_name = StringTypeFiled(name='author_screen_name')
        self.author_full_info = ObjectTypeFiled(name='author_full_info')
        self.group_id = StringTypeFiled(name='group_id')
        self.group_name = StringTypeFiled(name='group_name')
        self.extra_info = StringTypeFiled(name='extra_info')

        self.now = IntTypeFiled(int(time.time()), null=False)  # 非提交

    def end_check(self, d):
        del d['now']


class GolaxyNewsDataItem(GolaxyDataItem):
    ITEM_TYPE = 'news'

    def check_id(self):
        if not self._key.base_value:
            self.check_key()
        if not self._ch.base_value:
            self.check_ch()
        ch = str(self._ch.base_value).rjust(2, '0')
        self.id._value = '%s%s' % (ch, self._key.base_value)

    def check_ch(self):
        if not self._ch.base_value:
            raise DataCheckException('The attribute _ch must have value!')

    def check_key(self):
        if not self.url.base_value:
            self.check_url()
        self._key._value = security.EncryptUtils.md5(self.url.base_value)

    def check_spec(self):
        if not self._spec.base_value:
            raise DataCheckException('The attribute _spec must have value!')

    def check_dcm(self):
        if not self._dcm.base_value:
            raise DataCheckException('The attribute _dcm must have value!')

    def check_url(self):
        if not self.url.base_value:
            raise DataCheckException('The attribute url must have value!')

    def check_update_time(self):
        if not self.update_time.base_value:
            self.update_time._value = mix.DateTimeUtils.unify_time_stamp(time_data=self.now.base_value)
            self.gather_time._value = self.update_time.base_value
            self.insert_time._value = self.update_time.base_value

    def check_publish_time(self):
        self.publish_time._value = mix.DateTimeUtils.unify_time_stamp(time_data=self.publish_time.base_value)
        if not self.publish_time.base_value:
            self.publish_time._value = self.update_time.base_value

    def check_title(self):
        title = self.title.base_value
        if not title:
            raise DataCheckException("The attribute title must have value!")
        split_regex = None
        merge_sep = ''
        if self.lang.base_value != 'zh':
            split_regex = r'\S+'
            merge_sep = ' '
        title_words = base.TextUtils.split_text(title, regex=split_regex)
        if len(title_words) > 25:
            self.title._value = base.TextUtils.merge(title_words[:25], merge_sep=merge_sep) + '...'

    def check_content(self):
        if not self.content.base_value:
            raise DataCheckException("The attribute content must have value!")

    def check_content_raw(self):
        if not self.content_raw.base_value:
            self.content_raw._value = self.content.base_value

# 点评赞
class GolaxyUserBehaviorItem(GolaxyDataItem):
    ITEM_TYPE = 'user_behavior'
    def check_update_time(self):
        if not self.update_time.base_value:
            self.update_time._value = mix.DateTimeUtils.unify_time_stamp(time_data=self.now.base_value)
            self.gather_time._value = self.update_time.base_value
            self.insert_time._value = self.update_time.base_value

    def check_publish_time(self):
        self.publish_time._value = mix.DateTimeUtils.unify_time_stamp(time_data=self.publish_time.base_value)
        if not self.publish_time.base_value:
            self.publish_time._value = self.update_time.base_value

class GolaxyAppNewsDataItem(GolaxyNewsDataItem):
    ITEM_TYPE = 'app_news'



class GolaxyAppNewsCommentsDataItem(GolaxyDataItem):
    ITEM_TYPE = 'app_news_comments'


class GolaxyWenDaDataItem(GolaxyDataItem):
    ITEM_TYPE = 'wenda'


class GolaxyZhiKuDataItem(GolaxyNewsDataItem):
    ITEM_TYPE = 'zhiku'


class GolaxyOldAppNewsDataItem(Item):
    ITEM_TYPE = 'old_app_news'

    def __init__(self):
        self._id = StringTypeFiled(null=False, name='_id')
        self._key = StringTypeFiled(null=False, name='_key')
        self._ch = IntTypeFiled(null=False, name='_ch')
        self._spec = StringTypeFiled(null=False, name='_spec')
        self.lang = StringTypeFiled(null=False, value='zh', name='lang')
        self.url = StringTypeFiled(null=False, name='url')
        self.pt = IntTypeFiled(null=False, name='pt')
        self.title = StringTypeFiled(null=False, name='title')
        self.cont = StringTypeFiled(null=False, name='cont')
        self.author = StringTypeFiled(null=False, value='', name='author')
        self.i_bid = IntTypeFiled(null=False, name='i_bid')
        self.i_bn = StringTypeFiled(null=False, name='i_bn')
        self.i_sid = IntTypeFiled(null=False, name='i_sid')
        self.i_sn = StringTypeFiled(null=False, name='i_sn')
        self.loc = StringTypeFiled(null=False, value='', name='loc')
        self._ex = IntTypeFiled(null=False, value=0, name='_ex')
        self.gt = IntTypeFiled(null=False, value=0, name='gt')
        self.it = IntTypeFiled(null=False, value=0, name='it')
        self.ut = IntTypeFiled(null=False, value=0, name='ut')
        self.abstr = StringTypeFiled(null=False, value='', name='abstr')
        self.lpic = ArrayTypeFiled(null=False, value=[], name='lpic')
        self.lvideo = ArrayTypeFiled(null=False, value=[], name='lvideo')
        self.lkey = ArrayTypeFiled(null=False, value=[], name='lkey')
        self.vkey = ArrayTypeFiled(null=False, value=[], name='vkey')
        self.vpers = ArrayTypeFiled(null=False, value=[], name='vpers')
        self.vorg = ArrayTypeFiled(null=False, value=[], name='vorg')
        self.vrgn = ArrayTypeFiled(null=False, value=[], name='vrgn')
        self.sent = IntTypeFiled(null=False, value=0, name='sent')
        self.adp = StringTypeFiled(null=False, value='中科天玑', name='adp')
        self.nrd = IntTypeFiled(null=False, value=0, name='nrd')
        self.nrply = IntTypeFiled(null=False, value=0, name='nrply')
        self.purl = StringTypeFiled(null=False, value='', name='purl')


class GolaxyOldNewsDataItem(GolaxyOldAppNewsDataItem):
    ITEM_TYPE = 'old_news'

    def __init__(self):
        self.raw_cont = StringTypeFiled(null=False, value='', name='raw_cont')
        self.source = StringTypeFiled(null=False, value='', name='source')
        super(GolaxyOldNewsDataItem, self).__init__()


class GolaxyRecruitDataItem(Item):
    ITEM_TYPE = 'recruit'

    def __init__(self):
        self._id = StringTypeFiled(null=False, name='_id')
        self._key = StringTypeFiled(null=False, name='_key')
        self._ch = IntTypeFiled(null=False, name='_ch')
        self._spec = StringTypeFiled(null=False, name='_spec')
        self.lang = StringTypeFiled(null=False, value='zh', name='lang')
        self.url = StringTypeFiled(null=False, name='url')
        self._dcm = StringTypeFiled(null=False, name='_dcm', value="监控采集")
        self._adp = StringTypeFiled(null=False, value='中科天玑', name='_adp')
        self.tags = ArrayTypeFiled(null=False, value=[], name='tags')
        self.gather_time = IntTypeFiled(null=False, value=0, name='gather_time')
        self.update_time = IntTypeFiled(null=False, value=0, name='update_time')
        self.insert_time = IntTypeFiled(null=False, value=0, name='insert_time')
        self.publish_time = IntTypeFiled(null=False, value=0, name='publish_time')
        self.site_id = IntTypeFiled(null=False, name='site_id')
        self.site_name = StringTypeFiled(null=False, name='site_name')
        self.job_name = StringTypeFiled(null=False, value='', name='job_name')
        self.job_salary = StringTypeFiled(null=False, value='', name='job_salary')
        self.job_education = StringTypeFiled(null=False, value='', name='job_education')
        self.job_number = StringTypeFiled(null=False, value='', name='job_number')
        self.job_date_range = StringTypeFiled(null=False, value='', name='job_date_range')
        self.job_description = StringTypeFiled(null=False, value='', name='job_description')
        self.job_description_raw = StringTypeFiled(null=False, value='', name='job_description_raw')
        self.job_department = StringTypeFiled(null=False, value='', name='job_department')
        self.job_address = StringTypeFiled(null=False, value='', name='job_address')
        self.job_experience = StringTypeFiled(null=False, value='', name='job_experience')
        self.job_recruiter = StringTypeFiled(null=False, value='', name='job_recruiter')
        self.job_recruiter_position = StringTypeFiled(null=False, value='', name='job_recruiter_position')
        self.job_advantage = StringTypeFiled(null=False, value='', name='job_advantage')
        self.company_name = StringTypeFiled(null=False, value='', name='company_name')
        self.company_home_url = StringTypeFiled(null=False, value='', name='company_home_url')
        self.company_logo = StringTypeFiled(null=False, value='', name='company_logo')
        self.company_industry = StringTypeFiled(null=False, value='', name='company_industry')
        self.company_development_stage = StringTypeFiled(null=False, value='', name='company_development_stage')
        self.company_scale = StringTypeFiled(null=False, value='', name='company_scale')
        self.company_description = StringTypeFiled(null=False, value='', name='company_description')
        self.company_business_info = ObjectTypeFiled(null=False, name='company_business_info')
        self.extra_info = StringTypeFiled(null=False, value='', name='job_name')
        self.now = IntTypeFiled(int(time.time()), null=False)

    def end_check(self, d):
        del d['now']


class GolaxyCompanyBusinessInfoDataItem(Item):
    def __init__(self):
        self.company_name = StringTypeFiled(null=False, value='', name='company_name')
        self.legal_representative = StringTypeFiled(null=False, value='', name='legal_representative')
        self.registered_capital = StringTypeFiled(null=False, value='', name='registered_capital')
        self.foundation_date = StringTypeFiled(null=False, value='', name='foundation_date')
        self.business_type = StringTypeFiled(null=False, value='', name='business_type')
        self.business_status = StringTypeFiled(null=False, value='', name='business_status')
        self.registered_address = StringTypeFiled(null=False, value='', name='registered_address')
        self.uniform_code = StringTypeFiled(null=False, value='', name='uniform_code')
        self.business_scope = StringTypeFiled(null=False, value='', name='business_scope')
        self.extra_info = StringTypeFiled(null=False, value='', name='extra_info')


class GolaxyUserRelationShip(Item):
    ITEM_TYPE = 'relationship'

    def __init__(self):
        self.id = StringTypeFiled(null=False, name='id')
        self._ch = IntTypeFiled(null=False, name='_ch')
        self.owner_uid = StringTypeFiled(null=False, name='owner_uid')
        self.owner_name = StringTypeFiled(null=False, name='owner_name')
        self.owner_screen_name = StringTypeFiled(name='owner_screen_name')
        self.uid = StringTypeFiled(null=False, name='uid')
        self.name = StringTypeFiled(null=False, name='name')
        self.screen_name = StringTypeFiled(name='screen_name')
        self.media_id = StringTypeFiled(name='media_id')
        self.media_name = StringTypeFiled(null=False, name='media_name')
        self.profile_image_url = StringTypeFiled(name='profile_image_url')
        self.description = StringTypeFiled(name='description')
        self.register_time = LongTypeFiled(name='register_time')
        self.register_location = StringTypeFiled(name='register_location')
        self.bi_followers_count = IntTypeFiled(name='bi_followers_count')
        self.followers_count = IntTypeFiled(name='followers_count')
        self.friends_count = IntTypeFiled(name='friends_count')
        self.statuses_count = IntTypeFiled(name='statuses_count')
        self.relationship_type = StringTypeFiled(null=False, name='relationship_type')
        self.update_time = LongTypeFiled(null=False, name='update_time')
        self.gather_time = LongTypeFiled(null=False, name='gather_time')
        self.insert_time = LongTypeFiled(null=False, name='insert_time')



def new2old(item):
    old_item = None
    if item.item_type == 'news':
        old_item = GolaxyOldNewsDataItem()
        item = item.base_item
        old_item['_id'] = item['id']
        old_item['_key'] = item['_key']
        old_item['_ch'] = item['_ch']
        old_item['_spec'] = item['_spec']
        old_item['url'] = item['url']
        old_item['pt'] = item['publish_time']
        old_item['title'] = item['title']
        old_item['cont'] = item['content']
        old_item['author'] = item['author_name'] or ''
        old_item['i_bid'] = int(item['board_id'])
        old_item['i_bn'] = item['board_name']
        old_item['i_sid'] = int(item['media_id'])
        old_item['i_sn'] = item['media_name']
        old_item['loc'] = ','.join(item['media_location'])
        old_item['gt'] = item['gather_time']
        old_item['it'] = item['insert_time']
        old_item['ut'] = item['update_time']
        if item['abstract']:
            old_item['abstr'] = item['abstract']
        if item['picture_urls']:
            old_item['lpic'] = item['picture_urls']
        if item['video_urls']:
            old_item['lvideo'] = item['video_urls']
        if item['content_raw']:
            old_item['raw_cont'] = item['content_raw']
        if item['source']:
            old_item['source'] = item['source']
    elif item.item_type == 'app_news':
        old_item = GolaxyOldAppNewsDataItem()
        item = item.base_item
        old_item['_id'] = item['id']
        old_item['_key'] = item['_key']
        old_item['_ch'] = item['_ch']
        old_item['_spec'] = item['_spec']
        old_item['url'] = item['url']
        old_item['pt'] = item['publish_time']
        old_item['title'] = item['title']
        old_item['cont'] = item['content']
        old_item['author'] = item['author_name']
        old_item['i_bid'] = int(item['board_id'])
        old_item['i_bn'] = item['board_name']
        old_item['i_sid'] = int(item['media_id'])
        old_item['i_sn'] = item['media_name']
        old_item['loc'] = ','.join(item['media_location'])
        old_item['gt'] = item['gather_time']
        old_item['it'] = item['insert_time']
        old_item['ut'] = item['update_time']
        if item['abstract']:
            old_item['abstr'] = item['abstract']
        if item['picture_urls']:
            old_item['lpic'] = item['picture_urls']
        if item['video_urls']:
            old_item['lvideo'] = item['video_urls']
    return old_item


class Filed(object):
    """
    字段规范
    """

    def __init__(self, value=None, null=True, name=''):
        self._value = value
        self.null = null
        self.name = name

    @property
    def value(self):
        if self.null:
            return self._value
        if self._value is None:
            raise DataCheckException('The Filed %s must have value!' % self.name)
        return self._value

    def type_check(self, key, value):
        raise NotImplemented

    def __setitem__(self, key, value):
        self.__dict__[key] = self.type_check(key, value)

    def __getitem__(self, item):
        return self.__dict__[item]


class IntFiled(Filed):
    def type_check(self, key, value):
        if isinstance(value, int):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be int!' % self.name)


class StringFiled(Filed):

    def type_check(self, key, value):
        if isinstance(value, str):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be str!' % self.name)


class ListFiled(Filed):
    def type_check(self, key, value):
        if isinstance(value, list):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be list!' % self.name)


class DictFiled(Filed):
    def type_check(self, key, value):
        if isinstance(value, dict):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be list!' % self.name)


class BoolFiled(Filed):
    def type_check(self, key, value):
        if isinstance(value, bool):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be bool!' % self.name)


class DBItem(object):
    @property
    def item(self):
        self.start_check()
        d = {}
        for key, value in self.__dict__.items():
            check_func_name = key
            if not check_func_name.startswith('_'):
                check_func_name = '_%s' % check_func_name
            check_func_name = 'check%s' % check_func_name
            if hasattr(self, check_func_name):
                getattr(self, check_func_name)()
            d[key] = value.value
        self.end_check(d)
        return d

    def start_check(self):
        pass

    def end_check(self, d):
        pass

    @property
    def fields(self):
        return self.__dict__.keys()

    def __setitem__(self, key, value):
        self.__dict__[key]['_value'] = value

    def __getitem__(self, item):
        check_func_name = item
        if not check_func_name.startswith('_'):
            check_func_name = '_%s' % check_func_name
        check_func_name = 'check%s' % check_func_name
        if hasattr(self, check_func_name):
            getattr(self, check_func_name)()
        return self.__dict__[item].value


class GolaxyWemediaUserOldItem(DBItem):
    def __init__(self):
        self.wemedia_name = StringFiled(null=False, name='wemedia_name')
        self.wemedia_home_url = StringFiled(null=False, name='wemedia_home_url')
        self.user_name = StringFiled(null=False, name='user_name')
        self.user_id = StringFiled(null=False, name='user_id')
        self.registration_date = StringFiled(null=False, name='registration_date')
        self.user_home_url = StringFiled(null=False, name='user_home_url')
        self.description = StringFiled(value='', name='description')
        self.user_avatar_url = StringFiled(null=False, value='', name='user_avatar_url')
        self.follow_count = IntFiled(value=0, name='follow_count')
        self.digg_count = IntFiled(value=0, name='digg_count')
        self.collection_count = IntFiled(value=0, name='collection_count')
        self.publish_count = IntFiled(value=0, name='publish_count')
        self.auth_type = StringFiled(value='', name='auth_type')
        self.auth_info = StringFiled(value='', name='auth_info')
        self.country = StringFiled(value='中国', name='country')
        self.province = StringFiled(value='北京', name='province')
        self.city = StringFiled(value='北京', name='city')
        self.insert_time = IntFiled(value=0, name='insert_time')
        self.update_time = IntFiled(value=0, name='update_time')
        self.cnt = IntFiled(value=0, name='cnt')


class GolaxyWemediaUserSchedulerItem(DBItem):
    def __init__(self):
        self.md5 = StringFiled(null=False, name='md5')
        self.wemedia_id = IntFiled(null=False, name='wemedia_id')
        self.wemedia_name = StringFiled(null=False, name='wemedia_name')
        self.wemedia_board = StringFiled(null=False, value='all', name='wemedia_board')
        self.user_id = StringFiled(null=False, name='user_id')
        self.user_name = StringFiled(null=False, name='user_name')
        self.publish_count = IntFiled(value=0, name='publish_count')
        self.publish_day_count = IntFiled(value=0, name='publish_day_count')
        self.meta = StringFiled(name='meta')

    def check_md5(self):
        if not self.md5._value:
            self.md5._value = security.EncryptUtils.md5(
                '%s%s%s' % (str(self.wemedia_id.value), self.wemedia_board.value, self.user_id.value))


if __name__ == '__main__':
    import json

    data_item = GolaxyDataItem()
    data_item['_ch'] = 27
    # data_item['id'] = "271247754273992403"
    # data_item['_key'] = "1247754273992403"
    data_item['_spec'] = "M-TELEGRAM02-AI"
    data_item['_dcm'] = "监控采集"
    data_item['content'] = "德国是我们的老师"
    data_item['publish_time'] = 1625619982000
    data_item['update_time'] = 1625619982000
    data_item['gather_time'] = 1625619982000
    data_item['insert_time'] = 1625619982000
    data_item['author_id'] = "1087968824"
    data_item['author_name'] = "Group"
    data_item['media_name'] = ""
    data_item['url'] = "11"

    groups = Groups()
    groups['group_id'] = "1247754273"
    groups['group_name'] = "第六共产国际Sixth Rome"
    groups['group_members'] = -1
    groups['group_owner'] = ''

    author_full_info = AuthorFullInfo()
    author_full_info['uid'] = "1087968824"
    author_full_info['name'] = "Group"
    author_full_info['gender'] = -1
    author_full_info['groups'] = groups.item
    author_full_info['phonenumbers'] = ["111", "222"]

    data_item['author_full_info'] = author_full_info.item
    res = data_item.item

    print(json.dumps(res, ensure_ascii=False))
