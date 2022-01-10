# -*- coding:utf-8 -*-
# author: golaxy
# email: by951118@163.com
# date: 2021/10/13

from scrapy.cmdline import execute
# from task_scheduling import WemediaCommentTaskScheduling
#
# if __name__ == '__main__':
#     TaskScheduling = WemediaCommentTaskScheduling()
#     TaskScheduling.download_main(

def scrapy_main():
    execute(["scrapy", "crawl", "wemedia_comment"])

if __name__ == '__main__':
    scrapy_main()