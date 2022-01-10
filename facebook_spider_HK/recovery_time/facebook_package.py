import re
import random
import json
import requests
import time, datetime
import logging  # 引入logging模块
import os.path
import time
import configparser
import urllib3,requests
import dateutil.parser
import warnings

def format_pt(pt_data):
    #'Sat Sep 05 23:49:53 +0000 2020'
    month_data_all = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    time_datas =  pt_data.split(" ")
    pt_month_data = time_datas[1]
    pt_month = month_data_all.get(pt_month_data)
    pt_day = time_datas[2]
    pt_time = time_datas[3]
    pt_years = time_datas[5]
    pub_time = pt_years+"-"+pt_month+"-"+pt_day+" "+pt_time
    # print(pub_time)
    return pub_time


#时间戳转时间
def format_pubtime(timeStamp):
    timeArray = time.localtime(timeStamp)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return otherStyleTime

#时间转时间戳
def timeStamp_data(pt_data):
    #'Sat Sep 05 23:49:53 +0000 2020'
    pub_time = format_pt(pt_data)
    timeArray = time.strptime(pub_time, "%Y-%m-%d %H:%M:%S")
    timeStamp = int(time.mktime(timeArray))*1000
    # print(timeStamp)
    return timeStamp

#获取标签负面信息

def getlabel(data):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","Content-Type": "application/json","Accept": "application/json"}
    reponse = requests.post("http://192.168.1.20:8080/v2/label/getLable_28",headers=headers,data=data)
    resp = json.loads(reponse.text)
    return resp

#去重策略
def query_repeat(channel,id):
    return False
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36","Accept": "application/json"}
    reponse = requests.get("http://192.168.1.20:8090/api/v2/web/browse/duplicateByChannelAndId?channel=%s&id=%s"%(channel,id),headers=headers)
    resp = json.loads(reponse.text)
    data = resp['data']
    return data

#日志
def get_logger(logger_name, log_file, level=logging.INFO):
    l = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s : %(message)s', "%Y-%m-%d %H:%M:%S")
    fileHandler = logging.FileHandler(log_file, mode='a')
    fileHandler.setFormatter(formatter)
    l.setLevel(level)
    l.addHandler(fileHandler)

    return logging.getLogger(logger_name)
    


