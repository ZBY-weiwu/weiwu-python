import configparser
import urllib3,requests
from Scheduler_scrapy.facebook_scheduler import scheduler_running
import time
import os, sys
parent_dir = os.path.dirname(os.path.abspath(__file__))

urllib3.disable_warnings()
requests.packages.urllib3.disable_warnings()
conf = configparser.ConfigParser()
conf.read(parent_dir+"/config/config.ini",encoding="utf-8")
# conf.read(r"../",encoding="utf-8")

Scheduling_switch = conf.get("Scheduler_Time","Scheduling_switch")
scheduler_time = int(conf.get("Scheduler_Time","Scheduling_period"))


scheduler_running()
# while Scheduling_switch:
#     time.sleep(scheduler_time)
#     scheduler_running()
