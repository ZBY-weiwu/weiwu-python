import requests
import re
from FB_spider.un_name import username,password
from FaceBookLogin import Facebook_Login
fb_login = Facebook_Login()


def Fb_login_cookie():
    get_cookie = fb_login.login(username,password)
    print(get_cookie.headers)
    print(requests.utils.dict_from_cookiejar(get_cookie.cookies))
    return get_cookie

# 100052975728068





def index_page():


    proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
    # Fb_login_cookie().proxies = proxies
    # proxies = proxies
    resp = Fb_login_cookie().get("https://www.facebook.com/chungchunwong",proxies = proxies)
    body =resp.text
    next_link = "".join(re.findall("/profile/timeline/stream/\?cursor.*?\",proximity_pages",body))
    print("body:",body)
    print("next_link:",next_link)
    # data = {"fb_dtsg": "",
    #         "jazoest": "",
    #         "lsd": "",
    #         "__dyn": "",
    #         "__csr": "",
    #         "__req": "60",
    #         "__a": "",
    #         "__user": "100052975728068"}
    #
    # session
    # resq = session.post

"""第二页"""
def GetProxy():


        headers = {"Host": "m.facebook.com",
     "Connection": "keep-alive",
     "Content-Length": "421",
     "X-FB-LSD": "lq3dmAcBXcD9x6kwNR_xl9",
     "Content-Type": "application/x-www-form-urlencoded",
     "X-Requested-With": "XMLHttpRequest",
     "sec-ch-ua-mobile": "?0",
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
     "X-Response-Format": "JSONStream",
     "sec-ch-ua": "\" Not;A Brand\";v=\"99\", \"Google Chrome\";v=\"91\", \"Chromium\";v=\"91\"",
     "Accept": "*/*",
     "Origin": "https",
     "Sec-Fetch-Site": "same-origin",
     "Sec-Fetch-Mode": "cors",
     "Sec-Fetch-Dest": "empty",
     "Referer": "https",
     "Accept-Language": "zh-CN,zh;q=0.9",
     "Cookie": "sb=OMm-YJvgaMRoH0q_lUahyZGd; datr=Rcm-YHBQSPzUAvapJ15QHjlO; locale=zh_TW; c_user=100052975728068; spin=r.1004113327_b.trunk_t.1626319839_s.1_v.2_; dpr=1.375; m_pixel_ratio=1.25; xs=10%3AxHkde9jZN4OWfQ%3A2%3A1626319821%3A-1%3A15002%3A%3AAcVB16Nj_KNCL-LQZ0lSFq_sBVn05Vu0HHvEfWal0g; fr=1KH5IqYjbjmYBInfV.AWWVGK_nt2vikqAaMGTO64XQpis.Bg7-YJ.RY.AAA.0.0.Bg7-YJ.AWUL6uQWqAs; x-referer=eyJyIjoiL2hvbWUucGhwIiwiaCI6Ii9ob21lLnBocCIsInMiOiJtIn0%3D; wd=1519x722"}
        data ={"fb_dtsg": "AQG0fVBFuEWcuio%3A10%3A1626319821",
     "jazoest": "22026",
     "lsd": "lq3dmAcBXcD9x6kwNR_xl9",
     "__dyn": "1KQEGiFo525Ujwh8-t0BBBgS5UqxKcwRwAxu3-UcodUbEdEc8uKewhEfolxK4ohx21vwdK4olwYw9a260gq1gCwSxu0BU3JxO1ZxObwro7ifw5lxyeKdwGwFU6i12wsU52229wcq0C9EdE2IzUuw9O1Aw9-2i1qw8W1uwa-10w4cwp8Gdw",
     "__csr": "",
     "__req": "60",
     "__a": "AYkng3yjPQTiHLou1DKSdLaicS7KRMF00pQ0Vld0tljvyMdaKNmW_XIljWVArjsnPavP0YgSh5VROsG36qPr_nLwmcVBjzyXWyyqbI2MOFKcyQ",
     "__user": "100052975728068"}
        data["__dyn"] = ""
        session.cookies.update(cokie_data)
        resp = session.post("https://m.facebook.com/profile/timeline/stream/?cursor=AQHRfNthbn0jyR0JeAlRgvOMnnKipG7mVB0rfCavXeXC6vtoztZxk8nFL4Y5T2CxzE2yPkVKAS4KTlJb3oHx91UW913X7I3jjPSJeuLp5gB-Yoe-2dT2HBqtofHmFVJr8BBR&start_time=-9223372036854775808&profile_id=100000405556511&replace_id=u_4q_0_1r ",headers=headers,data=data,proxies=proxies)
        text = resp.text
        print(text)

if __name__ == '__main__':
    # GetProxy()
    index_page()
    pass