# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/14
import json


class RequestMeta(object):
    def __init__(self, **kwargs):
        self.request_kwargs = None  # 请求参数
        self.__dict__.update(**kwargs)

    @property
    def meta(self):
        return self.__dict__

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]


class ScrapyRequestMeta(RequestMeta):
    pass


class RequestKwargs(object):
    def __init__(self, **kwargs):
        self.method = None
        self.headers = {}
        self.__dict__.update(**kwargs)

    @property
    def kwargs(self):
        return {key: value for key, value in self.__dict__.items() if value is not None}

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]


class ScrapyRequestKwargs(RequestKwargs):
    def __init__(self, **kwargs):
        self.callback = None
        self.body = None
        self.cookies = None
        self.encoding = None
        self.priority = None
        self.dont_filter = None
        self.errback = None
        self.flags = None
        self.cb_kwargs = None
        super(ScrapyRequestKwargs, self).__init__(**kwargs)


class RequestConfig(object):
    def __init__(self, url, method='GET', params=None, headers_template=None, headers=None,
                 data_template=None, data=None, url_type=None):
        self.url = url
        self.method = method
        self.params = params
        self.headers_template = headers_template
        self.headers = headers
        self.data_template = data_template
        self.data = data
        self.url_type = url_type

    @property
    def config(self):
        return self.__dict__

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, item):
        return self.__dict__[item]


class RequestConfigUtils(object):
    @classmethod
    def parse_request_config(cls, config, params=None, headers_template=None,
                             headers=None, data_template=None, data=None):
        """
            解析app请求参数配置
            :param config: 配置信息
            :param params:url参数，如果为一个不为空的列表，则和config中的url进行拼接，其他不做处理。
            :param headers_template:json字符串模板
            :param headers:字典或列表，字典则直接使用，列表则和headers_template进行拼接。
            :param data_template:字符串模板
            :param data:如果为一个不为空的列表，和data_template拼接，其他不做处理。
            :return:
            """
        url = config['url']
        params = params or config['params']
        if params and isinstance(params, list):
            url = url % tuple(params)
        headers_template = headers_template or config['headers_template']
        headers = headers or config['headers']
        if headers_template:
            headers = json.loads(headers_template % tuple(headers))
        data_template = data_template or config['data_template']
        data = data or config['data'] or None
        if data_template:
            data = data_template % tuple(data)
        method = config['method'] or 'GET'
        method = method.upper()
        return {
            'url': url,
            'method': method,
            'headers': headers,
            'data': data
        }


class RequestKwargsUtils(object):
    @classmethod
    def update_headers(cls, old_headers, new_headers):
        old_keys = [key.lower() for key in old_headers]
        for key in new_headers:
            if key.lower() not in old_keys:
                old_headers[key] = new_headers[key]
