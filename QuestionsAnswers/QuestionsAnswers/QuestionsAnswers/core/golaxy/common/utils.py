# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/13

import random
from urllib import parse

from core.origin.common import db
from core.origin.common import base
from core.origin.common import match
from core.origin.common import internet
from core.origin.common import security
from core.origin.common import mix


class GolaxyHTMLContentXpathParser(internet.HTMLContentXpathParser):
    IMAGE_TAG = '\n{IMG: %s}\n'
    VIDEO_TAG = '\n{VIDEO: %s}\n'
    AUDIO_TAG = '\n{AUDIO: %s}\n'
    FILE_TAG = '\n{FILE: %s}\n'

    @classmethod
    def get_content_by_xpath(cls, html, pattern, base_url, *args, **kwargs):
        """
        通过xpath获取正文
        :param html: html页面
        :param pattern: xpath表达式
        :param base_url: 基url，用于补全链接
        :param args:
        :param kwargs:
        :return:
        """
        data = dict()
        data['base_url'] = base_url
        data['images'] = list()
        data['image_index'] = 0
        data['videos'] = list()
        data['video_index'] = 0
        data['audios'] = list()
        data['audio_index'] = 0
        data['files'] = list()
        data['file_index'] = 0
        raw_tags_handler = {
            'all': ('all', ['src', 'href'], cls.handle_raw_all_tag),
        }

        if 'raw_tags_handler' in kwargs:
            cls.update_tags_handler(raw_tags_handler, kwargs.get('raw_tags_handler'))
        kwargs['raw_tags_handler'] = raw_tags_handler

        tags_handler = {
            'img': ('image', ['src', ], cls.handle_image_by_tag)
        }

        if 'tags_handler' in kwargs:
            cls.update_tags_handler(tags_handler, kwargs.get('tags_handler'))
        kwargs['tags_handler'] = tags_handler

        if not kwargs.get('patterns_handler'):
            kwargs['patterns_handler'] = {}

        if not kwargs.get('raw_patterns_handler'):
            kwargs['raw_patterns_handler'] = {}

        return cls.get_data_by_xpath(html, pattern, data=data, raw_content_enabled=True,
                                     start_handle_raw_content_func=cls.start_handle_raw_content,
                                     start_handle_content_func=cls.start_handle_content, *args, **kwargs)

    @classmethod
    def start_handle_raw_content(cls, data_element, tags_handler, handle_elements, data):
        for element in data_element.iter():
            all_tag_handler = tags_handler['all']
            all_tag_handler[2](element, all_tag_handler[0], all_tag_handler[1], data)

    @classmethod
    def start_handle_content(cls, data_element, tags_handler, handle_elements, data):
        for element in data_element.iter():
            for key in tags_handler:
                if key != 'all' and element.tag == key:
                    tag_handler = tags_handler.get(key)
                    if tag_handler[2]:
                        tag_handler[2](element, tag_handler[0], tag_handler[1], data)
                    else:
                        handle_func_name = 'handle_%s_by_tag' % tag_handler[0]
                        if hasattr(cls, handle_func_name):
                            getattr(cls, handle_func_name)(element, tag_handler[0], tag_handler[1], data)
            for handle_element in handle_elements:
                if id(element) == handle_element[0]:
                    if handle_element[1]:
                        handle_element[1](*handle_element[2:], data)
                    else:
                        handle_func_name = 'handle_%s_by_pattern' % handle_element[2]
                        if hasattr(cls, handle_func_name):
                            getattr(cls, handle_func_name)(*handle_element[2:], data)
                    handle_elements.remove(handle_element)
                    break
        # 处理在正文范围外
        for handle_element in handle_elements:
            if handle_element[1]:
                handle_element[1](*handle_element[2:], data, local='tail')  # pattern_type, element, match_data, data
            else:
                handle_func_name = 'handle_%s_by_pattern' % handle_element[2]
                if hasattr(cls, handle_func_name):
                    getattr(cls, handle_func_name)(handle_element[2], data_element, handle_element[4], data, local='tail')
            handle_elements.remove(handle_element)


    @classmethod
    def update_tags_handler(cls, base_tags_handler, new_tags_handler):
        for key, value in new_tags_handler.items():
            if key in base_tags_handler:
                base_value = base_tags_handler[key]
                if base_value[0] != value[0]:
                    raise Exception('Tag 归类必须一致！')
                else:
                    base_value[1].extend(value[1])
            else:
                base_tags_handler[key] = value

    @classmethod
    def handle_raw_all_tag(cls, element, tag_type, attribs, data):
        for attrib in attribs:
            if attrib in element.attrib:
                element.attrib[attrib] = parse.urljoin(data['base_url'], element.attrib[attrib])

    @classmethod
    def handle_image_by_pattern(cls, pattern_type, element, match_data, data, local='text'):
        cls._handle_media_by_pattern(pattern_type, element, match_data, data, cls.IMAGE_TAG, local)

    @classmethod
    def handle_video_by_pattern(cls, pattern_type, element, match_data, data, local='text'):
        cls._handle_media_by_pattern(pattern_type, element, match_data, data, cls.VIDEO_TAG, local)

    @classmethod
    def handle_audio_by_pattern(cls, pattern_type, element, match_data, data, local='text'):
        cls._handle_media_by_pattern(pattern_type, element, match_data, data, cls.AUDIO_TAG, local)

    @classmethod
    def handle_file_by_pattern(cls, pattern_type, element, match_data, data, local='text'):
        cls._handle_media_by_pattern(pattern_type, element, match_data, data, cls.FILE_TAG, local)

    @classmethod
    def _handle_media_by_pattern(cls, pattern_type, element, match_data, data, media_tag, local):
        tag_type_data_key = '%ss' % pattern_type
        tag_type_index_key = '%s_index' % pattern_type
        match_data = [parse.urljoin(data['base_url'], url) for url in match_data]
        for _match_data in match_data:
            data[tag_type_data_key].append(_match_data)
            data[tag_type_index_key] += 1
            _tag = media_tag % data[tag_type_index_key]
            if local == 'text':
                if element.text:
                    element.text = '%s%s' % (element.text, _tag)
                else:
                    element.text = _tag
            elif local == 'tail':
                children = element.getchildren()
                if len(children) > 0:
                    children = children[-1]
                    if children.tail:
                        children.tail = '%s%s' % (children.tail, _tag)
                    else:
                        children.tail = _tag
                else:
                    if element.text:
                        element.text = '%s%s' % (element.text, _tag)
                    else:
                        element.text = _tag

    @classmethod
    def handle_image_by_tag(cls, element, tag_type, attribs, data):
        cls._handle_media_by_tag(element, tag_type, attribs, data, cls.IMAGE_TAG)

    @classmethod
    def handle_video_by_tag(cls, element, tag_type, attribs, data):
        cls._handle_media_by_tag(element, tag_type, attribs, data, cls.VIDEO_TAG)

    @classmethod
    def handle_audio_by_tag(cls, element, tag_type, attribs, data):
        cls._handle_media_by_tag(element, tag_type, attribs, data, cls.AUDIO_TAG)

    @classmethod
    def handle_file_by_tag(cls, element, tag_type, attribs, data):
        cls._handle_media_by_tag(element, tag_type, attribs, data, cls.FILE_TAG)

    @classmethod
    def _handle_media_by_tag(cls, element, tag_type, attribs, data, media_tag):
        for attrib in attribs:
            if attrib in element.attrib:
                tag_type_data_key = '%ss' % tag_type
                tag_type_index_key = '%s_index' % tag_type
                data[tag_type_data_key].append(element.attrib[attrib])
                data[tag_type_index_key] += 1
                if element.text:
                    element.text = '%s%s' % (element.text, media_tag % data[tag_type_index_key])
                else:
                    element.text = media_tag % data[tag_type_index_key]


