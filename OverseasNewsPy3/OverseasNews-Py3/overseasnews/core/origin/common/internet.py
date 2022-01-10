# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/9

import re
import time
import random
from copy import deepcopy
from urllib import request, parse

import tldextract
from lxml import etree

from core.origin.config import ua_conf
from core.origin.common import match
from core.origin.common import base


class HTMLUtils(object):
    """
    HTML相关工具
    """

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


class TextHTMLUtils(object):
    """
    HTML文本内容工具
    """

    @classmethod
    def remove_all_tags_by_regex(cls, text, sub_regex=None, sep=''):
        """
        删除html文本中的所有标签，只留文本内容
        :param text: html文本
        :param sub_regex: 附加删除正则
        :param sep: 替换后符号
        :return:
        """
        if sub_regex:
            if isinstance(sub_regex, str):
                sub_regex = [sub_regex, ]
            for regex in sub_regex:
                text = re.sub(regex, sep, text, flags=re.S | re.M)
        return re.sub(r'<.*?>', sep, text, flags=re.S | re.M).strip()

    @classmethod
    def remove_all_tags_from_content_by_regex(cls, content, sub_regex=None, sep=''):
        """
        删除html中正文区域所有标签
        :param content:
        :param sub_regex:
        :param sep:
        :return:
        """
        content = re.sub(r'<script>.*</script>', sep, content, flags=re.S | re.M)
        content = cls.remove_all_tags_by_regex(content, sub_regex, sep=sep)
        return content.strip()


# 各通用类型（视频、音频、文档、图片、文件）链接格式
URL_SUFFIX = {
    'VIDEO': ['mp4', 'ts'],
    'AUDIO': ['mp3'],
    'IMAGE': ['png', 'jpg'],
    'DOC': ['pdf', 'ppt', 'doc'],
    'COMP ': ['zip', 'rar', 'tar.gz', 'tar']
}


