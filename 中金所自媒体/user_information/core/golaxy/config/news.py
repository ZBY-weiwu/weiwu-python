import copy
import json
import time
from html import unescape
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import tostring, fromstring
from core.golaxy.common.utils import internet


def pretty_xml(element, indent, newline, level=0):
    """
    美化xml保存格式
    :param element: elemnt为传进来的Elment类
    :param indent: 缩进字符
    :param newline: 换行符号
    :param level:
    :return:
    """
    if element:  # 判断element是否有子元素
        if (element.text is None) or element.text.isspace():  # 如果element的text没有内容
            element.text = newline + indent * (level + 1)
        else:
            element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * (level + 1)
            # else:  # 此处两行如果把注释去掉，Element的text也会另起一行
            # element.text = newline + indent * (level + 1) + element.text.strip() + newline + indent * level
    temp = list(element)  # 将element转成list
    for subelement in temp:
        if temp.index(subelement) < (len(temp) - 1):  # 如果不是list的最后一个元素，说明下一个行是同级别元素的起始，缩进应一致
            subelement.tail = newline + indent * (level + 1)
        else:  # 如果是list的最后一个元素， 说明下一行是母元素的结束，缩进应该少一个
            subelement.tail = newline + indent * level
        pretty_xml(subelement, indent, newline, level=level + 1)  # 对子元素进行递归操作


class GolaxyDBNewsConfig(object):
    fields = ['idcrawler_config', 'cid', 'channel', 'time_modify', 'match_key',
              'name', 'description', 'config', 'schedule', 'tag_classify',
              'status', 'app_id', 'tag_appid', 'time_create', 'refresh_period',
              'site_id', 'site_name', 'entry_url', 'domain_url', 'board_name',
              'accurate_extraction', 'update_time', 'location', 'country',
              'priority', 'domain_status', 'js_enabled_golaxy', 'gfw_enabled_golaxy']

    def __init__(self, cid, config, site_id, site_name, entry_url, board_name, **kwargs):
        now = int(time.time())
        self.idcrawler_config = None
        self.cid = cid
        self.channel = 1
        self.time_modify = None
        self.match_key = entry_url
        self.name = board_name
        self.description = ''
        self.config = config
        self.schedule = '<ss c="10"><p>8</p><f>600</f></ss>'
        self.tag_classify = 'y10,m101'
        self.status = 1
        self.app_id = 1
        self.tag_appid = 'default'
        self.time_create = time.strftime('%Y-%m-%d %X', time.localtime(now))
        self.refresh_period = 600
        self.site_id = site_id
        self.site_name = site_name
        self.entry_url = entry_url
        self.domain_url = None
        self.board_name = board_name  #
        self.accurate_extraction = None  #
        self.update_time = int(now)
        self.location = '北京'
        self.country = '中国'
        self.priority = 10800
        self.domain_status = 1
        self.js_enabled_golaxy = 0
        self.gfw_enabled_golaxy = 0
        self.__dict__.update(kwargs)
        self.check_all()

    def check_all(self):
        for key in self.__dict__:
            if key.startswith('_'):
                key = key[1:]
            func = '_check_%s' % key
            if hasattr(self, func):
                getattr(self, func)()

    def _check_domain_url(self):
        if not self.domain_url:
            self.domain_url = get_domain(self.entry_url)

    def to_mysql(self, mysql_obj, table_name):
        config_dict = copy.deepcopy(self.__dict__)
        config_keys = list()
        config_values = list()
        for key in config_dict.keys():
            if config_dict[key] is not None:
                config_keys.append(key)
                config_values.append(config_dict[key])
        sql = 'insert into %s (%s) values %s' % (
            table_name, ','.join(config_keys),
            json.dumps(config_values, ensure_ascii=False).replace('[', '(').replace(']', ')'))
        print(sql)
        mysql_obj.modify(sql)

    @classmethod
    def from_mysql(cls, mysql, sql):
        rows = mysql.select(sql)
        if not rows:
            raise Exception('MySQL中没有符合条件的配置信息')
        if len(rows) == 1:
            return GolaxyDBNewsConfig(**rows[0])
        else:
            db_config_list = GolaxyDBNewsConfigList()
            for row in rows:
                db_config_list.add_config(GolaxyDBNewsConfig(**row))
            return db_config_list

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, dict):
            return cls._from_json(data)
        elif isinstance(data, list):
            config_list = GolaxyDBNewsConfigList()
            for config in data:
                config_list.add_config(cls._from_json(config))
            return config_list
        else:
            raise Exception('json数据错误！')

    @classmethod
    def _from_json(cls, data):
        kwargs = dict()
        config = GolaxyNewsConfig.from_json(data)
        kwargs['config'] = config.get_config_str()
        for key in data:
            if key in cls.fields:
                kwargs[key] = data[key]
            if 'board_id' == key:
                kwargs['cid'] = data[key]
        return GolaxyDBNewsConfig(**kwargs)

    def get_config(self):
        return GolaxyNewsConfig(**self._get_config_kwargs())

    def _get_config_kwargs(self):
        et = ET.ElementTree(fromstring(self.config)).getroot()
        kwargs = dict()
        for node in list(et):
            kwargs[node.tag] = node.text
        return kwargs