#时间抽取转换
def str_to_timestamp(date):
    dt = datetime.datetime.now()
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    now = int(time.time())
    isParse = False
    #if not "前" in date:
    #    isParse=True
    m = None
    #print("------------data:",date)
    if not isParse:
        m = re.search('(\d+)\s*秒前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))
    if not isParse:
        m = re.search('(\d+)\s*分钟前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60
    if not isParse:
        m = re.search('(\d+)\s*小时前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60
    if not isParse:
        m = re.search('(\d+)\s*天前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60*24
    if not isParse:
        m = re.search('(\d+)\s*个月前', date, re.M|re.I)
        if m:
            isParse = True
            now = now - int(m.group(1))*60*60*24*30
    if not isParse:
        m = re.search('今天\s*(\d+):(\d+)', date, re.M|re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                hour = m.group(1)
            if m.group(2):
                minute = m.group(2)
            s = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
            d =  dateutil.parser.parse(s,fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search('(\d{2,4})?年?(\d{1,2})月(\d{1,2})日\s*(\d{1,2})?[:时]?(\d{1,2})?[:分]?(\d{1,2})?', date, re.M|re.I)
        if m:
            isParse = True
            hour = 0
            minute = 0
            second = 0
            if m.group(1):
                year = m.group(1)
                if len(str(year))==2:
                    year = "20"+year
            if m.group(2):
                month = m.group(2)
            if m.group(3):
                day = m.group(3)
            if m.group(4):
                hour = m.group(4)
            if m.group(5):
                minute = m.group(5)
            if m.group(6):
                second = m.group(6)
            s = str(year)+"-"+str(month)+"-"+str(day)+" "+str(hour)+":"+str(minute)+":"+str(second)
            d =  dateutil.parser.parse(s,fuzzy=True)
            now = int(time.mktime(d.timetuple()))
    if not isParse:
        m = re.search( r'(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}-\d{1,2} \d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2}:\d{1,2})|(\d{4}/\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{1,2}/\d{1,2} \d{1,2}:\d{1,2})|(\d{4}-\d{1,2}-\d{1,2}\w\d{1,2}:\d{1,2}:\d{1,2})', date, re.M|re.I)
        if m:
            isParse = True
            date = m.group()
            d =  dateutil.parser.parse(date,fuzzy=True)
            t = int(time.mktime(d.timetuple()))
            if t < now:
                now = t
    return now

def Get_pubtime(url):
    url = re.sub("facebook.com", "m.facebook.com", url)
    #proxies = {"http":"http://192.168.1.10:1081","https":"https://192.168.1.10:1081"}
    proxies = random.choice(proxies_list)
    headers = {'cookie': 'datr=2VuhXz65PvhcSg5pO1BoTedW; sb=2luhX21PNMORg06RNCZ3aH7s; c_user=100052975728068; spin=r.1003054394_b.trunk_t.1607131521_s.1_v.2_; m_pixel_ratio=1; xs=9%3AqwZRx7I7EUdR5A%3A2%3A1604410966%3A16303%3A15002%3A%3AAcUCfMIqRvLcf7Ihgt6Ov8lL4Aqanh2PwIXmmkH-iw; fr=0Kmf56XvEgKsuyKju.AWXqBhosY1ntc6KbhOIvTIk_yJw.BfkotT.UN.AAA.0.0.Bfy0gI.AWUBwGVqklg; wd=2543x1248', 'origin': 'https://m.facebook.com', 'referer': 'https://m.facebook.com/story.php?story_fbid=2415788165239169&id=627043070780363', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 'x-requested-with': 'XMLHttpRequest', 'x-response-format': 'JSONStream'}
    resp = requests.get(url,headers=headers,proxies = proxies)
    body = resp.text
    if "story_fbid" in url:
        time_format = "".join(re.findall("__tn__=-R\"><abbr>(.*?)</abbr>",body))
    if "watch" in url:
        time_format = "".join(re.findall("",body))
        
    time_a = ["小时","分钟","秒"]
    time_add = False
    for time_b in time_a:
        if time_b in time_format:
            time_add=True
            break
    if time_add:
        time_format+="前"
        time_format = time_format.replace(" ","")
        time_format = time_format.replace("\t","")
    #print("time_format:",time_format)
    pt_time = str_to_timestamp(time_format)
    return pt_time

def Get_md5(url):
    import hashlib
    a = hashlib.md5(url.encode())
    md5_str = a.hexdigest()
    return md5_str

proxies_list = [{'http': 'http://192.168.1.44:1081', 'https': 'https://192.168.1.44:1081'},
                {'http': 'http://192.168.1.49:1081', 'https': 'https://192.168.1.49:1081'},
                {'http': 'http://192.168.1.50:1081', 'https': 'https://192.168.1.50:1081'},
                {'http': 'http://192.168.1.51:1081', 'https': 'https://192.168.1.51:1081'},
                {'http': 'http://192.168.1.52:1081', 'https': 'https://192.168.1.52:1081'},
                {'http': 'http://192.168.1.53:1081', 'https': 'https://192.168.1.53:1081'},
                {'http': 'http://192.168.1.54:1081', 'https': 'https://192.168.1.54:1081'},
                {'http': 'http://192.168.1.55:1081', 'https': 'https://192.168.1.55:1081'},
                {'http': 'http://192.168.1.56:1081', 'https': 'https://192.168.1.56:1081'},
                {'http': 'http://192.168.1.57:1081', 'https': 'https://192.168.1.56:1081'}]

if __name__ == '__main__':
    #pass
    #facebook时间抽取特殊案例
    url = "https://facebook.com/story.php?story_fbid=1844081665756780&id=491399324358361"
    #视频
    url = "https://facebook.com/watch?v=247011066752049"
    #图片
    url = "https://facebook.com/carmenkamanlau/photos/a.107623683904883/448559449811303/"
    url = "https://facebook.com/story.php?story_fbid=450697845889660&id=101221711235980"
    print("pub_time:",int(Get_pubtime(url)))
    print(format_pubtime(Get_pubtime(url)))
    data = {"content":"深水埗民主派區議員對實施禁足令之聲明》 經過多日的吹風後，政府終於在昨日凌晨四時宣佈引用《預防及控制疾病規例》第599J章，圍封佐敦指定區域，但卻引伸一連串問題，包括不少當區市民在禁足令宣佈前已撤離，這些人有機會將病毒帶離當區，同時政府事先也沒有和區議會溝通，令到居民接收訊息混亂，有些市民在離開家門口才知悉被禁足，不能上班，完全無所適從；同時區內的商店在疫情打擊下已奄奄一息，禁足令的實行更完全暫停周區的的經濟活動。 林鄭在昨日宣稱封區不會做一次，不少人已傳言下一步就是要封閉深水埗指定區域，頓時令深水埗區民人心惶惶，令社區無故被標籤，尤如死城無異。深水埗區與佐敦不同，現階段完全沒有科學證明或個案顯示疫情在深水埗區內擴散，而無論在楓樹街的流動採樣站或其他檢測站均沒有檢測到本區有大規模的隱形傳播者。 誠然，我們認為病毒散播的源頭很大機會和區內舊樓的舊式渠管有關，這也是早前不少大廈不同單位交叉感染的原因，政府現時首要工作，必是處理區內的污水渠道改裝或亂駁問道，渠管問題不會在禁足令完成後自動解決，當帶病毒者返回當區後，疫情也會繼續散播。 我們再重申，政府在處理封關、豁免檢疫和群組爆發多次把關不力，才令疫情出現發展至第四波到今天仍未收拾。深水埗及油尖旺多劏房，有不少基層市民居住，他們除了面對疫情威脅，還受政府多項限制社交活動措施所限，令生活百上加斤。但政府的抗疫行動偏偏越做越錯，越錯越做；現時打算封鎖整個地區的措施，亦只會造成污名化，令居民不得安寧，扼殺地區經濟，乃至日後生活上的各樣困難。現階段政府要做的，就是全方面檢測舊區的喉管(尤其三無大廈)，找出病毒所在，對症下藥，才是治本之道。 前車之鑒，深水埗區議會立場絕不希望政府有機會將某些深水埗位置成為禁區。 聯署人： 深水埗區議員 楊彧、伍月蘭、周琬雯、鄒穎恒、覃德誠、何啟明、江貴生、劉家衡、劉偉聰、利瀚庭、李文浩、李俊晞、李炯、李庭豐、麥偉明、冼錦豪、譚國僑、徐溢軒、衞煥南、黃傑朗、袁海文"}
    getlabel(json.dumps(data))
    
    # format_pt('Sat Sep 05 23:49:53 +0000 2020')
    # timeStamp_data('Sat Sep 05 23:49:53 +0000 2020')
    # time_division('2019-01-01','2020-01-07',"Trump")
    # console_out("logger_test")
    #2020年11月27日 14:00 和 1月11日 12:20
    #print(str_to_timestamp("2020年11月27日 14:00"))
    #print(str_to_timestamp("1月11日 12:20"))

    #print("test:",query_repeat("hk_facebook_test","439203037433439"))
