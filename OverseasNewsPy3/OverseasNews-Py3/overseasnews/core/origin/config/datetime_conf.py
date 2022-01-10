#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/3/23

BASE_DATE_RE_RULES = [
    # 精准策略
    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*$",
    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?\s*(?P<hour>\d{1,2})$",
    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?\s*(?P<hour>\d{1,2})\s*[:时]\s*(?P<minute>\d{1,2})\s*$",

    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?\s*T?(?P<hour>\d{1,2})\s*[:时]\s*(?P<minute>\d{1,2})\s*[:分]\s*(?P<second>\d{1,2})\s*[秒]?",
    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?\s*(?P<hour>\d{1,2})\s*[:时]\s*(?P<minute>\d{1,2})\s*[分]?",
    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?\s*(?P<hour>\d{1,2})\s*[时]?",
    "(?P<year>\d{4})\s*[-|/.年]\s*m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?",
    "m?(?P<month>\d{1,2})m?\s*[-|/.月]\s*(?P<day>\d{1,2})\s*[日]?",

    ""

    # 模糊策略
    "(?P<change_day_before>\d+)\s*天前",
    "(?P<change_minute_before>\d+)\s*分钟前",
    "(?P<change_hour_before>\d+)\s*小时前",
    "(?P<change_week_before>\d+)\s*周前",
    "(?P<change_month_before>\d+)\s*(个)?月前",
    "(?P<change_year_before>\d+)\s*年前",
    "(?P<change_second_before>\d+)\s*秒前",

    "(?P<change_day_within>\d+)\s*天内",
    "(?P<change_minute_within>\d+)\s*分钟内",
    "(?P<change_hour_within>\d+)\s*小时内",
    "(?P<change_week_within>\d+)\s*周内",
    "(?P<change_month_within>\d+)\s*(个)?月内",
    "(?P<change_year_within>\d+)\s*年内",
    "(?P<change_second_within>\d+)\s*秒内",

    "(?P<special_day>今天)\s*(?P<hour>\d+):(?P<minute>\d+)",
    "(?P<special_day>今天)",
    "(?P<special_day>昨天)\s*(?P<hour>\d+):(?P<minute>\d+)",
    "(?P<special_day>昨天)",
    "(?P<special_day>前天)\s*(?P<hour>\d+):(?P<minute>\d+)",
    "(?P<special_day>前天)",
    "(?P<special_more>刚刚)",

    # 特殊策略
    "(?P<month>\d{1,2})\s*月?\s*\.\s*(?P<day>\d{1,2})\s*日?\s*/(?P<year>\d{4})\s*年?",
    "(?P<day>\d{1,2})\s*\.\s*(?P<month>\d{1,2})\s*日?\s*/(?P<year>\d{4})\s*年?"
]

EN_DATE_RE_RULES = [
    "m(?P<month>\d{1,2})m\s*(?P<day>\d{1,2})\s*,\s*(?P<year>\d{4})",  # 10 25, 2021
    "(?P<day>\d{1,2})\s*m(?P<month>\d{1,2})m\s*(?P<year>\d{4})",  # 25 10 2021
    "m(?P<month>\d{1,2})m\s*(?P<year>\d{4})",  # 10 2021
]

# 中文语义正则规则
ZH_SEMANTICS_DATETIME_RE_RULES = [
    "(?P<change_day_before>\d+)\s*天前",
    "(?P<change_minute_before>\d+)\s*分钟前",
    "(?P<change_hour_before>\d+)\s*小时前",
    "(?P<change_week_before>\d+)\s*周前",
    "(?P<change_month_before>\d+)\s*(个)?月前",
    "(?P<change_year_before>\d+)\s*年前",
    "(?P<change_second_before>\d+)\s*秒前",

    "(?P<change_day_within>\d+)\s*天内",
    "(?P<change_minute_within>\d+)\s*分钟内",
    "(?P<change_hour_within>\d+)\s*小时内",
    "(?P<change_week_within>\d+)\s*周内",
    "(?P<change_month_within>\d+)\s*(个)?月内",
    "(?P<change_year_within>\d+)\s*年内",
    "(?P<change_second_within>\d+)\s*秒内",

    "(?P<special_day>今天)\s*(?P<hour>\d+):(?P<minute>\d+)",
    "(?P<special_day>今天)",
    "(?P<special_day>昨天)\s*(?P<hour>\d+):(?P<minute>\d+)",
    "(?P<special_day>昨天)",
    "(?P<special_day>前天)\s*(?P<hour>\d+):(?P<minute>\d+)",
    "(?P<special_day>前天)",
    "(?P<special_more>刚刚)",
]

