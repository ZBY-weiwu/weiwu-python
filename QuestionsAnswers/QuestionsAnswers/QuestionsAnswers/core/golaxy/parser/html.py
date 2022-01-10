#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/4/14
import re
from urllib.parse import urljoin
import copy
from lxml import etree

# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/4/6
import re
from copy import deepcopy


def str_to_html(text, whole=False):
    if whole:
        return etree.HTML(text)
    return etree.fromstring(text)


def get_data_by_xpath(html, xpath_pattern, raw=False):
    data = []
    if not isinstance(html, list):
        html = [html, ]
    for _html in html:
        data.extend(_get_data_by_xpath(_html, xpath_pattern, raw))
    return data


def _get_data_by_xpath(html, xpath_pattern, raw=False):
    if isinstance(html, str):
        html = str_to_html(html, whole=True)
    if raw:
        return html.xpath(xpath_pattern)
    if 'text()' not in xpath_pattern:
        xpath_pattern = '%s//text()' % xpath_pattern
    return html.xpath(xpath_pattern)


def replace_attrib(html, tag, attrib, replace_func):
    new_attrib_values = list()
    for element in html.iter():
        if element.tag == tag:
            element.attrib[attrib] = replace_func(element.attrib[attrib])
            new_attrib_values.append(element.attrib[attrib])
    return new_attrib_values


def remove_tag(html, tag, text_func=None):
    remove_index = 1
    if isinstance(html, str):
        html = str_to_html(html)
    for element in html.iter():
        if element.tag == tag:
            if text_func:
                previous_element = element.getprevious()
                if previous_element is None:
                    element.getparent().text = text_func(remove_index)
                else:
                    previous_element.tail = text_func(remove_index)
            element.getparent().remove(element)
            remove_index += 1


from lxml import etree


class HTMLUtils(object):
    @classmethod
    def init_html(cls, text_or_html, html=True, text=False):
        """
        初始化html页面
        """
        if isinstance(text_or_html, str):
            source_html = etree.HTML(text_or_html)
            text_html = text_or_html
        else:
            source_html = text_or_html
            text_html = etree.tostring(text_or_html, encoding='utf8').decode()
        if html and text:
            return {'html': source_html, 'text': text_html}
        if html:
            return source_html
        if text:
            return text_html

    @classmethod
    def is_render(cls, text_or_html, scale=0.3):
        """
        是否为渲染（js)页面
        """
        text_html = cls.init_html(text_or_html, html=False, text=True)
        js_content = ''.join(re.findall(r'<script.*?>(.*?)</script>', text_html, re.I | re.M | re.S))
        js_scale = len(js_content) / len(text_html)
        if js_scale >= scale:
            return True
        else:
            return False

    @classmethod
    def handle_html(cls, element, handle_tags_funcs=None, handle_elements_funcs=None, data=None):
        if not data:
            data = dict()
        tags_funcs_dict = dict()
        elements_funcs_dict = dict()
        if handle_tags_funcs:
            tags, tags_funcs = handle_tags_funcs
            tags_funcs_dict = dict(zip(tags, tags_funcs))
        if handle_elements_funcs:
            elements_funcs_dict = {id(k): v for k, v in handle_elements_funcs}
        for ele in element.iter():
            handle_func = tags_funcs_dict.get(ele.tag) or elements_funcs_dict.get(id(ele))
            if handle_func:
                handle_func(ele, data)

    @classmethod
    def get_head_tag(cls, html, copy=False):
        """
        获取head标签区域
        :param html:
        :param copy:
        :return:
        """
        _elements = html.getchildren()
        head = _elements[0]
        if head.tag == 'head':
            if copy:
                return deepcopy(head)
            return head
        return None

    @classmethod
    def get_body_tag(cls, html, copy=False):
        """
        获取body标签区域
        :param html:
        :param copy:
        :return:
        """
        _elements = html.getchildren()
        body = _elements[-1]
        if body.tag == 'body':
            if copy:
                return deepcopy(body)
            return body
        return None

    @classmethod
    def remove_tags_by_name(cls, element, names):
        """
        通过标签名删除标签
        :param element:
        :param names:
        :return:
        """
        for _element in element.iter():
            for name in names:
                if _element.tag == name:
                    _element.getparent().remove(_element)


def _add_img_tag(value):
    return "\n{IMG:" + str(value) + "}\n"


def html_urljoin_img_href(html, src_url):
    images = replace_attrib(html, 'img', 'src', replace_func=lambda url: urljoin(src_url, url))
    return images


def html_remove_img_tag(html):
    remove_tag(html, 'img', text_func=_add_img_tag)


IMAGE_TAG = '\n{IMG: %s}\n'
VIDEO_TAG = '\n{VIDEO: %s}\n'
AUDIO_TAG = '\n{AUDIO: %s}\n'
FILE_TAG = '\n{FILE: %s}\n'


