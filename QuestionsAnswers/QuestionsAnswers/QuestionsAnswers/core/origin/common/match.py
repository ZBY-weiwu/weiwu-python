# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/12


import re


class RegexUtils(object):
    """
        正则相关工具类
        """

    @classmethod
    def three_stage_match(cls, text, regex):
        """
        三段式匹配
        :param text: 文本
        :param regex: 带有三个()的表达式，取中间
        :return:
        """
        results = re.findall(regex, text, re.S)
        if results:
            result = results[0]
            return result[1].strip()


class RegexHandler(object):
    def __init__(self, text):
        self.text = text

    def handle(self, regex):
        if isinstance(regex, list) and len(regex) == 2:
            _regex, new = regex
            self.text = re.sub(_regex, new, self.text, re.S)
        else:
            self.text = ''.join(re.findall(regex, self.text, re.S))
        return self


# xpath表达式获取数据部分
XPATH_PATTERN_SUFFIX = {
    '//text()': './/text()',
    '/text()': './text()',
    '//@': './/@',
    '/@': './@',
}


class XpathUtils(object):

    @classmethod
    def spilt_pattern(cls, pattern):
        """
        分割xpath表达式，按|分隔
        :param pattern: xpath表达式
        :return: [(//h1/text(), //h1, ./text()), (//h1/@href, //h1, ./@href)]
        """
        if not pattern:
            return None
        pattern_list = list()
        pattern_split = pattern.split('|')
        for _pattern in pattern_split:
            base_pattern = _pattern
            left_pattern = base_pattern
            right_pattern = './/text()'
            for k, v in XPATH_PATTERN_SUFFIX.items():
                if k in base_pattern:
                    _pattern_split = base_pattern.split(k)
                    left_pattern = _pattern_split[0]
                    right_pattern = '%s%s' % (v, _pattern_split[1])
                    break
            pattern_list.append((base_pattern, left_pattern, right_pattern))
        return pattern_list

    @classmethod
    def get_element_pattern(cls, pattern):
        """
        获取xpath表达式的标签定位表达式部分
        :param pattern: xpath表达式
        :return:
        """
        return cls.spilt_pattern(pattern)[0][1]
