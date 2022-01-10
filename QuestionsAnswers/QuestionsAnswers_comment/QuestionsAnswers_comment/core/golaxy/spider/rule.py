#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/20


class GolaxyRule(object):
    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    @property
    def rule(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]


class GolaxyBoardParseRule(GolaxyRule):
    def __init__(self, **kwargs):
        # 定位包含翻页链接和板块集中正文入口的区间，缩小范围，不指定则从全页匹配。
        self.section_xpath = None
        # 正文区域
        self.detail_section_xpath = None
        # 正文URL确认正则表达式，通过定位a标签获取链接后确认
        self.detail_url_confirm_regex = None
        # 正文URL抽取正则
        self.detail_url_match_regex = None
        # 正文URL抽取xpath
        self.detail_url_match_xpath = None
        # url无效参数过滤
        self.detail_url_query_filter = None
        # 是否允许重定向
        self.detail_url_redirect_enabled = False
        # 翻页模板  %拼接，用于已知最大页数的情况下，进行全量采集，配合page_size属性，并不启用去重。
        self.turn_page_format = None
        # 翻页区域
        self.turn_page_section_xpath = None
        # 翻页确认正则，最多采集前page_size页，在之前没有采集过的情况下。
        self.turn_page_confirm_regex = None
        # 翻页抽取正则
        self.turn_page_match_regex = None
        # 翻页抽取xpath
        self.turn_page_match_xpath = None
        # 最大页数
        self.max_page_count = 10
        # 爬取过去指定时间内数据（单位：毫秒）
        self.before_seconds = 86400000
        super(GolaxyBoardParseRule, self).__init__(**kwargs)


class GolaxyDetailParseRule(GolaxyRule):
    def __init__(self, **kwargs):
        # 标题获取xpath
        self.title_xpath = None
        # 正文获取xpath
        self.content_xpath = None
        # 发布时间获取xpath
        self.publish_time_xpath = None
        # 发布时间格式解析
        self.publish_time_format = None
        # 来源获取xpath
        self.source_xpath = None
        # 来源正则
        self.source_regex = None
        # 作者获取xpath
        self.author_xpath = None
        # 作者正则
        self.author_regex = None

        # self.title_xpath = None
        # self.title_match_regex = None
        # self.title_handle_regex = None
        # self.content_xpath = None
        # self.content_match_regex = None
        # self.content_handle_regex = None
        # self.content_type=None
        # self.publish_time_xpath = None
        # self.publish_time_lang = None
        # self.publish_time_match_regex = None
        # self.publish_time_format = None
        # self.publish_time_parse_regex = None
        # self.source_xpath = None
        # self.source_match_regex = None
        # self.source_handle_regex = None
        # self.author_xpath = None
        # self.author_match_regex = None
        # self.author_handle_regex = None

        super(GolaxyDetailParseRule, self).__init__(**kwargs)


class GolaxyWebNewsBoardParseRule(GolaxyBoardParseRule):
    pass


class GolaxyWebNewsDetailParseRule(GolaxyDetailParseRule):
    pass

class GolaxyWemediaBoardParseRule(GolaxyWebNewsBoardParseRule):
    pass


class GolaxyWemediaDetailParseRule(GolaxyWebNewsDetailParseRule):
    pass


class GolaxyZhiKuBoardParseRule(GolaxyBoardParseRule):
    pass


class GolaxyZhiKuDetailParseRule(GolaxyDetailParseRule):
    pass
