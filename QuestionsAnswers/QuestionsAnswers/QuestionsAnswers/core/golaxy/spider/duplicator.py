# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/14
import json

from core.golaxy.spider.requester import GolaxyRequestsRequester


class GolaxyDuplicatorUtils(object):
    """
    去重工具类
    """
    HEADERS = {'Accept': 'application/json', 'Content-Type': 'application/json'}
    DUPLICATE_SERVER_URL = 'http://10.20.18.100:8799/golaxy/wde/crawler/deduplication/v1'

    @classmethod
    def get_kwargs(cls, channel, expire, target, params='0', server_url=None):
        """
        获取去重服务请求参数
        :param channel:
        :param expire:
        :param target:
        :param params:
        :param server_url:
        :return:
        """
        kwargs = dict()
        kwargs['url'] = server_url or cls.DUPLICATE_SERVER_URL
        data = json.dumps({
            'channel': channel,
            'expire': expire,
            'target': target,
            'params': params
        })
        kwargs['data'] = data
        kwargs['headers'] = cls.HEADERS
        return kwargs

    @classmethod
    def get_find_and_set_kwargs(cls, **kwargs):
        """
        获取去重查找和设置请求参数
        """
        _kwargs = cls.get_kwargs(**kwargs)
        _kwargs['method'] = 'post'
        return _kwargs

    @classmethod
    def get_confirm_kwargs(cls, **kwargs):
        """
        获取去重确认请求参数
        """
        _kwargs = cls.get_kwargs(**kwargs)
        _kwargs['method'] = 'put'
        return _kwargs

    @classmethod
    def find_and_set_analysis(cls, response, default=False):
        if not response:
            return default
        data = json.loads(response.text)
        if data['code'] == 0:
            try:
                if data['message'] == 'SUCESS':
                    return data['targetExists']
                else:
                    return default
            except Exception:
                return default
        else:
            return default


class GolaxyRequestsDuplicator(object):
    """
    Requests库去重器
    """

    @classmethod
    def find_and_set(cls, retry=3, **kwargs):
        """
        去重查找和设置
        """
        _kwargs = GolaxyDuplicatorUtils.get_find_and_set_kwargs(**kwargs)
        response = GolaxyRequestsRequester.retry_request(retry, **_kwargs)
        return GolaxyDuplicatorUtils.find_and_set_analysis(response)

    @classmethod
    def confirm(cls, retry=3, **kwargs):
        """
        去重确认
        """
        _kwargs = GolaxyDuplicatorUtils.get_confirm_kwargs(**kwargs)
        response = GolaxyRequestsRequester.retry_request(retry, **_kwargs)
