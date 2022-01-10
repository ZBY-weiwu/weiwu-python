#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/10

from requests import get, post

from core.origin.common import request as _request


class GolaxyScrapyBoardRequestMeta(_request.ScrapyRequestMeta):
    def __init__(self, **kwargs):
        self.board_seed = None  # 板块种子
        self.next_page_urls = []  # 翻页/列表页urls
        self.current_url = None  # 当前页
        self.current_url_in_next_page_urls_index = 0  # 当前页在列表页中的下标
        super(GolaxyScrapyBoardRequestMeta, self).__init__(**kwargs)


class GolaxyScrapyDetailRequestMeta(_request.ScrapyRequestMeta):
    def __init__(self, **kwargs):
        self.detail_seed = None
        super(GolaxyScrapyDetailRequestMeta, self).__init__(**kwargs)


class GolaxyScrapyBoardRequestKwargs(_request.ScrapyRequestKwargs):
    pass


class GolaxyScrapyDetailRequestKwargs(_request.ScrapyRequestKwargs):
    pass


class GolaxyRequestsRequester(object):
    """
    Requests库请求器
    """
    @classmethod
    def request(cls, **kwargs):
        """
        默认请求方法
        """
        method = kwargs.pop('method', 'GET').upper()
        if not kwargs.get('timeout', None):
            kwargs['timeout'] = 60
        if method == 'GET':
            return get(**kwargs)
        elif method == 'POST':
            return post(**kwargs)

    @classmethod
    def retry_request(cls, retry=1, **kwargs):
        """
        重试请求
        :param retry: 重试次数
        :return:
        """
        has_retry = 0
        while has_retry <= retry:
            try:
                return cls.request(**kwargs)
            except Exception as e:
                has_retry += 1
