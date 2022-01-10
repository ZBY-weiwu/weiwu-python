#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/3/23
import random
import re
import time
import datetime

from core.origin.config import datetime_conf
from core.origin.common import mix


class TextDateTimeLangAdapter(object):
    """
    文本时间语言适配器
    """

    @classmethod
    def adapt(cls, text, lang=None):
        """
        语言适配
        :param text:
        :param lang:
        :return:
        """
        if lang:
            return getattr(cls, 'adapt_%s' % lang)(text)
        return text

    @classmethod
    def adapt_en(cls, text):
        """
        英文适配器
        :param text:
        :return:
        """
        for i, j in datetime_conf.EN_MONTH:
            text = text.replace(i, j)
        for i, j in datetime_conf.EN_QUARTER:
            text = text.replace(i, j)
        return text


class TextDateTimeRegexParser(object):
    """
    文本时间正则解析
    """

    @classmethod
    def parse(cls, text, regex=None, lang=None, default=None, parser=None):
        """
        时间解析
        :param text:
        :param regex:
        :param lang:
        :param default:
        :param parser: 解析器
        :return:
        """
        text = text.strip()
        now = datetime.datetime.today()
        if not default:
            default = now
        if parser:
            result = cls.parse_by_parser(text, parser, now)
            if not result:
                return default
            return result
        text = TextDateTimeLangAdapter.adapt(text, lang)
        if regex:
            if not isinstance(regex, list):
                regex = [regex, ]
            result = cls.match_and_parse(text, regex, now)
            if result:
                return result
        if lang:
            re_rules_name = '%s_DATE_RE_RULES' % lang.upper()
            if hasattr(datetime_conf, re_rules_name):
                regex = getattr(datetime_conf, re_rules_name)
            result = cls.match_and_parse(text, regex, now)
            if result:
                return result
        result = cls.match_and_parse(text, datetime_conf.BASE_DATE_RE_RULES, now)
        if not result:
            return default
        return result

    @classmethod
    def parse_by_parser(cls, text, parser, base):
        """
        解析器解析
        :param text:
        :param parser:
        :param base:
        :return:
        """
        if parser == 'zh_semantics':
            return cls.parse_datetime_by_zh_semantics(text, base)

    @classmethod
    def parse_datetime_by_zh_semantics(cls, text, base):
        """
        通过中文语义解析
        :param text:
        :param base:
        :return:
        """
        regex = datetime_conf.ZH_SEMANTICS_DATETIME_RE_RULES
        return cls.match_and_parse(text, regex, base)

    @classmethod
    def match_and_parse(cls, text, regex, base):
        for _regex in regex:
            match_obj = None
            try:
                match_obj = re.search(_regex, text, flags=re.M | re.I | re.S)
            except Exception as e:
                print('The regex rule error, The regex rule is: %s' % _regex, 'reason is %s' % e)
            if match_obj:
                try:
                    result = cls._parse(match_obj.groupdict(), base)
                    return result
                except Exception as e:
                    print('warning', 'The regex rule is: %s' % _regex, 'reason is %s' % e)

    @classmethod
    def _parse(cls, match_group_dict, base):
        year = cls._get_value_from_group_dict(match_group_dict, 'year', base.year)
        if isinstance(year, str) and len(year) == 2:
            year = '20' + year
        year = int(year)
        month = int(cls._get_value_from_group_dict(match_group_dict, 'month', base.month))
        day = int(cls._get_value_from_group_dict(match_group_dict, 'day', base.day))
        hour = int(cls._get_value_from_group_dict(match_group_dict, 'hour', base.hour))
        minute = int(cls._get_value_from_group_dict(match_group_dict, 'minute', base.minute))
        second = int(cls._get_value_from_group_dict(match_group_dict, 'second', base.second))
        timestamp = cls._get_value_from_group_dict(match_group_dict, 'timestamp', 0)
        if timestamp:
            timestamp = mix.DateTimeUtils.unify_time_stamp(timestamp, 10)
            if timestamp > int(time.time()):
                timestamp = 0

        # 抽取到的具有变化含义的时间
        change_day = 0
        change_hour = 0
        change_minute = 0
        change_second = 0

        change_before = dict()
        change_before['change_year_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_year_before', 0))
        change_before['change_month_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_month_before', 0))
        change_before['change_week_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_week_before', 0))
        change_before['change_day_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_day_before', 0))
        change_before['change_hour_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_hour_before', 0))
        change_before['change_minute_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_minute_before', 0))
        change_before['change_second_before'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_second_before', 0))
        for key in change_before:
            if change_before[key] > 0:
                change_before[key] += round(random.random(), 1)

        change_within = dict()
        change_within['change_year_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_year_within', 0))
        change_within['change_month_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_month_within', 0))
        change_within['change_week_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_week_within', 0))
        change_within['change_day_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_day_within', 0))
        change_within['change_hour_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_hour_within', 0))
        change_within['change_minute_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_minute_within', 0))
        change_within['change_second_within'] = float(cls._get_value_from_group_dict(match_group_dict, 'change_second_within', 0))
        for key in change_within:
            if change_within[key] > 0:
                change_within[key] -= round(random.random(), 1)

        if change_before['change_year_before'] > 0:
            change_day += change_before['change_year_before'] * 365
        if change_before['change_month_before'] > 0:
            change_day += change_before['change_month_before'] * 30
        if change_before['change_week_before'] > 0:
            change_day += change_before['change_week_before'] * 7
        if change_before['change_day_before'] > 0:
            change_day += change_before['change_day_before']
        if change_before['change_hour_before'] > 0:
            change_hour += change_before['change_hour_before']
        if change_before['change_minute_before'] > 0:
            change_minute += change_before['change_minute_before']
        if change_before['change_second_before'] > 0:
            change_second += change_before['change_second_before']

        if change_within['change_year_within'] > 0:
            change_day += change_within['change_year_within'] * 365
        if change_within['change_month_within'] > 0:
            change_day += change_within['change_month_within'] * 30
        if change_within['change_week_within'] > 0:
            change_day += change_within['change_week_within'] * 7
        if change_within['change_day_within'] > 0:
            change_day += change_within['change_day_within']
        if change_within['change_hour_within'] > 0:
            change_hour += change_within['change_hour_within']
        if change_within['change_minute_within'] > 0:
            change_minute += change_within['change_minute_within']
        if change_within['change_second_within'] > 0:
            change_second += change_within['change_second_within']

        # 抽取到具有特殊含义的时间
        special_day = cls._get_value_from_group_dict(match_group_dict, 'special_day', "")
        special_more = cls._get_value_from_group_dict(match_group_dict, 'special_more', "")
        if special_day:
            if special_day == "今天":
                change_day += 0
            elif special_day == "昨天":
                change_day += 1
            elif special_day == "前天":
                change_day += 2
        if special_more:
            if special_more == '刚刚':
                change_second += 10

        try:  # 时间计算
            change_date = datetime.timedelta(days=change_day, hours=change_hour,
                                             minutes=change_minute, seconds=change_second)
            if timestamp:
                before_time = datetime.datetime.fromtimestamp(timestamp)
            else:
                before_time = base.replace(year=year, month=month, day=day, hour=hour,
                                           minute=minute, second=second)
            last_datetime = before_time - change_date
            if last_datetime > base:  # 不能大于当前时间
                return
            return last_datetime
        except Exception as e:
            print('parser time error: ', e)

    @classmethod
    def _get_value_from_group_dict(cls, group_dict, key, default):
        value = group_dict.get(key, default)
        if not value:
            value = default
        return value


class TextPublishDateTimeRegexParser(TextDateTimeRegexParser):
    @classmethod
    def parse(cls, text, regex=None, lang=None, default=None):
        if not regex:
            regex = datetime_conf.PUBLISH_DATE_RE_RULES
        return super().parse(text, regex, lang, default)


if __name__ == '__main__':
    pass
    """
    2021-02-25
    昨天 21:14
    """
