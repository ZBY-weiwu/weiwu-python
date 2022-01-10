# -*- coding:utf-8 -*-
# author: weiwu
# email: by951118@163.com
# date: 2021/7/28
from currency_module.DBConnect.py_db import PgDB
from currency_module.Tools.by_package import get_past_times


class GetTask():

    def __repr__(self)->str:
        return "Extract task!"

    @classmethod
    def get_user_behavior_task(cls)->list:
        past_time  = get_past_times(5)
        fetchall_datas = PgDB._fetchall("SELECT * FROM sjzt_wcm_website_zjs WHERE create_time_stamp>={}  ORDER BY update_time LIMIT 10".format(past_time))
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
            # PgDB.update_set(table="sjzt_wcm_website_zjs",id=id)
            list_item.append(item)
        return list_item

if __name__ == '__main__':
    GetTask().get_user_behavior_task()

