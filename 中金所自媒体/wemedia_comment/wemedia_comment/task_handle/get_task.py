# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28
from wemedia_comment.currency_module.DBConnect.py_db import PgDB
import time
class GetTask():
    # 评论使用的是根据update_time2更新调度的
    def __repr__(self)->str:
        return "Extract task!"

    @classmethod
    def get_user_wemediacomment_task(cls)->list:
        # sjzt_wcm_website_zjs_copy1 测试数据库
        # fetchall_datas = PgDB._fetchall("SELECT * FROM sjzt_wcm_website_zjs_copy1 WHERE site_id in (7010,33798,25953) ORDER BY update_time2 LIMIT 10;")
        fetchall_datas = PgDB._fetchall("SELECT * FROM sjzt_wcm_website_zjs WHERE site_id in (7010) ORDER BY update_time2 LIMIT 10;")
        list_item = []
        for data in fetchall_datas:
            item={}
            id = data[9]
            item["site_id"] = data[8]
            item["site_name"] = data[0]
            item["url"] = data[1]
            item["board_id"] = data[2]
            item["detail_id"] = data[3]
            item["detail_url"] = data[7]
            update_time = int(time.time())
            update_sql = "UPDATE {table} SET update_time2={update_time} WHERE id='{id}'".format(table="sjzt_wcm_website_zjs",update_time=update_time,id=id)
            PgDB.update_set(table="sjzt_wcm_website_zjs",id=id,update_sql=update_sql)
            list_item.append(item)
        return list_item

if __name__ == '__main__':
    GetTask.get_user_wemediacomment_task()

