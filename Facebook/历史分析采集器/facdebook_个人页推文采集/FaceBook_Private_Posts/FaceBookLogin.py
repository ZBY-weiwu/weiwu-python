# -*- coding:utf-8 -*-
# author: zby
# email: by951118@163.com
# date: 2021/7/8
from urllib.parse import urljoin
import warnings
import re
from functools import partial
from typing import Iterator, Union
import json
import requests


from requests import RequestException
from requests_html import HTMLSession


class Facebook_Login:


    have_checked_locale = False

    default_headers = {
        'Accept-Language': 'en-US,en;q=0.5',
        "Sec-Fetch-User": "?1",
        "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36",
    }

    def __init__(self):
        self.PC_index_url ="https://www.facebook.com/"
        self.m_index_url = "https://m.facebook.com/"


        session = HTMLSession()
        session.proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}
        session.headers.update(self.default_headers)

        self.session = session
        self.session.proxies = {'http': 'http://127.0.0.1:10809', 'https': 'https://127.0.0.1:10809'}


    def get(self, url, **kwargs):
        print(url)

        print("111")
        if not url.startswith("http"):
            url = urljoin(self.m_index_url, url)
        response = self.session.get(url=url,timeout=5, **kwargs)
        response.html.html = response.html.html.replace('<!--', '').replace('-->', '')
        response.raise_for_status()
        self.check_locale(response)
        if "cookie/consent-page" in response.url:
            print("112")
            response = self.submit_form(response)
        if (
            response.url.startswith(self.m_index_url)
            and "noscript" not in response.html.html
            and self.session.cookies.get("noscript") != "1"
        ):
            warnings.warn(
                f"Facebook served mbasic/noscript content unexpectedly on {response.url}"
            )
        title = response.html.find("title", first=True)
        not_found_titles = ["page not found", "content not found"]
        temp_ban_titles = [
            "you can't use this feature at the moment",
            "you can't use this feature right now",
            "you’re temporarily blocked",
        ]
        if title:
            pass
        return response


    def submit_form(self, response, extra_data={}):
        action = response.html.find("form", first=True).attrs.get('action')
        url = urljoin(self.m_index_url, action)
        elems = response.html.find("input[name][value]")
        data = {elem.attrs['name']: elem.attrs['value'] for elem in elems}
        data.update(extra_data)
        response = self.session.post(url, data=data)
        return response

    def check_locale(self, response):
        print(444)
        if self.have_checked_locale:
            return
        match = re.search(r'"IntlCurrentLocale",\[\],{code:"(\w{2}_\w{2})"}', response.text)
        if match:
            print(555)
            locale = match.groups(1)[0]
            if locale != "en_US":
                warnings.warn(f"Locale detected as {locale} - for best results, set to en_US")
            self.have_checked_locale = True


    def login(self, email: str, password: str):
        response = self.get(self.m_index_url)
        response = self.submit_form(
            response, {"email": email, "pass": password, "_fb_noscript": None}
        )
        login_error = response.html.find('#login_error', first=True)

        if login_error:
            print("账号密码错误")

        if "Login approval needed" in response.text or "checkpoint" in response.url:
            print("检查账号是否被封，或锁定")
            return "检查账号是否被封，或锁定"
        if 'c_user' not in self.session.cookies:
            print("Login unsuccessful")
        print("Login successful")
        print(requests.utils.dict_from_cookiejar(self.session.cookies))
        # return (requests.utils.dict_from_cookiejar(self.session.cookies))
        # print(self.session)
        return self.session
        # return self.session.cookies

if __name__ == '__main__':
    # login_cookie 为正确的cookie
    login_cookie = {'c_user': '100052975728068', 'datr': 'MB_nYOU375B6iyWgl_d0A5U8', 'fr': '1ggLy0oSx2diAsCBz.AWXZya0DawhZ0blaOSf1x-_3mN4.Bg5x8w.zS.AAA.0.0.Bg5x8x.AWVD40DdIWU', 'sb': 'MB_nYNkGWz8KeRBXi6urqOUc', 'xs': '5%3A6w14gs_kh8Bs9A%3A2%3A1625759537%3A-1%3A15002'}
    print(Facebook_Login().login("by951118@163.com","qq1161081779"))