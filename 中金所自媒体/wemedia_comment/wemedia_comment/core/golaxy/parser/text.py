#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/5/18
import re
import html

IMAGE_TAG = '\n{IMG: %s}\n'
VIDEO_TAG = '\n{VIDEO: %s}\n'


def text_unescape(text):
    return html.unescape(text)


def text_tagging_replace(text, regex=None, tag=None, html_tag=None, has_suffix=True, retain_text=True,
                         replace_func=None, replace_template=None, match_func=None, match_regex=None,
                         unescape=False):
    if unescape:
        text = text_unescape(text)
    pattern = ''
    if regex:
        pattern = regex
    elif tag:
        pattern = tag
    elif html_tag:
        if has_suffix:
            pattern = '(<%s.*?>)(.*?)(</%s>)' % (html_tag, html_tag)
        else:
            pattern = '(<%s.*?>)' % html_tag
    match_list = list(re.finditer(pattern, text, re.S | re.M | re.I))
    if replace_func:
        for match_index, match in enumerate(match_list):
            text = replace_func(text, replace_template, match_index, match, retain_text)
    items = list()
    if match_func:
        for match in match_list:
            items.extend(match_func(match, match_regex))
    else:
        for match in match_list:
            items.extend(match.groups())
    return text, items


def text_tagging_append(text, items=None, append_func=None, append_template=None, unescape=False):
    if unescape:
        text = text_unescape(text)
    if not items:
        return text
    if append_func:
        for index, item in enumerate(items):
            text = append_func(text, append_template, index, item)
    return text


def replace_func(text, replace_template, match_index, match, retain_text):
    groups = match.groups()
    if not groups:
        groups = (match.group(),)
    if len(groups) == 3:
        if not retain_text:
            old = ''.join(groups)
        else:
            text = text.replace(groups[2], '', 1)
            old = groups[0]
    else:
        old = groups[0]
    text = text.replace(old, replace_template % (match_index + 1), 1)
    return text


def match_func(match, match_regex):
    return re.findall(match_regex, match.group())


def text_tagging_replace_images(text, unescape=False):
    text, images = text_tagging_replace(text, html_tag='img', replace_func=replace_func,
                                        replace_template=IMAGE_TAG, has_suffix=False, retain_text=True,
                                        unescape=unescape, match_func=match_func, match_regex=r'src="(.*?)"')
    return text, images


def text_tagging_replace_common(text, **kwargs):
    kwargs.setdefault('replace_func', replace_func)
    kwargs.setdefault('match_func', match_func)
    return text_tagging_replace(text, **kwargs)


def append_images_func(text, append_template, index, item):
    return '%s%s' % (text, append_template % (index + 1))


def text_tagging_append_images(text, images, unescape=False):
    return text_tagging_append(text, items=images, append_func=append_images_func, append_template=IMAGE_TAG,
                               unescape=unescape)
