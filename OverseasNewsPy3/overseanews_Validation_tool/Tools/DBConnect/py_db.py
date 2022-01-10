# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/11/10

import os
import time
from psycopg2 import extras as ex
import psycopg2
import configparser

parent_dir = os.path.dirname(os.path.abspath(__file__))
conf = configparser.ConfigParser()
conf.read("config\config.ini", encoding="utf-8")
# conf.read(os.getcwd()+"\currency_module\config.ini", encoding="utf-8")



class PgDB():

    def __repr__(self):
        print("Pg 数据操作")

    @classmethod
    def Pg_connect(cls)->object:
        hosts = conf.get("Pg", "hosts")
        port = conf.get("Pg", "port")
        user = conf.get("Pg", "user")
        password = conf.get("Pg", "password")
        database = conf.get("Pg", "database")
        conn = psycopg2.connect(database=database, user=user, password=password, host=hosts, port=port)
        return conn

    # 单条插入
    @classmethod
    def Pg_write(cls,sql, params=None):
        conn  = cls.Pg_connect()
        cursor = conn.cursor()
        # 方法一
        # sql = """INSERT INTO student (num, name) VALUES (%s, %s)"""
        # params = (101, 'zszxz')

        # 方法二
        # sql = """INSERT INTO student (num, name) VALUES (%(num)s, %(name)s)"""
        # params = {'num': 102, 'name': 'zszxz'}
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        conn.close()

    # 批量插入
    @classmethod
    def Pg_list_write(cls,sql, datalist):
        # datalist 是个list,里面是数组形式
        # sql = """INSERT INTO sjzt_wcm_website_zjs (id,site_id, site_name,url,board_id,detail_id,update_time,create_time,create_time_stamp,detail_url,sjzt_wcm_websites,update_time2) VALUES %s"""
        conn = cls.Pg_connect()
        cursor = conn.cursor()
        ex.execute_values(cursor, sql, datalist, page_size=10000)
        conn.commit()
        conn.close()


    @classmethod
    def update_set(cls,table,id=None,update_sql=None): #只传入id就只更新update_time

        if update_sql:
            update_sql =update_sql
        elif id:
            update_time = int(time.time())
            update_sql = "UPDATE {table} SET update_time={update_time} WHERE id='{id}'".format(table=table,update_time=update_time,id=id)
        else:
            print("Error:id,update_sql meanwhile Null")
        conn = cls.Pg_connect()
        cursor = conn.cursor()
        cursor.execute(update_sql)
        conn.commit()
        cursor.close()
        conn.close()

    # 异步内存插入
    @classmethod
    def Pg_StringIO_write(cls,sql):
        pass

    # 去重查询
    @classmethod
    def Whether_exist(cls,sql):
        # PgDB.whether_exist("SELECT * FROM sjzt_wcm_users WHERE profile_url ='https://xueqiu.com/u/1191579772'")
        conn = cls.Pg_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        select_value = cursor.fetchone()
        conn.commit()
        conn.close()
        return select_value

    # 取任务
    @classmethod
    def _fetchall(cls, sql):
        # PgDB.whether_exist("SELECT * FROM sjzt_wcm_website WHERE profile_url =''")
        conn = cls.Pg_connect()
        cursor = conn.cursor()
        cursor.execute(sql)
        select_value = cursor.fetchall()
        conn.commit()
        conn.close()
        return select_value


if __name__ == '__main__':
    # EsDB.get_data()
    PgDB.Whether_exist("SELECT * FROM sjzt_wcm_users WHERE profile_url ='https://xueqiu.com/u/1191579772'")