#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author: origin
# email: 1194542196@qq.com
# date: 2021/4/9

import time
import urllib.parse

from gevent import monkey

monkey.patch_all()
from selenium import webdriver
from flask import request
from gevent.pywsgi import WSGIServer
from flask import Flask
from flask_bootstrap import Bootstrap
from selenium.common.exceptions import InvalidSessionIdException, WebDriverException
from selenium.webdriver import ChromeOptions

BROWSER_RUN = False


class SeleniumDynamicLoading(object):
    def __init__(self, *args, **kwargs):
        self._args = args
        self._kwargs = kwargs
        self.browser = None
        self.start_browser()

    def start_browser(self):
        chrome_options = ChromeOptions()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        self.browser = webdriver.Chrome(options=chrome_options, *self._args, **self._kwargs)

    def get_page(self, url, wait=1):
        try:
            self.browser.execute_script('window.open()')
            self.browser.switch_to.window(self.browser.window_handles[-1])
            self.browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
                "source": """
                                    Object.defineProperty(navigator, 'webdriver', {
                                      get: () => false
                                    })
                                  """
            })
            self.browser.get(url)
            time.sleep(wait)
            page_source = self.browser.page_source
            if len(self.browser.window_handles) >= 11:
                self.quit()
                self.start_browser()
            return page_source
        except (InvalidSessionIdException, WebDriverException):
            self.quit()
            self.start_browser()
        except Exception as e:
            print(type(e), '#' * 1000)
            self.quit()

    def quit(self):
        self.browser.quit()

    def close(self):
        self.browser.close()


app = Flask(__name__)
bootstrap = Bootstrap(app=app)


@app.route('/selenium/origin/v1', methods=['GET'])
def hello_world():
    global BROWSER_RUN
    args = request.args.to_dict()
    url, wait = args.pop('url'), args.pop('wait')
    if not wait:
        wait = 3
    else:
        wait = int(wait)
    url = '%s&%s' % (url, urllib.parse.urlencode(args))
    if request.method == 'GET':
        while True:
            if not BROWSER_RUN:
                try:
                    BROWSER_RUN = True
                    result = browser.get_page(url, wait)
                    if result:
                        return result
                    else:
                        return 'Null'
                except Exception:
                    return 'busy'
                finally:
                    BROWSER_RUN = False
            else:
                time.sleep(1)


if __name__ == '__main__':
    browser = SeleniumDynamicLoading()
    server = WSGIServer(('0.0.0.0', 8085), app)
    server.serve_forever()