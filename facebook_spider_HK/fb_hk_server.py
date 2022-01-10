from flask import Flask,request
import json
import os
import re
from urllib.parse import unquote
import requests
try:
    from FacebookSpider_by.fb_spider import  FacebookSpider
except:
    from FacebookSpider_by.fb_spider import  FacebookSpider

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'

app = Flask(__name__)

@app.route('/facebook_spider', methods=['POST','GET'])

def fb_server():
    if request.method == 'GET':
        json_data = request.args.get('json_data')
    elif request.method == 'POST':
        json_data = request.form.get('json_data')

    seed_json = json.loads(json_data)
    name = seed_json["name"]
    facebook_url = seed_json["facebook_url"]
    fb_url = re.sub("https://www.facebook.com/","",facebook_url)
    screen_name = unquote(fb_url.replace("/",""))
    user_datas = name+"++"+screen_name
    print("111111111111111111")

    FacebookSpider(user_datas) 
    return "采集完成"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5580)
