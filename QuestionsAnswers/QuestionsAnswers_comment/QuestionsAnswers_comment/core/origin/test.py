#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/6
import re
from urllib.parse import urlparse


urls = [
    'http://www.bj.chinanews.com/news/2032/0430/81777.html',
    'https://www.bj.chinanews.com/ne/ws/2021/0430/81777.htm'
]


def urls_parse(urls, scheme='', allow_fragments=True):
    scheme_list = list()
    netloc_list = list()
    path_prefix_list = list()
    path_suffix_list = list()
    params_list = list()
    query_list = list()
    fragment_list = list()
    for url in urls:
        parse_result = urlparse(url, scheme, allow_fragments)
        scheme_list.append(parse_result.scheme)
        netloc_list.append(parse_result.netloc)
        path_split = parse_result.path.split('.')
        path_prefix_list.append(path_split[0])
        path_suffix_list.append('.%s' % path_split[1])
        params_list.append(parse_result.params)
        query_list.append(parse_result.query)
        fragment_list.append(parse_result.fragment)
    return {
        'scheme_list': scheme_list,
        'netloc_list': netloc_list,
        'path_prefix_list': path_prefix_list,
        'path_suffix_list': path_suffix_list,
        'params_list': params_list,
        'query_list': query_list,
        'fragment_list': fragment_list,
    }


def char_regex(char, escape=None):
    escape = escape or ['.', '?', '*']
    if char.isdigit():
        new_char = r'\d'
    elif char in escape:
        new_char = '%s%s' % ('\\', char)
    else:
        new_char = r'\w'
    return new_char


def str_regex(text):
    new_text = ''
    for char in text:
        new_text = '%s%s' % (new_text, char_regex(char))
    new_text = re.sub(r'(\\d){2,}', r'\\d+', new_text)
    new_text = re.sub(r'(\\w){2,}', r'\\w+', new_text)
    return new_text


def str_list_regex(str_list: list, same_regex=False, comm_regex=False):
    str_set = set(str_list)
    if len(str_set) == 1:
        text = str_set.pop()
        if not same_regex:
            return text
        else:
            return str_regex(text)
    str_list = list(str_set)
    is_all_number = [_str.isdigit() for _str in str_list]
    if all(is_all_number):
        return r'\d+'
    max_comm_str = get_max_comm_str(str_list)
    if max_comm_str:
        left_str_set = set()
        right_str_set = set()
        for _str in str_list:
            _str_split = _str.split(max_comm_str)
            left_str_set.add(_str_split[0])
            right_str_set.add(_str_split[1])
        left_str_regex = str_list_regex(list(left_str_set), same_regex)
        right_str_regex = str_list_regex(list(right_str_set), same_regex)
        if comm_regex:
            max_comm_str = str_regex(max_comm_str)
        return '%s%s%s' % (left_str_regex, max_comm_str, right_str_regex)
    has_none = False
    if '' in str_list:
        has_none = True
    str_list = [_str for _str in str_list if _str]
    if has_none and len(str_list) == 1 and len(str_list[0]) == 1:
        return r'%s?' % str_list[0]
    str_regex_set = set()
    for _str in str_list:
        str_regex_set.add(str_regex(_str))
    if len(str_regex_set) == 1:
        return str_regex_set.pop()
    regex = ''
    if r'\w+' in str_regex_set:
        regex = r'\w+'
    elif r'\d+' in str_regex_set:
        regex = r'\d+'
    elif r'\w' in str_regex_set:
        regex = r'\w'
    elif r'\d' in str_regex_set:
        regex = r'\d'
    if has_none:
        if '+' in regex:
            regex = regex.replace('+', '*')
        else:
            regex = '%s%s' % (regex, '*')
    return regex


def get_regex(str_list: list, sep=None, same_regex=False, comm_regex=False):
    if sep:
        str_list = [i.split(sep) for i in str_list]
    else:
        str_list = [[i] for i in str_list]
    str_list.sort(key=len)
    max_str_len = len(str_list[-1])
    regex_list = list()
    for index in range(max_str_len):
        temp_str_list = list()
        for _str_list in str_list:
            try:
                temp_str_list.append(_str_list[index])
            except IndexError as e:
                temp_str_list.append('')
        regex_list.append(str_list_regex(temp_str_list, same_regex, comm_regex))
    if sep:
        return sep.join(regex_list)
    return ''.join(regex_list)
    # return str_list_regex(str_list, same_regex, comm_regex)


def get_urls_regex(urls):
    parse_result = urls_parse(urls)
    scheme_list = parse_result['scheme_list']
    netloc_list = parse_result['netloc_list']
    path_prefix_list = parse_result['path_prefix_list']
    path_suffix_list = parse_result['path_suffix_list']
    params_list = parse_result['params_list']
    query_list = parse_result['query_list']
    fragment_list = parse_result['fragment_list']
    scheme_regex = get_regex(scheme_list)
    netloc_regex = get_regex(netloc_list, sep='.')
    path_prefix_regex = get_regex(path_prefix_list, sep='/')
    path_suffix_regex = get_regex(path_suffix_list, sep='.')
    return '%s://%s%s%s' % (scheme_regex, netloc_regex, path_prefix_regex, path_suffix_regex)
    # params_regex = get_regex(params_list, seps)
    # query_regex = get_regex(query_list, seps)
    # fragment_regex = get_regex(fragment_list, seps)
    # return '%s://%s%s%s%s%s' % (scheme_regex, netloc_regex, path_regex, params_regex, query_regex, fragment_regex)


def get_max_comm_str(str_list: list, min_length=2):
    if '' in str_list:
        return None
    if len(str_list) == 1:
        return str_list[0]
    sort_str_list = sorted(str_list, key=len)
    max_comm = set()
    min_len = len(sort_str_list[0])
    # 从最长向最短匹配
    for i in range(min_len, 0, -1):
        # 每次最多可以分出几个字符串,循环匹配的次数
        for j in range(min_len - i + 1):
            math_str = sort_str_list[0][j:j + i]
            flag = True
            # 假设有大于2个字符串需要参加匹配
            for big_str in sort_str_list[1:]:
                if math_str not in big_str:
                    flag = False
            if flag:
                max_comm.add(math_str)
        if len(max_comm) > 0:
            break
    if not max_comm:
        return None
    max_comm = max_comm.pop()
    if len(max_comm) < min_length:
        return None
    return max_comm


# TODO url正则表达式

print(get_urls_regex(urls))


def align_str(text: list, sep=None, fill=''):
    if sep:
        text_split_list = [_text.split(sep) for _text in text]
    else:
        text_split_list = [list(_text) for _text in text]
    max_str_split_list = max(text_split_list, key=len)
    max_str_len = len(max_str_split_list)
    new_text_split_list = list()
    for text_split in text_split_list:
        current_str_len = len(text_split)
        current_left = 0
        current_right = current_str_len - 1
        max_str_left = 0
        max_str_right = max_str_len

        str_split = list()
        for i in range(current_str_len):
            for j in range(max_str_len):
                if text_split[i] == max_str_split_list[j]:
                    current_left = i
                    max_str_left = j
                    print(1)


print(align_str(['http', 'https'], sep=''))
print('ax'.find('ax'))

