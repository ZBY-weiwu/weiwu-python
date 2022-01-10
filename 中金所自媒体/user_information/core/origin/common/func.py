# -*- coding:utf-8 -*-
# author: kusen
# email: 1194542196@qq.com
# date: 2021/8/26


def get_future_value(obj, key, default=None):
    if hasattr(obj, key):
        return getattr(obj, key)
    else:
        if default:
            return default
        else:
            raise KeyError('Not set the expect value!')