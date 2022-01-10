#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import hashlib
class MD5:
    def __init__(self):
        pass
    def getMD5(self, s):
        md5 = hashlib.md5()
        if isinstance(s, unicode):
            md5.update(s.encode('utf-8'))
        else:
            md5.update(s)
        return  md5.hexdigest()