class URLUtils(object):
    """
    URL工具类
    """

    @classmethod
    def get_extname(cls, url):
        """
        获取URL后缀名/文件格式名
        :param url: URL链接
        :return:
        """
        try:
            return url.split('?')[0].split('.')[1]
        except IndexError:
            return None

    @classmethod
    def check(cls, url, startswith=None, endswith=None, contains=None, regex=None):
        """
        检查URL是否符合条件
        :param url: URL链接
        :param startswith: 以startswith开头
        :param endswith: 以endswith开头
        :param contains: 包含所有指定内容
        :param regex: 正则表达式
        :return:
        """
        flag = True
        if startswith:
            flag = url.startswith(startswith)
        if endswith:
            flag = url.endswith(endswith)
        if contains:
            for contain in contains:
                if contain not in url:
                    flag = False
        if regex:
            if not re.match(regex, url):
                flag = False
        return flag

    @classmethod
    def get_redirect_url(cls, url):
        """
        获取链接的重定向后链接，需联网，是同步阻塞获取的
        :param url: URL链接
        :return:
        """
        redirect = None
        try:
            redirect = request.urlopen(url, timeout=30)
        except Exception:
            pass
        if redirect and redirect == url:
            redirect = None
        return {'url': url, 'redirect': redirect}

    @classmethod
    def remove_unless_query(cls, url, unless_query=None):
        """
        去除URL中无效参数
        :param url: 要过滤的url
        :param unless_query: 不需要的query键的列表
        """
        if not unless_query:
            return url
        parser = parse.urlparse(url)
        query_dict = parse.parse_qs(parser.query)
        for query in unless_query:
            if query in query_dict:
                query_dict.pop(query)
        return parse.urlunparse(parser._replace(query=parse.urlencode(query_dict, doseq=True)))

    @classmethod
    def fill_protocol(cls, url, protocol='http'):
        """
        补全URL中的http协议
        """
        if url.startswith('http://') or url.startswith('https://'):
            return url
        for start in ['//', '://', '/', './/']:
            if url.startswith(start):
                url = url.split(start)[1]
                break
        return '%s://%s' % (protocol, url)

    @classmethod
    def find_urls_from_html(cls, text_or_html, xpath=None, tags=None, attribs=None, regex=None, base_url=None):
        """
        从html页面中提取URL
        """
        urls = set()
        init_html = HTMLUtils.init_html(text_or_html, text=True)
        html, text_html = init_html['html'], init_html['text_html']
        if xpath:
            html = html.xpath(xpath)
        if not tags:
            tags = ['a']
        if not attribs:
            attribs = ['href']
        elements = list()
        for tag in tags:
            elements.extend(html.xpath('.//%s' % tag))
        for element in elements:
            for attrib in attribs:
                urls.add(element.attrib[attrib])
        if regex:
            for url in re.findall(regex, text_html):
                urls.add(url)
        return [parse.urljoin(base_url, url) for url in urls]

    @classmethod
    def get_domain(cls, url, level=None, online=False, retry=3):
        """
        获取url的域名
        :param url: URL
        :param level: 域名级别
        :param online: 在线解析
        :param retry: 在线解析重试次数
        """

        if online:
            num = 0
            while num < retry:
                try:
                    val = tldextract.extract(url)
                    return "{0}.{1}".format(val.domain, val.suffix)
                except Exception as e:
                    num += 1
                    time.sleep(1)
        netloc = parse.urlparse(url).netloc
        if not netloc:
            return None
        netloc_split = netloc.split('.')
        netloc_split_len = len(netloc_split)
        if netloc.startswith('www'):
            netloc_split.pop(0)
        if not level:
            level = netloc_split_len
        return '.'.join(netloc_split[netloc_split_len - level - 1:netloc_split_len])

    @classmethod
    def get_urls_from_html_by_xpath(cls, html, section_pattern=None, extract_pattern=None,
                                    base_url=None, tags=None, attribs=None, keep_element=True):
        """
        从html中通过xpath获取url
        :param html: lxml.etree.Element
        :param section_pattern: 区域xpath表达式
        :param extract_pattern: 抽取xpath表达式
        :param base_url: 基础url，用于拼接完整链接
        :param tags: 标签
        :param attribs: 属性
        :param keep_element: 是否保留匹配的element
        :return:
        """
        urls = list()
        urls_set = set()
        if not tags:
            tags = ['a']
        if not attribs:
            attribs = ['href']
        if not section_pattern:
            elements = [html, ]
        else:
            elements = html.xpath(section_pattern)
        for element in elements:
            if extract_pattern:
                extract_pattern_split = match.XpathUtils.spilt_pattern(extract_pattern)
                element_pattern, data_pattern = extract_pattern_split[0][1:]
                _elements = element.xpath(element_pattern)
                for _element in _elements:
                    url = _element.xpath(data_pattern)
                    if url:
                        url = url[0].strip()
                        if url not in urls_set:
                            urls_set.add(url)
                            urls.append([_element, URLUtils.urljoin(base_url, url.strip())])
                if not keep_element:
                    urls = [url[1] for url in urls]
                    return urls
                return urls
            for tag in tags:
                for attrib in attribs:
                    _elements = element.xpath('.//%s' % tag)
                    for _element in _elements:
                        url = _element.xpath('./@%s' % attrib)
                        if url:
                            url = url[0].strip()
                            if url not in urls_set:
                                urls_set.add(url)
                                urls.append([_element, URLUtils.urljoin(base_url, url)])
        if not keep_element:
            urls = [url[1] for url in urls]
            return urls
        return urls

    @classmethod
    def urljoin(cls, base_url, urls):
        if isinstance(urls, str):
            return parse.urljoin(base_url, urls)
        return [parse.urljoin(base_url, url) for url in urls]


class UserAgentUtils(object):
    """
    UserAgent工具类
    """

    @classmethod
    def pc_user_agent(cls, _random=False, key='User-Agent', application='chrome'):
        ua = {
            key: None
        }
        if not _random:
            ua[key] = ua_conf.BASE_PC_USER_AGENT[application]
        else:
            ua[key] = random.choice(ua_conf.PC_USER_AGENTS[application])
        return ua

    @classmethod
    def m_user_agent(cls, _random=False, key='User-Agent', application='android'):
        ua = {
            key: None
        }
        if not _random:
            ua[key] = ua_conf.BASE_M_USER_AGENT[application]
        else:
            ua[key] = random.choice(ua_conf.M_USER_AGENTS[application])
        return ua

    @classmethod
    def _get_user_agent(cls, platform='pc', **kwargs):
        if platform == 'pc':
            return cls.pc_user_agent(**kwargs)
        elif platform == 'm':
            return cls.m_user_agent(**kwargs)


