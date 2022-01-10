# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/7/12

import base64
import hashlib


class CodeUtils(object):
    """
    编码相关工具
    """

    @classmethod
    def b64encode(cls, s, encoding='utf-8'):
        return base64.b64encode(s.encode(encoding)).decode(encoding)

    @classmethod
    def b64decode(cls, bs, decoding='utf-8'):
        return str(base64.b64decode(bs), decoding)


"""
    进制表示时，字符表示对应关系时，0-9代表0-9，a-z代表10-35，
    A-Z代表36-61，更高进制需要行指定符号
"""
BASE_MODEL = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
              'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
              'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
              'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D',
              'E', 'F', 'G', 'H', 'I', 'G', 'K', 'L', 'M', 'N',
              'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
              'Y', 'Z']


class TransformUtils(object):
    """
    转换相关工具
    """

    @classmethod
    def to10base(cls, from_num, from_base=10):
        if not isinstance(from_num, str):
            from_num = str(from_num)
        if 2 <= from_base <= 36:
            return int(from_num, from_base)

    @classmethod
    def from10base(cls, from_num, to_base=36):
        return ((from_num == 0) and "0") or (
                cls.from10base(from_num // to_base, to_base).lstrip("0") +
                BASE_MODEL[from_num % to_base])

    @classmethod
    def base2base(cls, from_num, from_base=10, to_base=36):
        from_num = cls.to10base(from_num, from_base)
        return cls.from10base(from_num, to_base)


class EncryptUtils(object):
    """
    加密相关工具
    """

    @classmethod
    def md5(cls, s, encoding='utf-8'):
        _md5 = hashlib.md5()
        _md5.update(s.encode(encoding))
        return _md5.hexdigest()

    @classmethod
    def kaiser(cls, s, key=0):
        """
        凯撒加密
        :param s: 字母字符串
        :param key: 偏移key
        :return:
        """
        cs = list()
        for c in s:
            cs.append(chr(ord(c) + key))
        return ''.join(cs)


class DecryptUtils(object):
    @classmethod
    def kaiser_by_key(cls, s, key=0):
        """
        凯撒解密
        :param s: 密文字母字符串
        :param key: 偏移key，和加密相反
        :return:
        """
        return EncryptUtils.kaiser(s, key)
