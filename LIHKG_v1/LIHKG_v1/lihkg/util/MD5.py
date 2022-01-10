#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import hashlib
class MD5:
    def __init__(self):
        pass
    def getMD5(self, s):
        md5 = hashlib.md5()
        md5.update(s.encode('utf-8'))
        return  md5.hexdigest()