PUBLISH_DATE_RE_RULES = [
    "(发布日期：|日期：)\s*(?P<year>\d{4})年?[-|/.](?P<month>[0-1][1-9])月?[-|/.](?P<day>[0-3][0-9])日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})"
    # 发布日期/日期
]

# BASE_TIME_RE_RULES = [
#     # 精准策略
#     "((发布日期：)|(时间：)|(日期：)|(发布于)|(发表于))\s*(?P<year>\d{4})[-|/.](?P<month>\d{1,2})[-|/.](?P<day>\d{1,2})\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})",
#     "((发布日期：)|(时间：)|(日期：)|(发布于)|(发表于))\s*(?P<year>\d{4})[-|/.](?P<month>\d{1,2})[-|/.](?P<day>\d{1,2})\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})",
#     "((发布日期：)|(日期：)|(时间：)|(发布于)|(发表于))\s*(?P<year>\d{4})[-|/.](?P<month>\d{1,2})[-|/.](?P<day>\d{1,2})",
#     "发布日期：|发布时间：|发表于\s*(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?",
#     "发布日期：|发布时间：|发表于\s*(?P<name_day>今天)\s*(?P<hour>\d+):(?P<minute>\d+)",
#     "发布日期：|发布时间：|发表于\s*(?P<name_day>昨天)\s*(?P<hour>\d+):(?P<minute>\d+)",
#     "发布日期：|发布时间：|发表于\s*(?P<name_day>前天)\s*(?P<hour>\d+):(?P<minute>\d+)",
#     "[(发布日期：)(发布时间：)(发表于)]?\s*(?P<change_year>\d+)( )?\s*年前",
#     "[(发布日期：)(发布时间：)(发表于)]?\s*(?P<change_month>\d+)( )?\s*(个)?月前",
#     "[(发布日期：)(发布时间：)(发表于)]?\s*(?P<change_day>\d+)( )?\s*天前",
#     "[(发布日期：)(发布时间：)(发表于)]?\s*(?P<change_hour>\d+)( )?\s*小时前",
#     "[(发布日期：)(发布时间：)(发表于)]?\s*(?P<change_minute>\d+)( )?\s*分钟前",
#     "[(发布日期：)(发布时间：)(发表于)]?\s*(?P<change_second>\d+)( )?\s*秒前",
#     "((Mon|Tue|Wen|Thu|Fri|Sat|Sun) (Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sept|Oct|Nov|Dec) \d{1,2} \d{2}:\d{2}:\d{2} \d{4})",
#     "(?P<year>\d{4})年?[-|/.](?P<month>\d{1,2})月?[-|/.](?P<day>\d{1,2})日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})",
#     "(?P<year>\d{4})年?[-|/.](?P<month>\d{1,2})月?[-|/.](?P<day>\d{1,2})日?",
#     "(?P<month>\d{1,2})月?[-|/.](?P<day>\d{1,2})日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})",
#     "(?P<year>\d{2})年?[-|/.](?P<month>\d{2})月?[-|/.](?P<day>\d{2})日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})",
#     "(?P<year>\d{2})年?[-|/.](?P<month>\d{2})月?[-|/.](?P<day>\d{2})日?",
#     "(?P<year>\d{4})年?[-|/.](?P<month>\d{1,2})月?[-|/.](?P<day>\d{1,2})日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2}):(?P<second>\d{1,2})",
#     "(?P<year>\d{4})年?[-|/.](?P<month>\d{1,2})月?[-|/.](?P<day>\d{1,2})日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})",
#     "(?P<month>\d{1,2})月?[-|/.](?P<day>\d{1,2})日?\s*(?P<hour>\d{1,2}):(?P<minute>\d{1,2})",
#
#     # 模糊策略
#     "(?P<name_day>今天)\s*(?P<hour>\d+):(?P<minute>\d+)",
#     "(?P<name_day>今天)",
#     "(?P<name_day>昨天)\s*(?P<hour>\d+):(?P<minute>\d+)",
#     "(?P<name_day>昨天)",
#     "(?P<name_day>前天)\s*(?P<hour>\d+):(?P<minute>\d+)",
#     "(?P<name_day>前天)",
#     "(?P<name_other>刚刚)",
#     "(\d{2}):(\d{2})",
#
#     # 待考证
#     "(?P<year>\d{4})[-|/|.](?P<month>\d{1,2})[-|/|.](?P<day>\d{1,2})\s*?(?P<hour>[0-1]?[0-9]):(?P<minute>[0-5]?[0-9]):(?P<second>[0-5]?[0-9])",
#     "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
#     "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
#     "(\d{4}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
#     "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[0-1]?[0-9]:[0-5]?[0-9])",
#     "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[2][0-3]:[0-5]?[0-9])",
#     "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2}\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
#     "(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{4}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
#     "(\d{4}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
#     "(\d{4}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
#     "(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{2}年\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
#     "(\d{2}年\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
#     "(\d{2}年\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
#     "(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9]:[0-5]?[0-9])",
#     "(\d{1,2}月\d{1,2}日\s*?[0-1]?[0-9]:[0-5]?[0-9])",
#     "(\d{1,2}月\d{1,2}日\s*?[2][0-3]:[0-5]?[0-9])",
#     "(\d{1,2}月\d{1,2}日\s*?[1-24]\d时[0-60]\d分)([1-24]\d时)",
#     "(?P<year>\d{4})[-|/|.](?P<month>\d{1,2})[-|/|.](?P<day>\d{1,2})",
#     "(\d{2}[-|/|.]\d{1,2}[-|/|.]\d{1,2})",
#
#
#     # 特殊策略
#     "(?P<month>\d{1,2})月[(\s*)](?P<day>\d{1,2})[,]\s*(?P<year>\d{2,4})",  # 三月 10, 2019 | Aug 30, 2020
#     "(?P<timestamp>\d{10,13})",
#     "(?P<month>\d{1,2})[,(\s*)]*(?P<day>\d{1,2})[,(\s*)]*(?P<year>\d{4})"  # Oct 12, 2020]
#     ]