class XpathUtils(object):
    @classmethod
    def match_content(cls, text_or_html, pattern=None, raw_content_enabled=False, ele_pattern_list=None,
                      start_handle_raw_content_func=None, start_handle_content_func=None,
                      end_handle_raw_content_func=None, end_handle_content_func=None,
                      *args, **kwargs):
        """
        xpath匹配内容
        :param text_or_html: html内容
        :param pattern:正文xpath
        :param raw_content_enabled:是否处理html格式正文
        :param ele_pattern_list: 详细定位指定元素进行处理，[(xpath, tag标记, 处理函数)]
        :param start_handle_raw_content_func:原文开始处理函数
        :param start_handle_content_func:正文开始处理函数
        :param end_handle_raw_content_func:原文处理后处理函数
        :param end_handle_content_func:正文处理后处理函数
        :param args:
        :param kwargs:
        :return:{raw_content: , content: , data: }
        """
        html = cls.__to_html(text_or_html)
        temp_data = dict()
        temp_data.update(**kwargs)
        raw_content = ''
        content = ''
        content_html = None
        handle_elements = list()
        success_pattern = (None, None, './/text()')
        if pattern:
            pattern_list = cls.split_xpath_pattern_by_text(pattern)
            if pattern_list:
                for _pattern in pattern_list:
                    success_pattern = _pattern
                    elements = html.xpath(_pattern[1])
                    if elements:
                        if len(elements) > 1:
                            content_html = etree.Element('div')
                            for ele in elements:
                                if not ele.getchildren() and not ele.text:
                                    continue
                                content_html.append(copy.deepcopy(ele))
                            if not content_html.getchildren():
                                continue
                        else:
                            element = elements[0]
                            if not element.getchildren() and not element.text:
                                continue
                            content_html = element
                        break
        else:
            content_html = html
        if ele_pattern_list:
            for ele_pattern, tag, func in ele_pattern_list:
                if not ele_pattern:
                    continue
                xpath_pattern_list = cls.split_xpath_pattern_by_attrib(ele_pattern)
                for xpath_pattern in xpath_pattern_list:
                    _pattern = xpath_pattern[1]
                    if _pattern.startswith('//'):
                        ele_list = html.xpath(_pattern)
                    else:
                        if _pattern.startswith('./') and not _pattern.startswith('.//'):
                            _pattern = _pattern.replace('./', './/')
                        ele_list = content_html.xpath(_pattern)
                    if ele_list:
                        for ele in ele_list:
                            match_items = ele.xpath(xpath_pattern[2])
                            match_items = list(
                                map(lambda item: item.replace('//', 'http://') if item.startswith('//') else item,
                                    match_items))
                            handle_elements.append((ele, tag, match_items, func))
                        break
        if start_handle_raw_content_func:
            start_handle_raw_content_func(content_html, handle_elements, temp_data)
        if raw_content_enabled:
            raw_content = '%s\n%s' % (
                raw_content, etree.tostring(content_html, encoding='utf-8', method='html').decode())
        if start_handle_content_func:
            start_handle_content_func(content_html, handle_elements, temp_data)
        content = '%s\n%s' % (
            content, ''.join(content_html.xpath(success_pattern[2])).strip())
        if raw_content_enabled:
            if end_handle_raw_content_func:
                end_handle_raw_content_func(temp_data)
        if end_handle_content_func:
            end_handle_content_func(temp_data)
        return {
            'raw_content': raw_content.strip(),
            'content': content.strip(),
            'data': temp_data
        }

    @classmethod
    def __to_html(cls, text_or_html):
        """
        转为lxml.etree.Element对象
        :param text_or_html: html内容
        :return:
        """
        if isinstance(text_or_html, str):
            return etree.HTML(text=text_or_html)
        return text_or_html

    @classmethod
    def split_xpath_pattern_by_attrib(cls, xpath_pattern):
        """
        根据带有属性的xpath表达式进行切割
        :param xpath_pattern: xpath表达式
        :return:
        """
        if not xpath_pattern:
            return
        pattern_list = list()
        xpath_pattern_list = xpath_pattern.split('|')
        for _xpath_pattern in xpath_pattern_list:
            source_xpath_pattern = _xpath_pattern
            _xpath_pattern_list = _xpath_pattern.split('/@')
            if len(_xpath_pattern_list) > 1:
                left_xpath_pattern, right_xpath_pattern = _xpath_pattern_list[0], './@%s' % _xpath_pattern_list[1]
            else:
                left_xpath_pattern, right_xpath_pattern = _xpath_pattern_list[0], None
            pattern_list.append((source_xpath_pattern, left_xpath_pattern, right_xpath_pattern))
        return pattern_list

    @classmethod
    def split_xpath_pattern_by_text(cls, xpath_pattern):
        """
        通过/text()、//text()、默认等三种情况进行分割xpath表达式
        :param xpath_pattern: xpath表达式
        :return: 分割后的xpath表达式列表
        """
        pattern_list = list()
        xpath_pattern_list = xpath_pattern.split('|')
        for _xpath_pattern in xpath_pattern_list:
            source_xpath_pattern = _xpath_pattern
            _xpath_pattern_list = _xpath_pattern.split('//text()')
            if len(_xpath_pattern_list) > 1:
                left_xpath_pattern, right_xpath_pattern = _xpath_pattern_list[0], './/text()'
            else:
                _xpath_pattern_list = _xpath_pattern.split('/text()')
                if len(_xpath_pattern_list) > 1:
                    left_xpath_pattern, right_xpath_pattern = _xpath_pattern_list[0], './text()'
                else:
                    left_xpath_pattern = source_xpath_pattern
                    right_xpath_pattern = ''
                    if '/@' not in source_xpath_pattern:
                        right_xpath_pattern = './/text()'
            pattern_list.append((source_xpath_pattern, left_xpath_pattern, right_xpath_pattern))
        return pattern_list


