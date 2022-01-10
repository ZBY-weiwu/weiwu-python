import json
# 字典格式转str
def cookie_to_dic(cookie):
    cookie = json.dumps(cookie)
    return {item.split('=')[0]: item.split('=')[1] for item in cookie.split('; ')}

def get_coockie_dict(cookie):
    cookie = cookie_to_dic(cookie)
    cookie_dic = {}
    for i in cookie.split('; '):
        cookie_dic[i.split('=')[0]] = i.split('=')[1]
    return cookie_dic

"""************json转回原生cookies*************"""

def get_dict_cookie(login_cookie):

    a = ""
    for i in login_cookie:
        a = a+i+"="+login_cookie[i]+"; "

    return a




if __name__ == '__main__':
    login_cookie = {'c_user': '100052975728068', 'datr': 'MB_nYOU375B6iyWgl_d0A5U8',
                    'fr': '1ggLy0oSx2diAsCBz.AWXZya0DawhZ0blaOSf1x-_3mN4.Bg5x8w.zS.AAA.0.0.Bg5x8x.AWVD40DdIWU',
                    'sb': 'MB_nYNkGWz8KeRBXi6urqOUc', 'xs': '5%3A6w14gs_kh8Bs9A%3A2%3A1625759537%3A-1%3A15002'}

    print(get_dict_cookie(login_cookie))