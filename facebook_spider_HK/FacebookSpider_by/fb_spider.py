from facebook_scraper import get_posts
import time
import json,os
import configparser
import random
import urllib3
import requests
import sys,os
# base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# sys.path.append(base_path)
# try:
#     from facebook_spider_HK.Tools.facebook_package import format_pt,timeStamp_data,get_logger,str_to_timestamp,Get_pubtime,format_pubtime,Get_md5,proxies_list,getlabel,query_repeat
#     from facebook_spider_HK.Tools.translate_method import to_zh,langid_text
#     from facebook_spider_HK.Tools.pipelines import pipelines_es,file_out
#     from facebook_spider_HK.Tools.download_img import download_img
#     from facebook_spider_HK.Tools.nlp_server import NLP_server
# except:
from Tools.facebook_package import format_pt,timeStamp_data,get_logger,str_to_timestamp,Get_pubtime,format_pubtime,Get_md5,proxies_list,getlabel,query_repeat
# from Tools.download_img import download_img
from Tools.pipelines import pipelines_es,file_out
# from Tools.nlp_server import NLP_server
from Tools.translate_method import langid_text
# from Tools.translate_method import to_zh



urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
conf = configparser.ConfigParser()
parent_dir = os.path.dirname(os.path.abspath(__file__))
conf.read(parent_dir+"/../config/config.ini",encoding="utf-8")

logger_path = conf.get("LoggerPath","logger_path")
#logger_path2 = conf.get("LoggerPath","logger_path2")
logger1 = get_logger('zby', logger_path)
#logger2 = get_logger('lsj', logger_path2)

index = conf.get("es_config","_index")
StorageSwitch = conf.get("StorageSwitch","switch")
logger_switch = conf.get("LoggerPath","logger_switch")
download_img_switch = conf.get("StorageSwitch","download_img_switch")
#proxies_list = conf.get("Request","proxies_list")
spider_pages = int(conf.get("Number_Pages","pages"))