# xpath表达式后缀
XPATH_PATTERN_SUFFIX = {
    '//text()': './/text()',
    '/text()': './text()',
    '//@': './/@',
    '/@': './@',
}


class HTMLElementUtils(object):
    @classmethod
    def get_elements_by_xpath(cls, element, pattern, split=True, suffix='.//text()', merge=True, merge_tag='match'):
        """
        根据xpath进行匹配出标签
        :param element: 根标签
        :param pattern: xpath表达式
        :param split: 是否需要分隔xpath表达式
        :param suffix: 默认后缀
        :param merge: 在匹配多个标签下，是否生成一个新的共同父标签
        :param merge_tag: 合并时父标签的标签名
        :return:
        """
        if not pattern:
            return [(element, suffix)]
        if not split:
            pattern_list = [(pattern, pattern, suffix)]
        else:
            pattern_list = match.XpathUtils.spilt_pattern(pattern)
        for _pattern in pattern_list:
            _elements = element.xpath(_pattern[1])
            if not _elements:
                continue
            if merge:
                match_element = cls.merge_elements(_elements, merge_tag=merge_tag)
                return [(match_element, _pattern[2])]
            else:
                return [(_element, _pattern[2]) for _element in _elements]

    @classmethod
    def merge_elements(cls, elements, merge_tag='match'):
        """
        合并标签列表
        :param elements: 标签列表
        :param merge_tag: 合并的父标签标签名
        :return:
        """
        if len(elements) > 1:
            root_element = etree.Element(_tag=merge_tag)
            for element in elements:
                root_element.append(deepcopy(element))  # 使用deepcopy，不在原html中删除元素
        else:
            root_element = elements[0]
        return root_element


