#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/14


class DetailURL(object):
    def __init__(self, **kwargs):
        self.detail_url_id = None
        self.detail_url = None
        self.visit_url = None
        self.title = None
        self.publish_time = None
        self.__dict__.update(**kwargs)

    def confirm(self):
        if not self.visit_url:
            self.visit_url = self.detail_url

    @property
    def url(self):
        self.confirm()
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]
