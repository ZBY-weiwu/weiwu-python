# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/9

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
    def unify_time_stamp(cls, time_data, width=13):
        """
        统一时间戳
        :param time_data: 时间数据
        :param width: 显示长度
        :return:
        """
        if isinstance(time_data, float):
            time_data = int(time_data)
        elif isinstance(time_data, datetime.datetime):
            time_data = int(time_data.timestamp())
        if isinstance(time_data, int):
            time_data = str(time_data)
        time_stamp_length = len(time_data)
        difference_length = time_stamp_length - width
        if difference_length > 0:
            time_data = time_data[:width]
        elif difference_length < 0:
            time_data = '%s%s' % (time_data, '0' * (-difference_length))
        return int(time_data)

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
    def parse_text_datetime(cls, text, stamp=True, width=13, parse_type=None, fmt=None, **kwargs):
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
                return cls.unify_time_stamp(result, width)
            except OSError:
                return None
        return result

    @classmethod
    def parse_datetime_by_fmts(cls):
        """
        标准时间格式
        """
