#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import re
import json
import pymysql.cursors
import pymysql

import os


def select_url(url):
    # url = "https://mp.sohu.com/profile?xpt=ZWR1c29odUBzb2h1LmNvbQ==&_f=index_pagemp_1"
    db = pymysql.connect("192.168.1.20", "root", "tianji@123", "hk", charset="utf8")
    cursor = db.cursor()
    select_url = "SELECT * FROM `personnel_base_v1` WHERE url='%s';" % url
    if cursor.execute(select_url):
        print("url已存在")
        db.commit
        return True
    else:
        return False


def update_datal(name, name_en, image_url, occupation, image_data, education, brief_introduction):
    db = pymysql.connect("192.168.1.20", "root", "tianji@123", "hk", charset="utf8")
    select_url = "SELECT * FROM `personnel_base_v1` WHERE name ='%s';" % name
    cursor = db.cursor()
    if cursor.execute(select_url):
        # db.commit
        thestand_name_en = 'update personnel_base_v1 set thestand_name_en="%s" where name="%s";' % (name_en, name)
        cursor.execute(thestand_name_en)
        thestand_occupation = 'update personnel_base_v1 set thestand_occupation="%s" where name="%s";' % (occupation, name)
        cursor.execute(thestand_occupation)
        thestand_brief_introduction = 'update personnel_base_v1 set thestand_brief_introduction="%s" where name="%s";' % (brief_introduction, name)
        cursor.execute(thestand_brief_introduction)
        thestand_picture = 'update personnel_base_v1 set thestand_picture="%s" where name="%s";' % (image_data, name)
        cursor.execute(thestand_picture)
        thestand_education = 'update personnel_base_v1 set thestand_education="%s" where name="%s";' % (education, name)
        cursor.execute(thestand_education)
        db.commit()
        print("更新成功---------------:name%s\n"%name)
    else:
        insertsql = """insert into personnel_base_v1 (name, thestand_name_en, thestand_occupation,thestand_picture,thestand_education,thestand_brief_introduction) VALUES ('%s','%s','%s','%s','%s','%s')""" % (
            name, name_en, occupation, image_data, education, brief_introduction)
        if True:
            cursor.execute(insertsql)
            db.commit()

        print("插入成功---------------:name%s\n"%name)
    db.close()
