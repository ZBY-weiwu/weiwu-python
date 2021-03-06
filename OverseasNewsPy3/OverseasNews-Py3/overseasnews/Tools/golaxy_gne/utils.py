import os
import re
import yaml
import unicodedata
from lxml.html import fromstring, HtmlElement
from lxml.html import etree
from urllib.parse import urlparse, urljoin
from .defaults import USELESS_TAG, TAGS_CAN_BE_REMOVE_IF_EMPTY, USELESS_ATTR, HIGH_WEIGHT_ARRT_KEYWORD
import datetime

def normalize_node(element: HtmlElement):
    etree.strip_elements(element, *USELESS_TAG)
    for node in iter_node(element):
        # inspired by readability.
        if node.tag.lower() in TAGS_CAN_BE_REMOVE_IF_EMPTY and is_empty_element(node):
            remove_node(node)

        # merge text in span or strong to parent p tag
        if node.tag.lower() == 'p':
            etree.strip_tags(node, 'span')
            etree.strip_tags(node, 'strong')

        # if a div tag does not contain any sub node, it could be converted to p node.
        if node.tag.lower() == 'div' and not node.getchildren():
            node.tag = 'p'

        if node.tag.lower() == 'span' and not node.getchildren():
            node.tag = 'p'

        # remove empty p tag
        if node.tag.lower() == 'p' and not node.xpath('.//img'):
            if not (node.text and node.text.strip()):
                drop_tag(node)

        class_name = node.get('class')
        if class_name:
            if class_name in USELESS_ATTR:
                remove_node(node)
                break


def html2element(html):
    html = re.sub('</?br.*?>', '', html)
    element = fromstring(html)
    return element


def pre_parse(element):
    normalize_node(element)
    return element


def remove_noise_node(element, noise_xpath_list):

    noise_xpath_list = noise_xpath_list or config.get('noise_node_list')

    if not noise_xpath_list:
        return
    for noise_xpath in noise_xpath_list:
        nodes = element.xpath(noise_xpath)
        for node in nodes:
            remove_node(node)
    return element


def iter_node(element: HtmlElement):
    yield element
    for sub_element in element:
        if isinstance(sub_element, HtmlElement):
            yield from iter_node(sub_element)


def remove_node(node: HtmlElement):
    """
    this is a in-place operation, not necessary to return
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        parent.remove(node)


def drop_tag(node: HtmlElement):
    """
    only delete the tag, but merge its text to parent.
    :param node:
    :return:
    """
    parent = node.getparent()
    if parent is not None:
        node.drop_tag()


def is_empty_element(node: HtmlElement):
    return not node.getchildren() and not node.text


def pad_host_for_images(host, url):
    """
    ????????????????????????????????????????????????

    ????????????????????????https://xxx.com/1.jpg
    ???????????? host ?????????????????? /1.jpg
    ??? host ???????????? scheme:  xxx.com/1.jpg ??????  ://xxx.com/1.jpg

    :param host:
    :param url:
    :return:
    """
    if url.startswith('http'):
        return url
    parsed_uri = urlparse(host)
    scheme = parsed_uri.scheme
    if url.startswith(':'):
        return f'{scheme}{url}'
    if url.startswith('//'):
        return f'{scheme}:{url}'
    return urljoin(host, url)


def read_config():
    pwdpath=(os.getcwd())
    if os.path.exists(pwdpath+'/gne/gne.conf'):
        with open(pwdpath+'/gne/gne.conf', encoding='utf-8') as f:
            config_text = f.read()
        if config_text:
            config = yaml.safe_load(config_text)
            return config
    return {}


def get_high_weight_keyword_pattern():
    return re.compile('|'.join(HIGH_WEIGHT_ARRT_KEYWORD), flags=re.I)


def get_longest_common_sub_string(str1: str, str2: str) -> str:
    """
    ?????????????????????????????????????????????

    ???????????????????????????????????????1?????????????????????2????????????

      ?????????????????????
    ???0 0 0 0 00 0
    ???0 0 0 0 00 0
    ???1 0 0 0 00 0
    ???0 1 0 0 00 0
    ???0 0 1 0 00 0
    ???0 0 0 1 00 0
    ???0 0 0 0 10 0
    ???0 0 0 0 01 0

    ????????????????????????????????????????????????????????????

    :param str1:
    :param str2:
    :return:
    """
    if not all([str1, str2]):
        return ''
    matrix = [[0] * (len(str2) + 1) for _ in range(len(str1) + 1)]
    max_length = 0
    start_position = 0
    for index_of_str1 in range(1, len(str1) + 1):
        for index_of_str2 in range(1, len(str2) + 1):
            if str1[index_of_str1 - 1] == str2[index_of_str2 - 1]:
                matrix[index_of_str1][index_of_str2] = matrix[index_of_str1 - 1][index_of_str2 - 1] + 1
                if matrix[index_of_str1][index_of_str2] > max_length:
                    max_length = matrix[index_of_str1][index_of_str2]
                    start_position = index_of_str1 - max_length
            else:
                matrix[index_of_str1][index_of_str2] = 0
    return str1[start_position: start_position + max_length]


def normalize_text(html):
    """
    ?????? NFKC ????????????????????????????????????????????????????????????????????????
    :param html:
    :return:
    """


    return unicodedata.normalize('NFKC', html)


config = read_config()
