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


class GolaxyDataItem(object):
    ITEM_TYPE = 'golaxy_data_item'

    def __init__(self, **kwargs):
        self._id = None
        self._key = None
        self._ch = None
        self._spec = None
        self.lang = 'zh'
        self.url = None

        self.now = time.time()  # 非提交数据
        self.__dict__.update(**kwargs)

    def _clean_key(self):
        if not self.url:
            self._clean_url()
        self._key = security.EncryptUtils.md5(self.url)

    def _clean_id(self):
        if not self._key:
            self._clean_key()
        if not self._ch:
            self._clean_ch()
        ch = self._ch
        if ch < 10:
            ch = '0%s' % ch
        self._id = '%s%s' % (ch, self._key)

    def _clean_ch(self):
        if not self._ch:
            raise Exception('The _ch of item is not None')

    def _clean_url(self):
        if not self.url:
            raise Exception('The url of item is not None')

    def _clean_spec(self):
        if not self._spec:
            raise Exception('The _spec of item is not None')

    @property
    def item(self):
        return self.__dict__

    @property
    def item_type(self):
        return self.ITEM_TYPE

    def confirm(self):
        getattr(self, 'start_clean')()
        for field in list(self.__dict__.keys()):
            if not field.startswith('_'):
                field = '_%s' % field
            clean_field_method = '_clean%s' % field
            if hasattr(self, clean_field_method):
                getattr(self, clean_field_method)()
        getattr(self, 'end_clean')()

    def start_clean(self):
        pass

    def end_clean(self):
        del self.now

    def __setitem__(self, key, value):
        if value is not None:
            self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return json.dumps(self.item, ensure_ascii=False)


class GolaxyNewsDataItem(GolaxyDataItem):
    pass


class GolaxyAppNewsDataItem(GolaxyNewsDataItem):
    ITEM_TYPE = 'golaxy_app_news_data_item'

    def __init__(self, **kwargs):
        self.pt = None  # 发布时间，13位int
        self.title = ''  # 标题,int
        self.cont = ''  # 去标签正文,str
        self.author = ''  # 作者,str
        self.i_bid = None  # 板块id，int
        self.i_bn = None  # 板块名称,str
        self.i_sid = None  # 网站id,int
        self.i_sn = None  # 网站名称,str
        self.loc = '中国,北京'  # 地区,str
        self._ex = 0
        self.gt = None
        self.it = None
        self.ut = None
        self.abstr = ''
        self.lpic = list()
        self.lvideo = list()
        self.lkey = list()
        self.vkey = list()
        self.vpers = list()
        self.vorg = list()
        self.vrgn = list()
        self.sent = 0
        self.adp = '中科天玑'
        self.nrd = 0
        self.nrply = 0
        self.purl = None
        super(GolaxyAppNewsDataItem, self).__init__(**kwargs)

    def _clean_purl(self):
        if not self.purl:
            self.purl = self.url

    def _clean_ut(self):
        if not self.ut:
            self.ut = self.gt

    def _clean_it(self):
        if not self.it:
            self.it = self.gt

    def _clean_gt(self):
        if not self.gt:
            self.gt = mix.DateTimeUtils.unify_time_stamp(self.now)

    def _clean_i_sn(self):
        if not self.i_sn:
            raise Exception('The i_sn of item is not None')

    def _clean_i_sid(self):
        if not self.i_sid:
            raise Exception('The i_sid of item is not None')

    def _clean_i_bn(self):
        if not self.i_bn:
            raise Exception('The i_bn of item is not None')

    def _clean_pt(self):
        if not self.pt:
            self.pt = self.now
        self.pt = mix.DateTimeUtils.unify_time_stamp(self.pt)

    def _clean_title(self):
        if not self.title:
            raise Exception('The title of item is not None')
        if len(self.title) > 25:
            self.title = self.title[:25]

    def _clean_cont(self):
        if not self.cont:
            raise Exception('The cont of item is not None')

    def _clean_lang(self):
        if not self.lang:
            raise Exception('The lang of item is not None')

    def _clean_i_bid(self):
        if not self.i_bid:
            raise Exception('The i_bid of item is not None')


class GolaxyWebNewsDataItem(GolaxyAppNewsDataItem):
    ITEM_TYPE = 'golaxy_web_news_data_item'

    def __init__(self, **kwargs):
        self.raw_cont = ''
        self.source = ''
        super(GolaxyWebNewsDataItem, self).__init__(**kwargs)

    def _clean_source(self):
        if not self.source:
            self.source = self.author


class GolaxyWemediaNewsDataItem(GolaxyWebNewsDataItem):
    ITEM_TYPE = 'golaxy_wemedia_news_data_item'

    def _clean_author(self):
        if not self.author:
            raise Exception('The i_author of item is not None')


