# -*- coding:utf-8 -*-
from datetime import datetime
from elasticsearch_dsl import  Date,DocType,Text,Integer,analyzer,Completion,Keyword
from elasticsearch_dsl.connections import connections
connections.create_connection(hosts=["10.20.8.1.26"])

"""
版本号说明
elasticsearch          5.5.3
elasticsearch-dsl      5.2.0
"""

class Article_reply(DocType):
      match_key = Text(analyzer ="ik_max_word")
      reply_match_key = Text(analyzer ="ik_max_word")
      like_count = Integer()
      dislike_count = Integer()
      user_id = Integer()
      images = Text(analyzer ="ik_max_word") 
      reply_pt = Integer()
      reply_pt_format = Text(analyzer ="ik_max_word")
      reply_user = Text(analyzer ="ik_max_word")
      reply_url = Keyword()
      reply_content = Text(analyzer ="ik_max_word")
      reply_content_zh = Text(analyzer ="ik_max_word")
      title = Text(analyzer ="ik_max_word")
      title_zh = Text(analyzer ="ik_max_word")
      msg_num = Integer()

      class Meta:
            index = "lihkg_reply"
            doc_type = "comment"

if __name__=="__main__":
      Article_reply.init()