class GolaxyHtmlContentXpathParser(XpathUtils):
    @classmethod
    def start_handle_raw_content(cls, element, handle_elements, temp_data):
        for ele in element.iter():
            for key in ['src', '_src', 'href', 'data_src', 'link']:
                if key in ele.attrib:
                    ele.attrib[key] = urljoin(temp_data['src_url'], ele.attrib[key])

    @classmethod
    def start_handle_content(cls, element, handle_elements, temp_data):
        images = list()
        videos = list()
        audios = list()
        files = list()
        for ele in element.iter():
            if ele.tag == 'img':
                images.append(ele.attrib['src'])
                temp_data['image_index'] += 1
                if ele.text:
                    ele.text = '%s%s' % (ele.text, IMAGE_TAG % temp_data['image_index'])
                else:
                    ele.text = IMAGE_TAG % temp_data['image_index']
            for handle_element in handle_elements:
                if ele == handle_element[0]:
                    handle_element[3](ele, handle_element[1], handle_element[2], temp_data)
                    handle_elements.remove(handle_element)
                    break
        # 处理在正文范围外
        for handle_element in handle_elements:
            handle_element[3](element, handle_element[1], handle_element[2], temp_data)
        temp_data['images'] = images
        temp_data['videos'] = videos
        temp_data['audios'] = audios
        temp_data['files'] = files

    @classmethod
    def match_content(cls, *args, **kwargs):
        video_xpath = kwargs.pop('video_xpath', None)
        audio_xpath = kwargs.pop('audio_xpath', None)
        file_xpath = kwargs.pop('file_xpath', None)
        image_xpath = kwargs.pop('image_xpath', None)
        kwargs['image_index'] = 0
        kwargs['video_index'] = 0
        kwargs['file_index'] = 0
        kwargs['audio_index'] = 0
        kwargs['images'] = list()
        kwargs['videos'] = list()
        kwargs['audios'] = list()
        kwargs['files'] = list()
        return super(GolaxyHtmlContentXpathParser, cls).match_content(
            start_handle_raw_content_func=cls.start_handle_raw_content,
            start_handle_content_func=cls.start_handle_content,
            raw_content_enabled=True, ele_pattern_list=[
                (video_xpath, 'video', cls.handle_video),
                (audio_xpath, 'audio', cls.handle_audio),
                (file_xpath, 'file', cls.handle_file),
                (image_xpath, 'image', cls.handle_image),
            ], *args, **kwargs)

    @classmethod
    def handle_video(cls, ele, tag, xpath, temp_data):
        cls.handle_media(ele, tag, xpath, temp_data, VIDEO_TAG)

    @classmethod
    def handle_audio(cls, ele, tag, xpath, temp_data):
        cls.handle_media(ele, tag, xpath, temp_data, AUDIO_TAG)

    @classmethod
    def handle_file(cls, ele, tag, xpath, temp_data):
        cls.handle_media(ele, tag, xpath, temp_data, FILE_TAG)

    @classmethod
    def handle_image(cls, ele, tag, xpath, temp_data):
        cls.handle_media(ele, tag, xpath, temp_data, IMAGE_TAG)

    @classmethod
    def handle_media(cls, ele, tag, match_items, temp_data, add_tag):
        """
        处理多媒体逻辑
        :param ele: 定位的element对象
        :param tag: 改对象的标记
        :param match_items: 匹配到的数据
        :param temp_data:
        :param add_tag: 打标的标记
        :return:
        """
        key = '%ss' % tag
        temp_data[key].extend(match_items)
        tag_index_key = '%s_index' % tag
        temp_data[tag_index_key] += 1
        ele_child_list = ele.getchildren()
        if ele_child_list:
            ele_child_list[-1].tail = '%s%s' % (ele_child_list[-1].tail, add_tag % temp_data[tag_index_key]) if \
                ele_child_list[-1].tail else add_tag % temp_data[tag_index_key]
        else:
            ele.text = '%s%s' % (ele.text, add_tag % temp_data[tag_index_key]) if ele.text else add_tag % temp_data[
                tag_index_key]


class GolaxyHtmlCommonXpathParser(XpathUtils):
    pass


class GolaxyHtmlUtils(object):
    @classmethod
    def parse_content(cls, *args, **kwargs):
        return GolaxyHtmlContentXpathParser.match_content(*args, **kwargs)

    @classmethod
    def parse_common(cls, *args, **kwargs):
        return GolaxyHtmlCommonXpathParser.match_content(*args, **kwargs)
