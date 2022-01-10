# -*- coding:utf-8 -*-
# author: weiwu
# email: by951118@163.com
# date: 2021/12/22
import os
from lxml import etree
import logging
import re
import json
from w3lib import html as w3lib_html
from GolaxyRequests import GolaxyRequests
from Tools.utils import parse_publish_time
from Tools.DBConnect.py_db import PgDB
from Tools.utils import replace_by_img_tag,domain_extraction1

class overseas_news_test:
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    @classmethod
    def download_html(cls,url,**kwargs):
        html = GolaxyRequests.get(url,**kwargs).text
        return html

    @classmethod
    def read_seed(cls):
        for root, dirs, files in os.walk("./seed"):
            for file in files:
                with open("./seed/"+file,encoding="utf-8") as f:
                    seed_obj = f.read()
            return seed_obj

    @classmethod
    def pg_insert(cls,cfg):

        proxy_enabled = cfg.get("proxy_enabled")
        js_enabled = cfg.get("js_enabled")
        media_name = cfg.get("media_name")
        board_name = cfg.get("board_name")
        media_id = cfg.get("media_id")
        entry_url = cfg.get("entry_url")
        location = cfg.get("location") or "其他"
        extractor_config = json.dumps(cfg.get("extractor_config"),ensure_ascii=False)

        domain_url = domain_extraction1(entry_url)
        sql = "SELECT * FROM sjzt_wcm_boards_copy1 WHERE url ='{}' and channel=4;".format(entry_url)
        if PgDB.Whether_exist(sql):
            cls.logger.error("Website already exists!")
            return
        sql_data = 'INSERT INTO "sjzt_wcm_boards_copy1" (board_name, channel, url, "domain", "location", tags, site_id, site_name, status, create_time, update_time, creator, update_by, "period", last_gather_time, js_enabled, crawler_id, proxy_enabled, proxy_group_id, extractor_config, old_board_id, config, reserve1, reserve2, account_enabled, account_group_id, tenant_id, "encoding", "language", disabled, application_id, location_id, approve_info, remarks, alarm_is_access, alarm_time_window, alarm_data_volume) VALUES '+"""('{board_name}', 4, '{entry_url}', '{domain_url}', '{location}', '{{}}', {media_id}, '{media_name}', 7, '2021-12-20 18:22:47.000', '2021-08-18 18:22:47.000', '{{"jss"}}', NULL, 180, 0, {js_enabled}, 0, {proxy_enabled}, 0, '{extractor_config}', 0, '', NULL, NULL, 0, 0, '{{"jss"}}', NULL, NULL, false, NULL, '', NULL, NULL, false, NULL, NULL);""".format(proxy_enabled=proxy_enabled,js_enabled=js_enabled,media_name=media_name,board_name=board_name,media_id=media_id,entry_url=entry_url,location=location,extractor_config=extractor_config,domain_url=domain_url)
        print(sql_data)
        PgDB.Pg_write(sql_data)
        cls.logger.info("config write success")
    @classmethod
    def article_parse(cls,cfg):
        url = cfg.get("detail_page_url")
        proxy_enabled = cfg.get("proxy_enabled")
        if proxy_enabled==1:
            proxies = {'http': 'http://127.0.0.1:10809', 'https': 'http://127.0.0.1:10809'}
            resp = cls.download_html(url,proxies=proxies)
        else:
            resp = cls.download_html(url)
        resp = w3lib_html.remove_comments(resp)
        extractor_config = cfg.get("extractor_config")
        extract_config = extractor_config["extract_config"]
        title_xpath = extract_config.get("title_xpath")
        content_xpath = extract_config.get("content_xpath")
        publish_time_xpath = extract_config.get("publish_time_xpath")
        author_xpath = extract_config.get("author_xpath")
        media_name = extract_config.get("media_name")
        html_pages = etree.HTML(resp)
        data_obj = {}

        data_obj["media_name"]=media_name
        data_obj["detail_page_url"] = url
        if title_xpath:
            if "//text()" not in title_xpath:
                title_xpath += "//text()"
            data_obj["title"] = "".join(html_pages.xpath(title_xpath))
        else:
            cls.logger.error("title_xpath is None")
            return
        if len(data_obj["title"])<1:
            cls.logger.error("title_xpath is analysis error")
            return
        if publish_time_xpath:
            if "//text()" not in publish_time_xpath:
                publish_time_xpath += "//text()"
            publish_time = "".join(html_pages.xpath(publish_time_xpath))
            data_obj["publish_time"] = parse_publish_time(publish_time)
        else:
            cls.logger.error("publish_time_xpath is None")
            return
        if len(publish_time)<1:
            cls.logger.error("publish_time_xpath is analysis error")
            return
        if author_xpath:
            if "//text()" not in author_xpath:
                author_xpath += "//text()"
            data_obj["author"] = html_pages.xpath(author_xpath)
        else:
            data_obj["author"] =''
        if content_xpath:
            content_xpath = content_xpath.replace("//text()","")
            content_html = html_pages.xpath(content_xpath)
            try:
                tmp_content = ''
                for _content_data in content_html:
                    tmp_content += etree.tostring(_content_data, encoding='utf-8').decode()
                content_data = tmp_content
                content = re.sub("<img.*?src=.*?>", "{img}", content_data, 0, re.S | re.M | re.I)
            except Exception as e:
                cls.logger.error("content_xpath analysis Error")
                return
            data_obj['images'] = re.findall("<img.*?src=\"(.*?)\".*?>", content_data)
            content = w3lib_html.remove_tags(content, which_ones=('script', 'style'))
            dr = re.compile(r'<[^>]+>', re.S)
            content = dr.sub('', content)
            data_obj['content'] = replace_by_img_tag(content)
            cls.logger.info("End of test")
            return data_obj
        else:
            cls.logger.error("content_xpath is None")
            return

    @classmethod
    def main_pg(cls):
        for cfg in json.loads(cls.read_seed()):
            print(cfg)
            cls.pg_insert(cfg)

    @classmethod
    def output_write(cls):
        output = []
        for cfg in json.loads(cls.read_seed()):
            output.append(cls.article_parse(cfg))
        with open("./output/file.json","a+",encoding="utf-8") as f:
            f.write(json.dumps(output, ensure_ascii=False))
        write_pg = input("\n是否将配置写入Pg{True|False}：\n")
        if write_pg=="True":
            cls.main_pg()
        else:
            pass

    @classmethod
    def main(cls):
        cls.output_write()
        return "END"


if __name__ == '__main__':
    print(overseas_news_test.output_write())


