# -*- coding:utf-8 -*-
from datetime import datetime
from elasticsearch_dsl import  Date,DocType,Text,Integer,analyzer,Completion,Keyword,Integer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["192.168.1.20"])
"""
版本号说明
elasticsearch          5.5.3
elasticsearch-dsl      5.2.0
"""
class ArticleType(DocType):
      match_key = Text(analyzer ="ik_max_word")
      board_id = Integer()
      board_name = Text(analyzer ="ik_max_word")
      site_id = Integer()
      site_name = Text(analyzer ="ik_max_word")
      thread_id = Integer()
      like_count = Integer()
      dislike_count = Integer()
      publish_time = Integer()
      publish_time_format = Text(analyzer ="ik_max_word")
      u_id = Integer()
      u_name = Text(analyzer ="ik_max_word")
      url = Keyword()
      reply_like_count = Keyword()
      reply_dislike_count = Keyword()
      title = Keyword()
      title_zh = Keyword()
      gather_time = Integer()
      lang = Keyword()

      class Meta:
            index = "lihkg"
            doc_type = "article"

if __name__=="__main__":
      ActicleType.init()
