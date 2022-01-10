# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/28


import redis   # 导入redis 模块

r = redis.Redis(host='10.1.101.53', port=6379, db=1,decode_responses=True)
r.set('name', 'runoob')  # 设置 name 对应的值
print(r['name'])
