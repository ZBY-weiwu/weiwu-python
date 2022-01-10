#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/14


class DetailURL(object):
    """
    详情页类
    """
    def __init__(self,
                 detail_url_id=None,
                 detail_url=None,
                 visit_url=None,
                 duplicate_url=None,
                 detail_assist_info=None,
                 data=None):
        self.detail_url_id = detail_url_id  # 详情页url id
        self.detail_url = detail_url  # 详情页url
        self.visit_url = visit_url  # 详情页访问接口/url
        self.duplicate_url = duplicate_url  # 去重url
        if detail_assist_info is None:  # 详情页辅助信息
            detail_assist_info = {}
        self.detail_assist_info = detail_assist_info  # 附加信息，如title,publish_time等
        self.data = data  # 详情页访问接口post请求时的data信息

    def confirm(self):
        if not self.visit_url:
            self.visit_url = self.detail_url
        if not self.duplicate_url:
            self.duplicate_url = self.detail_url

    @property
    def url(self):
        self.confirm()
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]
