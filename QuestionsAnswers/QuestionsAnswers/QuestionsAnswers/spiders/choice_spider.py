# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/8/4



class abstractFactory(object):
    def __init__(self):
        pass

    def getFactory(self, wenda_id):
        if wenda_id == 1:
            from .baiduzhidao_spider import Baiduzhidao_Spider
            return Baiduzhidao_Spider()

        elif wenda_id == 2:
            from ._360wenda_spider import  wenda_360Spider
            return wenda_360Spider()

        elif wenda_id == 3:
            from .souguowenda_spider import  souguowenda_Spider
            return souguowenda_Spider()

        elif wenda_id == 4:
            from .wukongwenda_spider import wukongwenda_Spider
            return wukongwenda_Spider()

