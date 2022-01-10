# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/15

from core.origin.common import mix
from core.origin.config import datetime_conf


class WebPagePublishDateTimeParser(object):
    @classmethod
    def parse(cls, datetime_string=None, html_and_text=None, xpath=None, **kwargs):
        if datetime_string:
            return mix.DateTimeUtils.parse_text_datetime(datetime_string, **kwargs)
        html, text = html_and_text
        result = cls.parse_by_xpath(html, xpath) or cls.parse_by_meta(html) or text
        return mix.DateTimeUtils.parse_text_datetime(result, **kwargs)

    @classmethod
    def parse_by_meta(cls, html):
        try:
            head_element = html.xpath('//head')[0]
        except IndexError:
            head_element = html
        for meta_xpath in datetime_conf.WEB_PAGE_PUBLISH_DATETIME_META_XPATH:
            result = head_element.xpath(meta_xpath)
            if result:
                return result[0]

    @classmethod
    def parse_by_xpath(cls, html, xpath):
        if not xpath:
            return
        result = html.xpath(xpath)
        if result:
            return result[0]


class WebPageAuthorParser(object):
    pass


class WebPageSourceParser(object):
    @classmethod
    def parse(cls, source_text=None, html_and_text=None, xpath=None, match_regex=None, handle_regex=None, **kwargs):
        pass


class WebPageContentParser(object):
    pass


class WebPageTitleParser(object):
    pass


class WebPageBoardParser(object):
    pass