class HTMLContentXpathParser(object):
    @classmethod
    def get_data_by_xpath(cls,
                          html,
                          pattern=None,
                          raw_patterns_handler=None,
                          raw_tags_handler=None,
                          patterns_handler=None,
                          tags_handler=None,
                          data=None,
                          merge=True,
                          *args,
                          **kwargs):
        """
        通过xpath获取标签数据
        :param html: 根html
        :param pattern: xpath表达式
        :param raw_patterns_handler:需要在原格式html中处理的扩展表达式， {pattern_type:(pattern, func), }
        :param raw_tags_handler: 需要在原格式html中处理的指定标签处理 {tag: (tag_type, (attribs, ), func)}
        :param patterns_handler:不需要在原格式html中处理的扩展表达式
        :param tags_handler:不需要在原格式html中处理的指定标签处理
        :param data:中间传递的数据
        :param merge:
        :param args:
        :param kwargs:
        :return:
        """
        html = HTMLUtils.init_html(html)
        if data is None:
            data = {}
        if not raw_patterns_handler:
            raw_patterns_handler = {}
        if not raw_tags_handler:
            raw_tags_handler = {}
        if patterns_handler is None:
            patterns_handler = {}
        if tags_handler is None:
            tags_handler = {}
        content_elements = HTMLElementUtils.get_elements_by_xpath(html, pattern, merge=merge)
        if not content_elements:
            return {'raw_text': '', 'text': '', 'data': {}}
        if len(content_elements) == 1:
            content_element, content_data_xpath = content_elements[0]
            raw_patterns_handle_elements = cls.get_handle_elements(html, content_element, raw_patterns_handler)
            patterns_handle_elements = cls.get_handle_elements(html, content_element, patterns_handler)
            return cls.__get_data(content_element, content_data_xpath, raw_tags_handler, raw_patterns_handle_elements,
                                  tags_handler, patterns_handle_elements, data, *args, **kwargs)
        else:
            values = list()
            for content_element in content_elements:
                _content_element, _content_data_xpath = content_element
                values.extend(_content_element.xpath(_content_data_xpath))
            values = [value.strip() for value in values]
            return {'raw_text': '', 'text': values, 'data': {}}

    @classmethod
    def get_handle_elements(cls, base_element, content_element, extra_patterns):
        """
        获取扩展xpath匹配出来的符合条件的标签和数据
        :param base_element: 基础element
        :param content_element: 内容element
        :param extra_patterns: 扩展xpath表达式
        :param data:中间传递数据
        :return:
        """
        handle_elements = list()
        for pattern_type, extra_pattern in extra_patterns.items():
            _pattern, func = extra_pattern
            if not _pattern:
                continue
            _pattern_list = match.XpathUtils.spilt_pattern(_pattern)
            for __pattern in _pattern_list:
                if __pattern[1].startswith('//'):
                    elements = HTMLElementUtils.get_elements_by_xpath(base_element, __pattern[1],
                                                                      suffix=__pattern[2],
                                                                      split=False,
                                                                      merge=False)
                else:
                    elements = HTMLElementUtils.get_elements_by_xpath(content_element, __pattern[1],
                                                                      suffix=__pattern[2],
                                                                      split=False,
                                                                      merge=False)
                if elements:
                    for element in elements:
                        handle_elements.append(
                            (id(element[0]), func, pattern_type, element[0], element[0].xpath(element[1])))
                    break
        return handle_elements

    @classmethod
    def __get_data(cls,
                   data_element,
                   data_element_xpath,
                   raw_tags_handler,
                   raw_patterns_handle_elements,
                   tags_handler,
                   patterns_handle_elements,
                   data,
                   raw_content_enabled=False,
                   text_merge=True,
                   text_merge_sep='\n',
                   start_handle_raw_content_func=None,
                   start_handle_content_func=None,
                   end_handle_raw_content_func=None,
                   end_handle_content_func=None
                   ):
        """
        获取最终数据
        :param data_element: 数据element
        :param data_element_xpath: 数据xpath表达式
        :param raw_tags_handler:
        :param raw_handle_elements: 需要在原格式html中处理的elements
        :param tags_handler:
        :param handle_elements: 不需要在原格式html中处理的elements
        :param data:
        :param raw_content_enabled: 是否处理原格式
        :param text_merge: 是否合并列表数据
        :param start_handle_raw_content_func: 开始处理原格式html方法
        :param start_handle_content_func: 开始处理非原格式html方法
        :param end_handle_raw_content_func:结束处理原格式内容方法
        :param end_handle_content_func:结束处理非原格式html方法
        :return:
        """
        raw_text = ''
        text = ''
        if start_handle_raw_content_func:
            start_handle_raw_content_func(data_element, raw_tags_handler, raw_patterns_handle_elements, data)
        if raw_content_enabled:
            raw_text = '%s\n%s' % (
                raw_text, etree.tostring(data_element, encoding='utf-8', method='html').decode())

        if start_handle_content_func:
            start_handle_content_func(data_element, tags_handler, patterns_handle_elements, data)

        text_list = data_element.xpath(data_element_xpath)
        text_list = [text.strip() for text in text_list]
        text_list = base.ListUtils.remove_none(text_list)
        if text_merge:
            text = '%s%s' % (
                text, text_merge_sep.join(text_list).strip())
            text = text.strip()
        else:
            text = text_list
        if raw_content_enabled:
            if end_handle_raw_content_func:
                end_handle_raw_content_func(data)
        if end_handle_content_func:
            end_handle_content_func(data)
        return {
            'raw_text': raw_text.strip(),
            'text': text,
            'data': data
        }


class ProxyUtils(object):
    DOMESTIC_HTTP_PROXIES = None
    DOMESTIC_HTTPS_PROXIES = None
    ABROAD_HTTP_PROXIES = None
    ABROAD_HTTPS_PROXIES = None

    @classmethod
    def _get_proxy(cls, url=None, protocol='http', local='domestic'):
        _protocol = protocol
        proxies = cls.DOMESTIC_HTTP_PROXIES
        if url:
            if url.startswith('https'):
                _protocol = 'https'
        if _protocol == 'https' and local == 'domestic':
            proxies = cls.DOMESTIC_HTTPS_PROXIES
        elif _protocol == 'http' and local == 'abroad':
            proxies = cls.ABROAD_HTTP_PROXIES
        elif _protocol == 'https' and local == 'abroad':
            proxies = cls.ABROAD_HTTPS_PROXIES
        return '%s://%s' % (_protocol, random.choice(proxies))

