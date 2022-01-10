# -*- coding:utf-8 -*-
import os
import sys
import time
s= 0
while True:
    s += 1
    os.system("./start.sh lihkg_v1")
    time.sleep(3600)
    print ("******************************已执行完[%d]次"%s)
