# -*- coding: UTF-8 -*-
from langdetect import detect
from langdetect import DetectorFactory



def get_langtect(cont):

    DetectorFactory.seed = 0
    lang_type = (detect(text=cont))  # zh-cn
    if lang_type =="zh-cn":
        lang_type ="zh"
    elif lang_type =="et":
        lang_type == "en"
    print(lang_type)
    return lang_type

if __name__ == '__main__':
    get_langtect("奥术大师多")