class GolaxyWemediaAppNewsDataItem(GolaxyAppNewsDataItem):
    ITEM_TYPE = 'golaxy_wemedia_app_news_data_item'

    def _clean_author(self):
        if not self.author:
            raise Exception('The i_author of item is not None')


class GolaxyRecruitWebDataItem(GolaxyDataItem):
    ITEM_TYPE = 'golaxy_recruit_web_data_item'

    def __init__(self, **kwargs):
        self._dcm = None
        self._adp = '中科天玑'
        self.tags = []
        self.gather_time = None
        self.update_time = None
        self.insert_time = None
        self.publish_time = None
        self.site_id = None
        self.site_name = None
        self.job_name = ''
        self.job_salary = ''
        self.job_education = ''
        self.job_number = ''
        self.job_date_range = ''
        self.job_description = ''
        self.job_description_raw = ''
        self.job_department = ''
        self.job_address = ''
        self.job_experience = ''
        self.job_recruiter = ''
        self.job_recruiter_position = ''
        self.job_advantage = ''
        self.company_name = ''
        self.company_home_url = ''
        self.company_logo = ''
        self.company_industry = ''
        self.company_development_stage = ''
        self.company_scale = ''
        self.company_description = ''
        self.company_business_info = {
            'company_name': '',
            'legal_representative': '',
            'registered_capital': '',
            'foundation_date': '',
            'business_type': '',
            'business_status': '',
            'registered_address': '',
            'uniform_code': '',
            'business_scope': '',
            'extra_info': '',
        }
        self.extra_info = ''
        super(GolaxyRecruitWebDataItem, self).__init__(**kwargs)

    def _clean_company_name(self):
        if not self.company_name:
            raise Exception('The company_name of item is not None')

    def _clean_site_name(self):
        if not self.site_name:
            raise Exception('The site_name of item is not None')

    def _clean_site_id(self):
        if not self.site_id:
            raise Exception('The site_id of item is not None')

    def _clean_update_time(self):
        if not self.update_time:
            self.update_time = self.gather_time

    def _clean_insert_time(self):
        if not self.insert_time:
            self.insert_time = self.gather_time

    def _clean_gather_time(self):
        if not self.gather_time:
            self.gather_time = mix.DateTimeUtils.unify_time_stamp(self.now)

    def _clean_publish_time(self):
        if not self.publish_time:
            self.publish_time = self.gather_time
        self.publish_time = mix.DateTimeUtils.unify_time_stamp(self.publish_time)


# class GolaxyZhiKuDataItem(GolaxyNewDataItem):
#     ITEM_TYPE = 'golaxy_zhiku_data_item'


# 新标准
class DataTypeException(Exception):
    pass


class DataCheckException(Exception):
    pass


class Filed(object):
    """
    字段规范
    """
    TYPE = ''

    def __init__(self, _value=None, null=True, name=''):
        self._value = _value
        self.null = null
        self.name = name

    @property
    def value(self):
        if self._value is None:
            if self.null:
                return None
            # raise Exception('The Filed must have value!')
        if self.null:
            return {
                self.TYPE: self._value
            }
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


class IntFiled(Filed):
    TYPE = 'int'

    def type_check(self, key, value):
        if isinstance(value, int):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be int!' % self.name)


class LongFiled(IntFiled):
    TYPE = 'long'


class StringFiled(Filed):
    TYPE = 'string'

    def type_check(self, key, value):
        if isinstance(value, str):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be str!' % self.name)


class ArrayFiled(Filed):
    TYPE = 'array'

    def type_check(self, key, value):
        if isinstance(value, list):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be list!' % self.name)


class ObjectArrayFiled(ArrayFiled):
    pass


class BooleanFiled(Filed):
    TYPE = 'boolean'

    def type_check(self, key, value):
        if isinstance(value, bool):
            return value
        if self.null and value is None:
            return value
        raise DataTypeException('The %s must be bool!' % self.name)


class ObjectFiled(Filed):
    def __setitem__(self, key, value):
        items = list(value.items())[0]
        self.__dict__['TYPE'], self.__dict__[key] = self.type_check(key, items)

    def type_check(self, key, value):
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
        return self.__dict__[item].value


class RetweetedStatus(Item):
    NAME = 'retweeted_status'

    def __init__(self):
        self._id = StringFiled(name='_id')
        self._key = StringFiled(name='_key')
        self.title = StringFiled(name='title')
        self.content = StringFiled(name='content')
        # self.title_CN = StringFiled(name='name')
        # self.content_CN = StringFiled(name='name')
        self.publish_time = LongFiled(name='publish_time')
        self.url = StringFiled(name='url')
        self.picture_urls = ArrayFiled(name='picture_urls')
        self.author_id = StringFiled(name='author_id')
        self.author_name = StringFiled(name='author_name')


