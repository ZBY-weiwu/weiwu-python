import requests,re

def time_ps(url):
    url = re.sub("facebook.com", "m.facebook.com", url)
    proxies = {"http":"http://192.168.1.44:1081","https":"https://192.168.1.44:1081"}
    headers = {'cookie': 'datr=2VuhXz65PvhcSg5pO1BoTedW; sb=2luhX21PNMORg06RNCZ3aH7s; c_user=100052975728068; spin=r.1003054394_b.trunk_t.1607131521_s.1_v.2_; m_pixel_ratio=1; xs=9%3AqwZRx7I7EUdR5A%3A2%3A1604410966%3A16303%3A15002%3A%3AAcUCfMIqRvLcf7Ihgt6Ov8lL4Aqanh2PwIXmmkH-iw; fr=0Kmf56XvEgKsuyKju.AWXqBhosY1ntc6KbhOIvTIk_yJw.BfkotT.UN.AAA.0.0.Bfy0gI.AWUBwGVqklg; wd=2543x1248', 'origin': 'https://m.facebook.com', 'referer': 'https://m.facebook.com/story.php?story_fbid=2415788165239169&id=627043070780363', 'sec-fetch-dest': 'empty', 'sec-fetch-mode': 'cors', 'sec-fetch-site': 'same-origin', 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36', 'x-requested-with': 'XMLHttpRequest', 'x-response-format': 'JSONStream'}
    resp = requests.get(url,headers=headers,proxies = proxies)
    body = resp.text
    # print(body)
    time_format = "".join(re.findall("__tn__=-R\"><abbr>(.*?)</abbr>",body))
    time_a = ["小时", "分钟", "秒"]
    time_add = False
    for time_b in time_a:
        if time_b in time_format:
            time_add = True
            break
    if time_add:
        time_format += "前"
    pt_time = str_to_timestamp(time_format)
    print("pt_time:", pt_time)
    return pt_time

if __name__ == '__main__':
    url = "https://facebook.com/story.php?story_fbid=1844081665756780&id=491399324358361"
    time_ps(url)
