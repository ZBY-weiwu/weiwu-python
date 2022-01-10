#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import re
import MySQLdb
import json

reload(sys)
sys.setdefaultencoding('utf-8')

import os


db = MySQLdb.connect("10.20.18.100","golaxy","123456","app_config" , charset="utf8")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()
"""
sql = "SELECT * FROM app_config"
try:
   # 执行SQL语句
   cursor.execute(sql)
   # 获取所有记录列表
   results = cursor.fetchall()
   for row in results:
      fname = row[0]
      lname = row[1]
      age = row[2]
      sex = row[3]
      income = row[4]
      # 打印结果
      print fname#, lname, age, sex, income )
except:
   print "Error: unable to fecth data"

"""

file_dir="../seed/"
def file_name(file_dir):
    index1=1
    for root, dirs, files in os.walk(file_dir):

        for sub in files:
            file = open("../seed/"+sub)
            while True:
                line = file.read()
                if not line:
                    break
                line=line.strip()
                data=json.loads(line)
                for sub in data:
                    appname= sub['appname']
                    appid=sub['appid']
                    boardid=sub['boardid']
                    boardname=sub['boardname']
                    entryurl=sub['entryurl']
                    config=sub['config']
                    index1=index1+1
                    insertsql="insert into app_config_test(appid,appname,boardid,boardname,entryurl,config) VALUES (%d,'%s',%d,'%s','%s','%s')"%(appid,appname.encode('utf-8','ignore'),boardid,boardname.encode('utf-8','ignore'),entryurl.encode('utf-8','ignore'),config)
                    try:
                        #print insertsql
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        cursor.execute(insertsql)
                        db.commit()
                    except:
                        pass
                        #db.rollback()
    db.close()
file_name(file_dir)

