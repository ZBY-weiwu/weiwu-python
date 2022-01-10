# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/16


"""
算法相关工具库
"""
import random

import requests

class ProbeSearcher(object):
    @classmethod
    def search(cls, start, step=1, sub=None, forward_fail_retry_count=15, **kwargs):
        """
        搜索试探
        :param start: 起点
        :param step: 步长
        :param sub: 试探出的终点和起点的最大差距
        :param forward_fail_retry_count: 从开始试探失败的重试次数
        :param kwargs:
        :return: (起点， 终点， 步长)
        """
        if not sub:
            sub = 1000 * step
        end = start
        change = step * random.randint(16, 128)
        cursor = start + change
        meet_fail = False  # 中途是否遇到错误
        first_success = False  # 首次试探是否成功
        forward_fail_count = 0  # 连续试探错误次数
        forward_fail_smooth_retry_count = int(forward_fail_retry_count * 2 // 3)  # 连续试探错误平滑试探次数
        while True:
            if change // step < 1 or end < start:
                break
            _cursor_is_valid = cls.cursor_is_valid(cursor, **kwargs)
            if _cursor_is_valid and not meet_fail:  # 从未发生试探失败
                end = cursor
                change *= 2 * step
                cursor += change
                if not first_success:
                    first_success = True
            elif not first_success:  # 首次试探失败后操作
                if _cursor_is_valid:
                    return start, cursor, step
                else:
                    if forward_fail_count < forward_fail_smooth_retry_count:
                        change = int(change * 1.1) * step
                        cursor = random.randint(end, end + change)
                    else:
                        change *= 2 * step
                        cursor = random.randint(end, end + change)
                    forward_fail_count += 1
                    if forward_fail_count > forward_fail_retry_count:
                        return start, end, step
            elif meet_fail:  # 中途出现试探失败
                change //= 2 * step
                if _cursor_is_valid:
                    end = cursor
                    cursor += change
                else:
                    cursor -= change
            else:  # 首次出现试探失败
                meet_fail = True
                first_success = False
                change //= 2 * step
                cursor -= change
        if sub:
            if end - start > sub:
                end = start + sub
        return start, end, step

    @classmethod
    def cursor_is_valid(cls, cursor, *args, **kwargs):
        """
        指针试探是否成功
        :param cursor: 指针
        :param args:
        :param kwargs:
        :return:
        """
        raise NotImplemented


class WebLinkProbeSearcher(ProbeSearcher):
    SEARCH_URL_MODE = ''
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    @classmethod
    def cursor_is_valid(cls, cursor, **kwargs):
        url = cls.handle_url(cls.SEARCH_URL_MODE, cursor)
        try:
            response = requests.get(url, headers=cls.HEADERS, timeout=30)
        except Exception as e:
            return False
        if response.status_code >= 400:
            return False
        return cls.response_is_valid(response)

    @classmethod
    def handle_url(cls, url_mode, cursor):
        """
        构建请求url
        :param url_mode: url模板
        :param cursor:
        :return:
        """
        return url_mode % cursor

    @classmethod
    def response_is_valid(cls, response):
        """
        请求响应内容判断试探是否成功
        :param response:
        :return:
        """
        return True