class GolaxyTextUtils(base.TextUtils):
    pass


class GolaxyProxyUtils(internet.ProxyUtils):
    DOMESTIC_HTTP_PROXIES = ['10.20.18.100:7777',
                             '10.1.101.52:7777']
    DOMESTIC_HTTPS_PROXIES = []
    ABROAD_HTTP_PROXIES = ['10.1.101.52:8118']
    ABROAD_HTTPS_PROXIES = []

    @classmethod
    def get_proxy(cls, proxy_type, **kwargs):
        local = kwargs.pop('local', 'domestic')
        if proxy_type == 1:
            pass
        elif proxy_type == 2:
            local = 'abroad'
        else:
            return None
        return cls._get_proxy(local=local, **kwargs)


class GolaxyUserAgentUtils(internet.UserAgentUtils):
    @classmethod
    def get_user_agent(cls, user_agent_type, **kwargs):
        if user_agent_type == -1:
            return {'User-Agent': 'python-requests/2.25.1'}
        elif user_agent_type == 0:
            return cls._get_user_agent(platform='pc', )


class GolaxyDynamicLoadUtils(object):
    @classmethod
    def get_dynamic_load_url(cls, url, dynamic_load_type):
        if dynamic_load_type == 1:
            return 'http://crawler-splash.golaxy.local/render.html?url=%s&timeout=30&wait=5' % url
        elif dynamic_load_type == 2:
            return 'http://10.20.18.111:30095/selenium/kusen/v1?url=%s&wait=1' % url
        else:
            return url

