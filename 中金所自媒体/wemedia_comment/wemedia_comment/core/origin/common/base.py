# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/6/25
import re
import json
import random
import collections

import langid
from lxml.etree import Element


class Utils(object):
    """
    工具类，只提供类方法
    """
    pass


class Parser(object):
    """
    解析器，只提供类方法
    """
    pass


class Handler(object):
    """
    处理器，只提供实例方法
    """
    pass


class DictUtils(object):
    @classmethod
    def to_html(cls, d, tag):
        """
        字典数据转html
        :param d: 字典数据，建议为collections.OrderedDict有序字典，保证结果唯一
        :param tag: 顶级标签名
        :return:
        """
        if isinstance(d, str):
            d = json.loads(d, object_pairs_hook=collections.OrderedDict)
        ele = Element(tag)
        cls.__to_html(None, d, ele)
        return ele

    @classmethod
    def __to_html(cls, k, v, element):
        """
        字典数据转html
        :param k: 键
        :param v: 值
        :param element: Element对象
        :return:
        """

        if k:
            child = Element(k)
            element.append(child)
        else:
            child = element
        if isinstance(v, dict):
            for _k, _v in v.items():
                cls.__to_html(_k, _v, child)
        elif isinstance(v, (list, tuple)):
            for index in range(len(v)):
                cls.__to_html('li', v[index], child)
        else:
            child.text = str(v)
            element.append(child)


class StrUtils(object):
    pass


class TextUtils(StrUtils):
    @classmethod
    def add_tag(cls, text, tag=None, items=None, position='bottom', handle_func=None, *args, **kwargs):
        """
        添加标签
        :param text:
        :param tag:
        :param items:
        :param position:bottom or top
        :param handle_func:
        :param args:
        :param kwargs:
        :return:
        """
        if not tag or not items:
            return text
        item_count = len(items)
        if not handle_func:
            tag_text = ''
            for index in range(1, item_count + 1):
                tag_text = '%s%s' % (tag_text, tag % index)
            if position == 'top':
                return '%s%s' % (tag_text, text)
            return '%s%s' % (text, tag_text)
        return handle_func(text, tag, position, *args, **kwargs)

    @classmethod
    def recognise_lang(cls, text, simple_recognise=False):
        """
        识别文本语种
        :param text: 文本
        :param simple_recognise: 是否自定义简单快速识别，此结果支持的语种少，准确性不高。
        :return:
        """
        if simple_recognise:
            return cls.simple_recognise_lang(text)
        return langid.classify(text)[0]

    @classmethod
    def merge(cls, texts, merge_sep='', startswith='', endswith=''):
        """
        合并多个文本
        :param texts: 文本列表
        :param merge_sep: 合并符号
        :param startswith: 每段文本开始预留内容
        :param endswith: 每段文本结尾预留内容
        :return:
        """
        news_texts = list()
        if not startswith and not endswith:
            return merge_sep.join(texts)
        for text in texts:
            text = text.strip()
            text = '%s%s' % (startswith, text)
            text = '%s%s' % (text, endswith)
            news_texts.append(text)
        return merge_sep.join(news_texts)

    @classmethod
    def __simple_recognise_character_lang(cls, c):
        c_id = ord(c)
        if c_id > 40869:
            return None
        elif c_id > 19967:
            return 'zh'
        elif c_id > 122:
            return None
        elif c_id > 96:
            return 'en'
        elif c_id > 90:
            return None
        elif c_id > 64:
            return 'en'
        else:
            return None

    @classmethod
    def simple_recognise_lang(cls, text, default='zh'):
        if len(text) > 1500:
            text = random.sample(text, 1000)
        d = dict()
        for ch in text:
            lang = cls.__simple_recognise_character_lang(ch)
            if lang:
                if lang not in d:
                    d[lang] = 0
                d[lang] += 1
        if d:
            d = sorted(d.items(), key=lambda x: x[1], reverse=True)
            return d[0][0]
        else:
            return default

    @classmethod
    def count_word(cls, text, lang='zh'):
        if lang == 'en':
            return len(re.findall(r'\S+', text))

    @classmethod
    def split_text(cls, text, sep=None, regex=None):
        if sep:
            return text.split(sep)
        if regex:
            return re.findall(regex, text)
        return list(text)


class NumberUtils(object):
    @classmethod
    def int2str(cls, num, width=None, direction='l', fillchar='0'):
        num = str(num)
        if width is None:
            return num
        else:
            if direction == 'r':
                return num.rjust(width, fillchar)
            else:
                return num.ljust(width, fillchar)


class ListUtils(object):
    """
    列表相关工具
    """

    @classmethod
    def remove_none(cls, _list):
        return list(filter(None, _list))
