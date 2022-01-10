from w3lib import html
import requests
from lxml import etree

res = requests.get("http://www.example.com/")
response = etree.HTML(res.content)
temp = response.xpath('//body') # 返回值为一个列表

doc = etree.tostring(temp[0])   # 将定位到的元素转成str，即获得源码

# 以上代码只是为了获取body的源码，与函数演示无关

result = html.remove_tags(doc) # 标签全部去除
print(result)
