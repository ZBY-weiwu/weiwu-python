import re

href = "https://www.afpbb.com/xinhuanet/-/3377455cn"
a = False
Hot_Pixel=['eastmoney.com',".cn", 'xinhuanet', 'news.xhby.net', 'pravda.ru', 'chinaqw', 'en.nhandan.com.vn', 'news.ycwb.com', 'huanqiu.com', 'sina', 'sohu', 'asahi.com', 'ap.org', 'rodong.rep.kp']
for i in Hot_Pixel:
    if re.findall(i,href):
        a = True

if a:
    print("跳过")