class GolaxyDBNewsConfigList(object):
    def __init__(self, db_config_list=None):
        if db_config_list is None:
            db_config_list = list()
        for config in db_config_list:
            if isinstance(config, GolaxyDBNewsConfig):
                raise Exception('列表中含有不是GolaxyNewsConfig对象的元素')
        self.db_config_list = db_config_list

    def add_config(self, config):
        self.db_config_list.append(config)

    def to_mysql(self, mysql_obj, table_name):
        for config in self.db_config_list:
            config.to_mysql(mysql_obj, table_name)

    def get_config(self):
        config_list = GolaxyNewsConfigList()
        for config in self.db_config_list:
            config_list.add_config(config.get_config())
        return config_list


class GolaxyNewsConfig(object):
    fields = ['app_id', 'board_id', 'site_id', 'channel_id', 'board_name',
              'site_name', 'entry_url', 'entry_type', 'character_set',
              'current_news_regex', 'gather_depth', 'js_enabled', 'http_interval',
              'gfw_enabled', 'docurl_regex_yes', 'docurl_regex_no', 'docurl_regex_page',
              'imgurl_regex_yes', 'imgurl_regex_no', 'boardurl_page_regex',
              'boardurl_max_pages', 'evidence_degree', 'importance_degree',
              'is_homepage', 'board_class_tag', 'refresh_period', 'sub_board_list',
              'extractor_config', 'post_enabled']

    def __init__(self, board_id, site_id, board_name, site_name, entry_url, docurl_regex_yes, **kwargs):
        self.app_id = 1
        self.board_id = board_id
        self.site_id = site_id
        self.channel_id = 1
        self.board_name = board_name
        self.site_name = site_name
        self.entry_url = entry_url
        self.entry_type = 0
        self.character_set = '*|*'
        self.current_news_regex = None
        self.gather_depth = 1
        self.js_enabled = 0
        self.http_interval = 0
        self.gfw_enabled = 0
        self.docurl_regex_yes = docurl_regex_yes  #
        self.docurl_regex_no = None  #
        self.docurl_regex_page = None  #
        self.imgurl_regex_yes = None  #
        self.imgurl_regex_no = None  #
        self.boardurl_page_regex = None
        self.boardurl_max_pages = 10
        self.evidence_degree = 3
        self.importance_degree = 3
        self.is_homepage = 0
        self.board_class_tag = 'y10,m101'
        self.refresh_period = 600
        self.sub_board_list = None
        self.extractor_config = None
        self.post_enabled = 0
        self.__dict__.update(kwargs)

    def _get_element(self):
        et = ET.Element('board')
        for child_tag_name in self.__dict__.keys():
            text = self.__dict__[child_tag_name]
            if text == 'None':
                text = ''
            if isinstance(text, int):
                text = str(text)
            ET.SubElement(et, child_tag_name).text = text
        return et

    def to_xml(self, file_path):
        et = self._get_element()
        pretty_xml(et, '\t', '\n')
        et_tree = ET.ElementTree(et)
        et_tree.write(file_path, encoding="utf-8", short_empty_elements=True)

    @classmethod
    def from_xml(cls, file_path):
        xml_tree = ET.parse(file_path)
        root = xml_tree.getroot()
        if root.tag == 'board':
            return cls.parse_xml_config(root)
        elif root.tag == 'board_list':
            config_list = GolaxyNewsConfigList()
            for board_node in root.iter('board'):
                config_list.add_config(cls.parse_xml_config(board_node))
            return config_list

    @classmethod
    def from_json(cls, data):
        if isinstance(data, str):
            data = json.loads(data)
        if isinstance(data, dict):
            return cls._from_json(data)
        elif isinstance(data, list):
            config_list = GolaxyNewsConfigList()
            for config in data:
                config_list.add_config(cls._from_json(config))
            return config_list
        else:
            raise Exception('json数据错误！')

    @classmethod
    def _from_json(cls, data):
        kwargs = dict()
        for key in data:
            if key in cls.fields:
                value = data[key]
                if isinstance(value, str):
                    if '&amp;' not in value and '&' in value:
                        value.replace('&', '&amp;')
                kwargs[key] = value
        return GolaxyNewsConfig(**kwargs)

    @classmethod
    def parse_xml_config(cls, board_node):
        kwargs = {}
        for node in list(board_node):
            kwargs[node.tag] = node.text
        return GolaxyNewsConfig(**kwargs)

    def get_config_str(self):
        return unescape(tostring(self._get_element()).decode('utf-8'))

    def get_db_config(self):
        config = self.get_config_str()
        domain_url = internet.URLUtils.get_domain(self.entry_url)
        return GolaxyDBNewsConfig(cid=self.board_id, config=config,
                                  site_id=self.site_id, site_name=self.site_name, entry_url=self.entry_url,
                                  domain_url=domain_url, board_name=self.board_name)


