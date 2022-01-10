# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/8/4
class abstractFactory(object):
    def __init__(self):
        pass


    def getFactory(self, comment_id):

        if comment_id == 7010:
            from .guba_comment_spider import DongfangcaifugubaCommentSpider
            return DongfangcaifugubaCommentSpider()
        if comment_id == 33798:
            from .toutiao_comment_spider import JinritoutiaoCommentSpider
            return JinritoutiaoCommentSpider()
        if comment_id == 25953:
            from .xueqiu_comment_spider import XueqiuCommentSpider
            return XueqiuCommentSpider()


