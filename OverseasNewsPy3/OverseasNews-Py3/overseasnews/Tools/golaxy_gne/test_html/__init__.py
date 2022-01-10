from .utils import pre_parse, remove_noise_node, config, html2element, normalize_text
from gne.extractor import ContentExtractor, TitleExtractor, TimeExtractor, AuthorExtractor, ListExtractor
import re
import json
from lxml import etree
from urllib.parse import urljoin
from .tool import *
def replace_by_img_tag(txt):
    begin = 0
    end = 0
    i = 1
    while True:
        end = txt.find('{img}', begin)
        if end == -1:
            break
        new = '\n{IMG:' + str(i) + '}\n'
        txt = txt.replace('{img}', new, 1)
        begin = end + len(new)
        i = i + 1
    return txt

class GeneralNewsExtractor:
    def extract(self,
                html,
                title_xpath='',
                author_xpath='',
                publish_time_xpath='',
                host='',
                body_xpath='',
                noise_node_list=None,
                with_body_html=False):

        # 对 HTML 进行预处理可能会破坏 HTML 原有的结构，导致根据原始 HTML 编写的 XPath 不可用
        # 因此，如果指定了 title_xpath/author_xpath/publish_time_xpath，那么需要先提取再进行
        # 预处理
        normal_html = normalize_text(html)
        doc = re.sub(r'<!--.*?-->','',normal_html, re.S | re.M |re.I)
        doc = re.sub(r'<meta.*?>', '', doc)
        doc = re.sub(r'<script>.*?</script>', '', doc)
        dr = re.compile(r'<[^>]+>', re.S)
        doc = dr.sub('', doc)

        pubtime_re=str_to_timestamp(doc)
        #print(pub_time)
        #增加稿件来源提取，采用正则方式
        source=''
        #results = re.search(r">*\s*[　]*来源\s*[：\-:](</em>)*\s*(\S*?)((<)|(\s)|(/)|(，)|(）|\"))", doc, re.M|re.I)
        #if '来源：' in doc:
            #print("*"*100)
        results = re.search(r">*\s*[　]*来源\s*[：\-:](</em>)*\s*(\S*?)((<)|(\s)|(/)|(，)|(）|\"))", doc, re.M | re.I)

        if results:
            source= results.group(2)
            source=source.strip()

        normal_html = normalize_text(html)
        element = html2element(normal_html)
        title = TitleExtractor().extract(element, title_xpath=title_xpath)
        publish_time = TimeExtractor().extractor(element, publish_time_xpath=publish_time_xpath)
        author = AuthorExtractor().extractor(element, author_xpath=author_xpath)
        element = pre_parse(element)
        remove_noise_node(element, noise_node_list)
        content = ContentExtractor().extract(element,
                                             host=host,
                                             with_body_html=with_body_html,
                                             body_xpath=body_xpath)
        pubtime_gne=str_to_timestamp(publish_time)
        publish_time=get_real_time(pubtime_re,pubtime_gne)

        result = {'title': title,
                  'author': author,
                  #'pub_time':publish_time,
                  'publish_time': publish_time,
                  #'content': content[0][1]['text'],
                  'source':source,
                  'images': []#content[0][1]['images']
                  }
        if with_body_html or config.get('with_body_html', False):
            result['body_html'] = content[0][1]['body_html']

        content = re.sub("<img.*?src=.*?>", "{img}", result['body_html'], 0, re.S | re.M | re.I)
        content = re.sub(r'<!--.*?-->', '', content,  flags=re.DOTALL)
        content = re.sub(r'<script>.*?</script>', '', content)

        content = replace_by_img_tag(content)
        dr = re.compile(r'<[^>]+>', re.S)
        content = dr.sub('', content)

        result['content'] = content
        pics = re.findall("<img.*?src=\"(.*?)\".*?>", result['body_html'])
        for pic in pics:
            pic = urljoin(host, pic)
            result['images'].append(pic)
        return result


class ListPageExtractor:
    def extract(self, html, feature):
        normalize_html = normalize_text(html)
        element = html2element(normalize_html)
        extractor = ListExtractor()
        return extractor.extract(element, feature)
