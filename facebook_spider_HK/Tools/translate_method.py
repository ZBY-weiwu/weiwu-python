import requests
from urllib.parse import quote
import time
import langid
import socket
import socks

def langid_text(text):
    lang_data = langid.classify(text)
    try:
        lang_cont = list(lang_data)[0]
    except:
        lang_cont ="zh"
    return lang_cont


def to_zh(text):#翻译英文转中文{多语种}
    socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1089)
    socket.socket = socks.socksocket
    time.sleep(1)
    get_data = quote(text)
    a=0
    while True:
        resp = requests.get("http://10.1.101.51:5590/translate?data_cont={}".format(get_data))
        if resp.status_code==200:
            body = resp.text
            return body


if __name__ == '__main__':
    print(to_zh("test format"))
    print(to_zh("紡織及製衣界"))
    #print(langid_text("紡織及製衣界"))