class QuotedStatus(RetweetedStatus):
    NAME = 'quoted_status'


class Vector(Item):
    def __init__(self):
        self.v = StringFiled(null=False, name='v')
        self.w = IntFiled(null=False, name='w')


class Member(Item):
    def __init__(self):
        self.id = StringFiled(null=False, name='id')
        self.name = StringFiled(null=False, name='name')


class Groups(Item):
    NAME = 'groups'

    def __init__(self):
        self.group_id = StringFiled(null=False, name='group_id')
        self.group_name = StringFiled(null=False, name='group_name')
        self.group_description = StringFiled(name='group_description')
        self.group_owner = StringFiled(null=False, name='group_owner')
        self.group_members = IntFiled(null=False, name='group_members')
        self.members = ArrayFiled(name='members')
        self.extra_info = StringFiled(name='extra_info')


class AuthorFullInfo(Item):
    NAME = 'author_full_info'

    def __init__(self):
        self.uid = StringFiled(null=False, name='uid')
        self.name = StringFiled(name='name')
        self.screen_name = StringFiled(name='screen_name')
        self.description = StringFiled(name='description')
        self.realname = StringFiled(name='realname')
        self.emails = ArrayFiled(name='emails')
        self.phonenumbers = ArrayFiled(name='phonenumbers')
        self.gender = IntFiled(null=False, name='gender')
        self.birthday = StringFiled(name='birthday')
        self.profile_url = StringFiled(name='profile_url')
        self.profile_image_url = StringFiled(name='profile_image_url')
        self.cover_image = StringFiled(name='cover_image')
        self.friends_count = IntFiled(name='friends_count')
        self.bi_followers_count = IntFiled(name='bi_followers_count')
        self.favourites_count = IntFiled(name='favourites_count')
        self.followers_count = IntFiled(name='followers_count')
        self.statuses_count = IntFiled(name='statuses_count')
        self.listed_count = IntFiled(name='listed_count')
        self.accounts_status = IntFiled(name='accounts_status')
        self.tags = ArrayFiled(name='tags')
        self.verified = BooleanFiled(False, null=False, name='verified')
        self.verified_type = IntFiled(1, null=False, name='verified_type')
        self.verified_reason = StringFiled(name='verified_reason')
        self.is_vip = BooleanFiled(False, null=False, name='is_vip')
        self.register_time = LongFiled(name='register_time')
        self.register_location = StringFiled(name='register_location')
        self.register_organization = StringFiled(name='register_organization')
        self.in_organizations = ArrayFiled(name='in_organizations')
        self.groups = ObjectFiled(name='groups')
        self.extra_info = StringFiled(name='extra_info')


