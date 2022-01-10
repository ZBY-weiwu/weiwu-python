# -*- coding:utf-8 -*-
from datetime import datetime
from elasticsearch_dsl import  Date,DocType,Text,Integer,analyzer,Completion,Keyword,Integer
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["192.168.1.20"])

class ActicleType(DocType):
      match_key = Text(analyzer ="ik_max_word")
      board_id = Integer()
      board_name = Text(analyzer ="ik_max_word")
      site_id = Integer()
      site_name = Text(analyzer ="ik_max_word")
      thread_id = Integer()
      like_count = Integer()
      dislike_count = Integer()
      publish_time = Integer()
      u_id = Integer()
      u_name = Text(analyzer ="ik_max_word")
      url = Keyword()
      reply_like_count = Keyword()
      reply_dislike_count = Keyword()
      title = Keyword()
      title_zh = Keyword()
      gather_time = Integer()
      reply_user = Keyword()
      lang = Keyword()
      reply_url = Keyword()

      class Meta:
            index = "jobbile"
            doc_type = "article"

if __name__=="__main__":
      ActicleType.init()
