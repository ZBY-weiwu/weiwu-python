# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/9

import time
import datetime

# import dateparser

from core.origin.parser import regexdatetime

DATETIME_FMTS = [
    ''
]


class DateTimeUtils(object):
    """
        时间处理工具
        """

    @classmethod
    def unify_time_stamp(cls, time_data, unit='ms'):
        """
        统一时间戳
        :param time_data: 时间数据
        :param unit: 单位
        :return:
        """
        if not time_data:
            return time_data
        if isinstance(time_data, float):
            time_data = int(time_data)
        elif isinstance(time_data, datetime.datetime):
            time_data = int(time_data.timestamp())
        if unit == 'ms':
            time_stamp_length = len(str(time_data))
            if time_stamp_length <= 10:
                return time_data * 1000
            return time_data
        elif unit == 's':
            return time_data

    @classmethod
    def compare(cls, dt1, dt2):
        dt1 = cls.to_datetime(dt1)
        dt2 = cls.to_datetime(dt2)
        if dt1 > dt2:
            return 1
        elif dt1 == dt2:
            return 0
        else:
            return -1

    @classmethod
    def to_datetime(cls, dt):
        if isinstance(dt, datetime.datetime):
            return dt

    @classmethod
    def parse_text_datetime(cls, text, stamp=True, unit='ms', parse_type=None, fmt=None, **kwargs):
        # result = dateparser.parser(text)  # 速度很慢
        # if result:
        #     return result
        result = None
        if fmt and text:
            try:
                result = datetime.datetime.strptime(text, fmt)
            except ValueError:
                pass
        if not result:
            if parse_type == 'publish':
                result = regexdatetime.TextPublishDateTimeRegexParser.parse(text, **kwargs)
            else:
                result = regexdatetime.TextDateTimeRegexParser.parse(text, **kwargs)
        if stamp:
            try:
                return cls.unify_time_stamp(result, unit)
            except OSError:
                return None
        return result

    @classmethod
    def str2stamp(cls, text, fmt):
        return int(time.mktime(time.strptime(text, fmt)))