WEB_PAGE_PUBLISH_DATETIME_META_XPATH = [  # 部分特别规范的新闻网站，可以直接从 HTML 的 meta 数据中获得发布时间
    '//meta[starts-with(@property, "rnews:datePublished")]/@content',
    '//meta[starts-with(@property, "article:published_time")]/@content',
    '//meta[starts-with(@property, "og:article:published_time")]/@content',
    '//meta[starts-with(@property, "og:published_time")]/@content',
    '//meta[starts-with(@property, "og:release_date")]/@content',
    '//meta[starts-with(@itemprop, "datePublished")]/@content',
    '//meta[starts-with(@itemprop, "dateUpdate")]/@content',
    '//meta[starts-with(@name, "OriginalPublicationDate")]/@content',
    '//meta[starts-with(@name, "article_date_original")]/@content',
    '//meta[starts-with(@name, "og:time")]/@content',
    '//meta[starts-with(@name, "apub:time")]/@content',
    '//meta[starts-with(@name, "publication_date")]/@content',
    '//meta[starts-with(@name, "sailthru.date")]/@content',
    '//meta[starts-with(@name, "PublishDate")]/@content',
    '//meta[starts-with(@name, "publishdate")]/@content',
    '//meta[starts-with(@name, "PubDate")]/@content',
    '//meta[starts-with(@name, "pubtime")]/@content',
    '//meta[starts-with(@name, "_pubtime")]/@content',
    '//meta[starts-with(@name, "weibo: article:create_at")]/@content',
    '//meta[starts-with(@pubdate, "pubdate")]/@content',
]

# 英文月份对应数字
EN_MONTH = [
    ("Jan", "m1m"),
    ("Feb", "m2m"),
    ("Mar", "m3m"),
    ("Apr", "m4m"),
    ("May", "m5m"),
    ("Jun", "m6m"),
    ("Jul", "m7m"),
    ("Aug", "m8m"),
    ("Sept", "m9m"),
    ("Sep", "m9m"),
    ("Oct", "m10m"),
    ("Nov", "m11m"),
    ("Dec", "m12m"),
    ("January", "m1m"),
    ("February", "m2m"),
    ("March", "m3m"),
    ("April", "m4m"),
    ("May", "m5m"),
    ("June", "m6m"),
    ("July", "m7m"),
    ("August", "m8m"),
    ("September", "m9m"),
    ("October", "m10m"),
    ("November", "m11m"),
    ("December", "m12m"),
]

EN_QUARTER = [
    ('Spring', '2'),
    ('Summer', '5'),
    ('Autumn', '8'),
    ('Winter', '11')
]

# 中文月份对应数字
ZH_MONTH = [
    ("十一月", "m11m"),
    ("十二月", "m12m"),
    ("一月", "m1m"),
    ("二月", "m2m"),
    ("三月", "m3m"),
    ("四月", "m4m"),
    ("五月", "m5m"),
    ("六月", "m6m"),
    ("七月", "m7m"),
    ("八月", "m8m"),
    ("九月", "m9m"),
    ("十月", "m10m")
]
