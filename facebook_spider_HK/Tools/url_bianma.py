from urllib import parse
from urllib import request
str1 = 'haha哈哈'
str2 = parse.quote(str1)   #quote()将字符串进行编码
print(str2)                #str2=haha%E5%93%88%E5%93%88
str3 = parse.unquote("Trump%20OR%20Clinton%20since%3A2006-12-13%20until%3A2007-09-07") #解码字符串
print(str3)                #str3=haha哈哈