class GolaxyNewsConfigList(object):
    def __init__(self, config_list=None):
        if config_list is None:
            config_list = list()
        for config in config_list:
            if isinstance(config, GolaxyNewsConfig):
                raise Exception('列表中含有不是GolaxyNewsConfig对象的元素')
        self.config_list = config_list

    def add_config(self, config):
        self.config_list.append(config)

    def to_xml(self, file_path):
        et = ET.Element('board_list')
        for config in self.config_list:
            et.append(config._get_element())
        pretty_xml(et, '\t', '\n')
        et_tree = ET.ElementTree(et)
        et_tree.write(file_path, encoding="utf-8", short_empty_elements=True)

    def get_db_config(self):
        config_list = GolaxyDBNewsConfigList()
        for config in self.config_list:
            obj = config.get_db_config()
            config_list.add_config(obj)
        return config_list


def from_xml(file_path):
    return GolaxyNewsConfig.from_xml(file_path)


def from_mysql(mysql, sql):
    return GolaxyDBNewsConfig.from_mysql(mysql, sql)


def from_json(data):
    return GolaxyDBNewsConfig.from_json(data)


if __name__ == '__main__':
    # MySQL ==> .xml
    # db = LengthConnectMySQL(host='10.20.18.100', user='root', passwd='123456', db='wde_golaxy', )
    # db_config = from_mysql(db, sql='select * from %s where cid=%s' % ('`news-crawler`', '11670696 or cid=11670697'))
    # config = db_config.get_config()
    # config.to_xml('c.xml')

    # .xml ==> MySQL
    # config = from_xml('b.xml')
    # db_config = config.get_db_config()
    # db_config.to_mysql(db, '`news-crawler`')

    d = [{'entry_url': 'http://www.cipg.org.cn/node_1005751.htm', 'site_name': '中国外文出版发行事业局',
          'board_name': '中国外文出版发行事业局-要闻动态', 'site_id': 46768, 'board_id': 12799191,
          'entry_url_regx': 'http://www.cipg.org.cn/node_1005751_%d.htm',
          'docurl_regex_yes': 'http://www.cipg.org.cn/\\d+-\\d+/\\d+/content_\\d+.htm', 'boardurl_max_pages': 10,
          'location': '中国', 'country': '北京', 'js_enabled_golaxy': 0, 'gfw_enabled_golaxy': 0,
          'accurate_extraction': 'eyJ0aXRsZV94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJUaXRsZVwiXSIsICJ0aXRsZV9yZWdleCI6ICIiLCAiY29udGVudF94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJDb250ZW50XCJdIiwgImNvbnRlbnRfcmVnZXgiOiAiIiwgInB1Ymxpc2hfdGltZV94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJ0aW1lXCJdIiwgInB1Ymxpc2hfcmVnZXgiOiAiNVkrUjViaUQ1cGUyNlplMDc3eWFLQzRxS2NLZ3dxRENvTUtnIiwgInVybF9maWx0ZXIiOiAiIiwgInNvdXJjZV94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJ0aW1lXCJdIiwgInNvdXJjZV9yZWdleCI6ICI1cDJsNXJxUTc3eWFLQzRxS1Z4eSIsICJzb3VyY2Vfc3RyaXAiOiAiXFwsJSw/LCBcciIsICJzb3VyY2VfZmlsdGVyIjogIiIsICJhdXRob3JfeHBhdGgiOiAiIiwgImF1dGhvcl9yZWdleCI6ICIiLCAiYXV0aG9yX3N0cmlwIjogIiIsICJhdXRob3JfZmlsdGVyIjogIiIsICJkZXRhaWxfanMiOiAwfQ==',
          'domain_url': 'org.cn'},
         {'entry_url': 'http://www.cipg.org.cn/node_1005751.htm', 'site_name': '中国外文出版发行事业局',
          'board_name': '中国外文出版发行事业局-要闻动态', 'site_id': 46768, 'board_id': 12799191,
          'entry_url_regx': 'http://www.cipg.org.cn/node_1005751_%d.htm',
          'docurl_regex_yes': 'http://www.cipg.org.cn/\\d+-\\d+/\\d+/content_\\d+.htm', 'boardurl_max_pages': 10,
          'location': '中国', 'country': '北京', 'js_enabled_golaxy': 0, 'gfw_enabled_golaxy': 0,
          'accurate_extraction': 'eyJ0aXRsZV94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJUaXRsZVwiXSIsICJ0aXRsZV9yZWdleCI6ICIiLCAiY29udGVudF94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJDb250ZW50XCJdIiwgImNvbnRlbnRfcmVnZXgiOiAiIiwgInB1Ymxpc2hfdGltZV94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJ0aW1lXCJdIiwgInB1Ymxpc2hfcmVnZXgiOiAiNVkrUjViaUQ1cGUyNlplMDc3eWFLQzRxS2NLZ3dxRENvTUtnIiwgInVybF9maWx0ZXIiOiAiIiwgInNvdXJjZV94cGF0aCI6ICIvL2RpdltAY2xhc3M9XCJ0aW1lXCJdIiwgInNvdXJjZV9yZWdleCI6ICI1cDJsNXJxUTc3eWFLQzRxS1Z4eSIsICJzb3VyY2Vfc3RyaXAiOiAiXFwsJSw/LCBcciIsICJzb3VyY2VfZmlsdGVyIjogIiIsICJhdXRob3JfeHBhdGgiOiAiIiwgImF1dGhvcl9yZWdleCI6ICIiLCAiYXV0aG9yX3N0cmlwIjogIiIsICJhdXRob3JfZmlsdGVyIjogIiIsICJkZXRhaWxfanMiOiAwfQ==',
          'domain_url': 'org.cn'}]
    c = GolaxyDBNewsConfig.from_json(d)
    print(c.__dict__)