class _GolaxyDataItem(Item):
    def __init__(self):
        self._id = StringFiled(null=False, name='_id')
        self._ch = IntFiled(null=False, name='_ch')
        self._key = StringFiled(null=False, name='_key')
        self._spec = StringFiled(null=False, name='_spec')
        self._dcm = StringFiled(null=False, name='_dcm')
        self._adp = StringFiled('中科天玑', null=False, name='_adp')
        self.lang = StringFiled('zh', name='lang')
        self.title = StringFiled(name='title')
        self.content = StringFiled(name='content')
        self.abstract = StringFiled(name='abstract')
        self.content_raw = StringFiled(name='content_raw')
        self.title_CN = StringFiled(name='title_CN')
        self.content_CN = StringFiled(name='content_CN')
        self.abstract_CN = StringFiled(name='abstract_CN')
        self.tags = ArrayFiled(name='tags')
        self.source = StringFiled(name='source')
        self.update_time = LongFiled(null=False, name='update_time')
        self.gather_time = LongFiled(null=False, name='gather_time')
        self.insert_time = LongFiled(null=False, name='insert_time')
        self.publish_time = LongFiled(null=False, name='publish_time')
        self.cover_image_urls = ArrayFiled(name='cover_image_urls')
        self.picture_urls = ArrayFiled(name='picture_urls')
        self.audio_urls = ArrayFiled(name='audio_urls')
        self.video_urls = ArrayFiled(name='video_urls')
        self.file_urls = ArrayFiled(name='file_urls')
        self.picture_paths = ArrayFiled(name='picture_paths')
        self.audio_paths = ArrayFiled(name='audio_paths')
        self.video_paths = ArrayFiled(name='video_paths')
        self.file_paths = ArrayFiled(name='file_paths')
        self.picture_contents = ArrayFiled(name='picture_contents')
        self.audio_contents = ArrayFiled(name='audio_contents')
        self.video_contents = ArrayFiled(name='video_contents')
        self.media_id = StringFiled(name='media_id')
        self.media_name = StringFiled(null=False, name='media_name')
        self.media_url = StringFiled(name='media_url')
        self.media_location = ArrayFiled(name='media_location')
        self.board_id = StringFiled(name='board_id')
        self.board_name = StringFiled(name='board_name')
        self.board_url = StringFiled(name='board_url')
        self.board_name_full = ArrayFiled(name='board_name_full')
        self.url = StringFiled(null=False, name='url')
        self.reposts_count = IntFiled(name='reposts_count')
        self.likes_count = IntFiled(name='likes_count')
        self.dislikes_count = IntFiled(name='dislikes_count')
        self.views_count = IntFiled(name='views_count')
        self.comments_count = IntFiled(name='comments_count')
        self.attitudes_count = IntFiled(name='attitudes_count')
        self.favourites_count = IntFiled(name='favourites_count')
        self.quoted_count = IntFiled(name='quoted_count')
        self.viewing_count = IntFiled(name='viewing_count')
        self.play_count = IntFiled(name='play_count')
        self.share_count = IntFiled(name='share_count')
        self.danmaku_count = IntFiled(name='danmaku_count')
        self.keywords = ArrayFiled(name='keywords')
        self.keywords_vector = ObjectArrayFiled(name='keywords_vector')
        self.persons_vector = ObjectArrayFiled(name='persons_vector')
        self.organizations_vector = ObjectArrayFiled(name='organizations_vector')
        self.regions_vector = ObjectArrayFiled(name='regions_vector')
        self.message_type = IntFiled(1, null=False, name='message_type')
        self.mention_list = ArrayFiled(name='mention_list')
        self.topic_list = ArrayFiled(name='topic_list')
        self.post_location = ArrayFiled(name='post_location')
        self.post_location_geo = ArrayFiled(name='post_location_geo')
        self.root_id = StringFiled(name='root_id')
        self.parent_id = StringFiled(name='parent_id')
        self.retweeted_status = ObjectFiled(name='retweeted_status')
        self.quoted_status = ObjectFiled(name='quoted_status')
        self.sentiment = IntFiled(0, null=False, name='sentiment')
        self.similar_id = StringFiled(name='similar_id')
        self.is_public = IntFiled(1, null=False, name='is_public')
        self.author_id = StringFiled(name='author_id')
        self.author_name = StringFiled(name='author_name')
        self.author_screen_name = StringFiled(name='author_screen_name')
        self.author_full_info = ObjectFiled(name='author_full_info')
        self.group_id = StringFiled(name='group_id')
        self.group_name = StringFiled(name='group_name')
        self.extra_info = StringFiled(name='extra_info')

        self.now = IntFiled(int(time.time()), null=False)  # 非提交

    def end_check(self, d):
        del d['now']


class GolaxyNewsDataItem(_GolaxyDataItem):
    ITEM_TYPE = 'news'

    def check_id(self):
        if not self._key.value:
            self.check_key()
        if not self._ch.value:
            self.check_ch()
        ch = str(self._ch.value).rjust(2, '0')
        self._id._value = '%s%s' % (ch, self._key.value)

    def check_ch(self):
        if not self._ch.value:
            raise DataCheckException('The attribute _ch must have value!')

    def check_key(self):
        if not self.url.value:
            self.check_url()
        self._key._value = security.EncryptUtils.md5(self.url.value)

    def check_spec(self):
        if not self._spec.value:
            raise DataCheckException('The attribute _spec must have value!')

    def check_dcm(self):
        if not self._dcm.value:
            raise DataCheckException('The attribute _dcm must have value!')

    def check_url(self):
        if not self.url.value:
            raise DataCheckException('The attribute url must have value!')

    def check_update_time(self):

        if not self.update_time.value:
            self.update_time._value = mix.DateTimeUtils.unify_time_stamp(time_data=self.now.value)
            self.gather_time._value = self.update_time.value
            self.insert_time._value = self.update_time.value

    def check_publish_time(self):
        if not self.publish_time.value:
            self.publish_time._value = self.update_time.value

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


class GolaxyAppNewsDataItem(GolaxyNewsDataItem):
    ITEM_TYPE = 'app_news'


class GolaxyAppNewsCommentsDataItem(_GolaxyDataItem):
    ITEM_TYPE = 'app_news_comments'


class GolaxyWenDaDataItem(_GolaxyDataItem):
    ITEM_TYPE = 'wenda'


class GolaxyZhiKuDataItem(GolaxyNewsDataItem):
    ITEM_TYPE = 'zhiku'


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
