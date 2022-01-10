# -*- coding:utf-8 -*-
#!/usr/bin/python3
# author: zby
# email: by951118@163.com
# date: 2021/7/28

import re
import random
import time
import requests
import json
from lxml import etree
from requests_html import HTMLSession
from urllib.parse import urljoin

import sys
import time
import json
import pymysql
import contextlib

@contextlib.contextmanager
def mysql(host='10.20.18.100', port=3306, user='golaxy', passwd='123456', db='app_config',
          charset='utf8'):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    try:
        yield cursor
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == '__main__':

    outputfile=sys.argv[1]
    bContinue=True
    seed_empty=True
    boardinfo=[]
    with mysql() as cursor:
        row_count = cursor.execute("SELECT * FROM wenda-crawl ORDER BY updata_time asc limit 10")
        row_contents = cursor.fetchall()
        ids = []
        for item in row_contents:
            dictObj={
                'site_id':                int(item['site_id']),
                'site_name':              item['site_name'],
                'board_id' :             item['board_id'],
                'board_name':            item['site_id']+'-'+item['board_name'],
                'entryurl' :            item['entryurl'],
                'config' :              item['config']
            }
            assert (1 == update_row_count)
            #schedule_lts
            bFirst=True
            with mysql() as cursor_schedule_select:
                row_count_select = cursor_schedule_select.execute("SELECT * from schedule_info where board_id= "+str(item['board_id']))
                row_contents_select = cursor_schedule_select.fetchall()
                for item_select in row_contents_select:
                    info=item_select['info']
                    bFirst=False
                    if len(info)>1:
                        infoobject=json.loads(info)
                        info_one_item=[]
                        time_local = time.localtime(time.time())
                        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                        if len(infoobject)>10:
                            info_one_item.append(dt)
                            infoobject=info_one_item
                        else:
                            infoobject.append(dt)
                        update_row_count = cursor_schedule_select.execute("update schedule_info set info ='%s' where board_id=%d" % (json.dumps(infoobject),item['board_id']))
                if bFirst:
                    with mysql() as cursor_schedule_select_first:
                        info_one_item=[]
                        time_local = time.localtime(time.time())
                        dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
                        info_one_item.append(dt)
                        update_row_count = cursor_schedule_select_first.execute("insert into  schedule_info (site_id,board_id ,info) values(%d,%d,'%s')" % (item['site_id'],item['board_id'],json.dumps(info_one_item)))

        with open(outputfile,'w') as json_file:
            json.dump(boardinfo,json_file,ensure_ascii=False)
            sys.exit()