def FacebookSpider(user_data):
    print("user_data",user_data)
    if "++" in user_data:
        user_data_list = user_data.split("++")
        name = user_data_list[0]
        screen_name = user_data_list[1]
    else:
        name=""
        screen_name = user_data
    if len(screen_name)==0:
        return 

    a = 0
    print("screen_name:%s"%screen_name)
    #现设置2页采集
    for post in get_posts(account=screen_name, pages=spider_pages,extra_info=True,credentials=("lonelychen@live.cn","Lanchen870120")):
        a+=1
        # print("第[{}]条推文，内容是:{}".format(a,post))
        item={}
        item["person_name"] = name
        item["screen_name"] = screen_name
        item["post_id"] = post["post_id"]

        """
        #去重策略
        if query_repeat(index,item["post_id"]):
            logger1.info("数据去重")            
            continue
        """

        if post.get("shared_post_id"):

            item["repost_original_user_id"] = post.get("shared_user_id")#转发原文作的id
            item["repost_original_user_url"] = post.get("") #转发原文作的头像
            item["repost_original_user"] = post.get("shared_username")#转发原文作者
            item["repost_original_url"] = post.get("shared_post_url")#转发原链接
            item["repost_original_text"] = post.get("shared_text")#转发原帖

        else:
            item["repost_original_user_id"] = ""#转发原文作的id
            item["repost_original_user_url"] = ""#转发原文作的头像
            item["repost_original_user"] = ""#转发原文作
            item["repost_original_url"] = ""#转发原链接
            item["repost_original_text"] = ""#转发原帖

        item["url"] = post.get("post_url","")
        if not item["url"]:
            continue
        item["cont"] = post["text"]
        if not item["cont"] or len(item["cont"])<1:
            continue
        try:
            item["lang"] = langid_text(item["cont"])
        except:
            item["lang"] = "zh"
        # try:
        #     translate_cont = json.loads(to_zh(item["cont"]))
        #     item["cont_zh"] = translate_cont.get("cont","")
        # except:
        #     item["cont_zh"] = ""
        item["cont_zh"] = ""
        item["translate_source"] = ""
        # item["translate_source"] = translate_cont.get("translate_source","")

        if post["time"]:
            #pt = timeStamp_data(item["pub_time"])
            #format_data_pt = format_pt(pt)
            pt_format = post["time"]

            item["format_pubtime"] = pt_format.strftime("%Y-%m-%d %H:%M:%S")
        else:
            try:
                pub_time = int(Get_pubtime(item["url"]))
            except:
                logger1.info("时间获取失败")
                pub_time = int(time.time())
            item["pub_time"] = pub_time
            item["format_pubtime"] = format_pubtime(item["pub_time"])

        images = post["images"]
        if not images:
            item['images'] = []
        else:
            item['images'] = images
        item['gt'] = int(time.time())

        if len(item["cont_zh"])>0:
            content = item["cont_zh"]
        else:
            content = item["cont"]
        #附加-----
        # nlp_data=NLP_server(content).index()
        # nlp_obj = json.loads(nlp_data)
        # item["lkey"] = nlp_obj["lkey"]
        # item["vkey"] = nlp_obj["vkey"]
        # item["vrgn"] = nlp_obj["vrgn"]
        # item["vpers"] = nlp_obj["vpers"]
        # item["vorg"] = nlp_obj["vorg"]
        # item["abstr"] = nlp_obj["abstr"]
        # item["sent"] = nlp_obj["sent"]
        # item["sent_num"] = nlp_obj["sent_num"]
        item["gt"] = int(time.time()*1000)
        """
        label_content = {"content":content}
        label_data = getlabel(json.dumps(label_content))
        
        if len(label_data)>2:
            item["person"] = label_data[0]['label']
            item["negative_score"] = label_data[1]['score']
            item["tag"] = label_data[2]['label']

        if len(label_data)==2:
            item["person"] = label_data[0]['label']
            item["negative_score"] = label_data[1]['score']
            item["tag"] = []
        else:
            item["person"] = []
            item["negative_score"] = 0.0
            item["tag"] = []
        """
        if not post['video']:
            item['video'] = ""
        else:
            item["video"] = post["video"]
        if not post['video_thumbnail']:#视频缩略图
            item['video_thumbnail'] = ""
        else:
            item["video_thumbnail"] = post["video_thumbnail"]
        if not post['video_id']:
            item['video_id'] = ""
        else:

            item["video_id"] = post["video_id"]
        item["likes"] = post["likes"]
        item["comment_num"] = post["comments"]
        item["shares_num"] = post["shares"]
        if post.get("link")==None:
           item["share_url"]  = ""
        else:
            item["share_url"] = post.get("link","")
        item["user_id"] = post["user_id"]
        try:
            reactions= post["reactions"]#表情
        except:
            reactions=""
        # print("reactions:",reactions)
        try:
            item["expression_like"] = reactions["like"]#点赞
        except:
            item["expression_like"] = ""
        try:
            item["expression_anger"] = reactions["anger"]#愤怒
        except:
            item["expression_anger"] = ""
        try:
            item["expression_support"] = reactions["support"]#喜欢【抱心】
        except:
            item["expression_support"]=""
        try:
            item["expression_love"] = reactions["love"]  # 喜欢
        except:
            item["expression_love"] = ""
        try:
            item["expression_sorry"] = reactions["sorry"]#心碎
        except:
            item["expression_sorry"] =""
        try:
            item["expression_haha"] = reactions["haha"]#大笑
        except:
            item["expression_haha"] = ""
        try:
            item["expression_wow"] = reactions["wow"]#惊讶
        except:
            item["expression_wow"] = ""  # 惊讶

        item["w3_fb_url"] = post.get("w3_fb_url","")

        item_data = json.dumps(item,ensure_ascii=False)
        if logger_switch:
            logger1.info("name:[{}],post_id:[{}]".format(item["person_name"],item["post_id"]))
            #logger2.info("name:[{}],post_id:[{}]".format(item["person_name"],item["post_id"]))
        if StorageSwitch:
            pipelines_es(item_data,item["post_id"])
            file_out(item)

if __name__ == '__main__':
    pass



