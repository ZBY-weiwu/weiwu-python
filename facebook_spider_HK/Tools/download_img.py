# coding: utf8
import requests,os
from fake_useragent import UserAgent
import re
ua = UserAgent()
def download_img(img_url, personal_name,md5_url, proxy_ip):
    
    img_suffix = ".jpg" 
    header = {"User-Agent":ua.chrome} 
    #r = requests.get(img_url, headers=header, stream=True,proxies=proxy_ip)
    a = 0
    try:
        while True:
            if a>3:
                break
            try:
                r = requests.get(img_url, headers=header, proxies=proxy_ip)
                if r.status_code == 200:
                    File_Path='output/fb_img/'+personal_name+"/"
                    if not os.path.exists(File_Path):
                        os.makedirs(File_Path)
                    open(File_Path+md5_url+img_suffix, 'wb').write(r.content) # 将内容写入图片
                    print("下载图片成功:",md5_url+img_suffix)
                else:
                    download_img
                break
            except:
               a+=1 
               print("下载图片重连[%d]次数"%a)
    except:
        return

if __name__ == '__main__':
    # 下载要的图片
    img_url = "http://pbs.twimg.com/profile_images/895251621382434818/c3mNgz5T_normal.jpg"
    download_img(img_url,{'http': 'http://192.168.1.44:1081', 'https': 'https://192.168.1.44:1081'})
