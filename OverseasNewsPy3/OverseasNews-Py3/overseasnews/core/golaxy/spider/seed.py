#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/18
import random
import time


class GolaxyBaseSeed(object):
    """
    基础种子类
    """

    def __init__(self, **kwargs):
        self.dynamic_load_type = 0  # 动态加载类型，0不启用，1国内splash动态加载，2国内selenium动态加载，3国外splash,4国外其他自定义
        self.proxy_type = 0  # 代理类型，0不启用，1随机选择，其他自定义
        self.crawl_time = int(time.time()) * 1000  # 采集时间
        self.spider_id = ''  # spider标识id
        self.lang = ''  # 语言
        self.user_agent_type = 0  # ua类型，0默认pc端ua，1默认手机端ua，2随机pc端ua，3随机手机ua, -1请求库默认ua
        self.request_kwargs = {}  # 请求参数
        # 请求参数有：
        #     headers
        #     cookies
        self.resources = dict()
        self.__dict__.update(**kwargs)

    @property
    def seed(self):
        # return self.__dict__
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]


class GolaxyBoardSeed(GolaxyBaseSeed):
    """
    板块种子类
    """

    def __init__(self, **kwargs):
        self.detail_proxy_type = 0
        self.detail_dynamic_load_type = 0
        self.board_parse_rule = None  # 板块页解析规则
        self.detail_assist_parse_rule = None  # 板块页辅助解析到详情页规则
        self.detail_parse_rule = None  # 详情页解析规则
        super(GolaxyBoardSeed, self).__init__(**kwargs)

    @property
    def board_info(self):
        info = {}
        for key in self.__dict__:
            if key not in ('dynamic_load_type', 'proxy_type', 'crawl_time', 'spider_id',
                           'board_parse_rule', 'detail_parse_rule', 'detail_proxy_type',
                           'detail_dynamic_load_type'):
                info[key] = self.__dict__[key]
        return info


class GolaxyDetailSeed(GolaxyBaseSeed):
    """
    详情页种子类
    """

    def __init__(self, **kwargs):
        self.board_info = None  # 板块信息
        self.detail_parse_rule = None  # 详情页解析规则
        self.detail_url = None  # 详情页url
        self.has_duplicate = False  # 详情页是否去重
        super(GolaxyDetailSeed, self).__init__(**kwargs)


class GolaxyWemediaBoardSeed(GolaxyBoardSeed):
    """
    自媒体板块种子类
    """

    def __init__(self, **kwargs):
        self.wemedia_id = None  # 自媒体id
        self.wemedia_name = None  # 自媒体名称
        self.wemedia_board = None  # 自媒体板块（类别）
        self.user_id = None  # 用户id
        self.user_name = None  # 用户名
        self.meta = None  # 扩展信息
        super(GolaxyWemediaBoardSeed, self).__init__(**kwargs)


class GolaxyWemediaUserMonitorSeed(GolaxyBaseSeed):
    def __init__(self, **kwargs):
        self.wemedia_board = None
        self.user_id = None
        self.meta = None
        self.user = None
        super(GolaxyWemediaUserMonitorSeed, self).__init__(**kwargs)


class GolaxyWemediaDetailSeed(GolaxyDetailSeed):
    """
    自媒体详情页种子类
    """
    pass


class GolaxyWemediaUserSupplySeed(GolaxyBaseSeed):
    def __init__(self, **kwargs):
        self.visit_url = None
        super(GolaxyWemediaUserSupplySeed, self).__init__(**kwargs)


class GolaxyRecruitBoardSeed(GolaxyBoardSeed):
    """
    招聘信息板块种子类
    """

    def __init__(self, **kwargs):
        self.keyword = None  # 搜索关键字
        self.site_id = None  # 网站id
        self.site_name = None  # 网站名称
        self.a = None
        super(GolaxyRecruitBoardSeed, self).__init__(**kwargs)


class GolaxyRecruitDetailSeed(GolaxyDetailSeed):
    """
    招聘信息详情页种子类
    """
    pass


class GolaxyWebNewsBoardSeed(GolaxyBoardSeed):
    """
    网页新闻板块种子类
    """

    def __init__(self, **kwargs):
        self.entry_url = None  # 入口（板块）URL
        self.site_id = None  # 网站id
        self.site_name = None  # 网站名称
        self.board_id = None  # 板块id
        self.board_name = None  # 板块名称
        self.domain = None  # 域名
        self.location = None  # 地区
        super(GolaxyWebNewsBoardSeed, self).__init__(**kwargs)


class GolaxyWebNewsDetailSeed(GolaxyDetailSeed):
    """
    网页新闻详情页种子类
    """
    pass


class GolaxyZhiKuBoardSeed(GolaxyBoardSeed):
    """
    智库板块种子类
    """

    def __init__(self, **kwargs):
        self.entry_url = None
        self.site_id = None
        self.site_name = None
        self.site_url = None
        self.board_id = None
        self.board_name = None
        self.domain = None
        self.location = None
        super(GolaxyZhiKuBoardSeed, self).__init__(**kwargs)


class GolaxyAutoincrementDetailSeed(GolaxyDetailSeed):
    """
    自增采集种子类
    """

    def __init__(self, **kwargs):
        self.detail_url_id = None
        self.duplicate_channel = None
        super(GolaxyAutoincrementDetailSeed, self).__init__(**kwargs)


class GolaxyAutoincrementProbeSeed(GolaxyBaseSeed):
    def __init__(self, **kwargs):
        self.start = 0
        self.end = 0
        self.step = 1
        self.sub = 1000
        self.change = self.step * random.randint(16, 128)
        self.forward_fail_retry_count = 15
        self.meet_fail = False  # 中途是否遇到错误
        self.first_success = False  # 首次试探是否成功
        self.forward_fail_count = 0  # 连续试探错误次数
        self.cursor_is_valid = False  # 链接是否成功访问
        self.probe_interval = 10  # 最小探测时间间隔
        super(GolaxyAutoincrementProbeSeed, self).__init__(**kwargs)
        self.cursor = self.start + self.change
        self.forward_fail_smooth_retry_count = int(self.forward_fail_retry_count * 2 // 3)  # 连续试探错误平滑试探次数
