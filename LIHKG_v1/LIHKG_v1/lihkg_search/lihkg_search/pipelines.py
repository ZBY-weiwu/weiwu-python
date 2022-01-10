# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter, JsonLinesItemExporter
from lihkg_search.items import DetailItem
from lihkg_search.items import reply_Item
from util.langIden import get_langtect


class LihkgPipeline:
    def process_item(self, item, spider):
        if isinstance(item, DetailItem):
            d = {}
            d['match_key']            = item['match_key']
            d['kw']                   = item['key_wrod']
            d['t']                    = item['title']
            d['t_zh']                 = item['title_zh']
            d['reply_like_count']     = item['reply_like_count']
            d['reply_dislike_count']  = item['reply_dislike_count']
            d['bn']                   = item['board_name']
            d['u_id']                 = item['u_id']
            d['u_name']               = item['u_name']
            d['u']                    = item['url']
            d['like_count']           = item['like_count']
            d['reply_like_count']     = item['reply_like_count']
            d['reply_dislike_count']  = item['reply_dislike_count']
            #item_content = item['content']
            item_content = item_content.replace('<br>','\n')
            item_content = item_content.replace('<br/>','\n')
            #item_content = item_content.replace('</P>','\n')
            #item_content = item_content.replace('<P>','\n')
            #item_content = item_content.replace('<p>','\n')
            #item_content = item_content.replace('</p>','\n')
            #d['c']      = item_content
            #if len(d['c'])   < 1:
            #    print ("content<1")
            #    return
            #d['pic']    = item['lpic']
            d['gt']     = item['gather_time']
            if len(str(item['publish_time'])) == 10:
                d['pt'] = int(item['publish_time'])*1000
            elif len(str(item['publish_time'])) == 13:
                d['pt'] = int(item['publish_time'])
            elif len(str(item['publish_time'])) <= 0:
                d['pt'] = item['gather_time']
            elif len(str(item['publish_time'])) != 10 and len(str(item['publish_time'])) != 10:
                d['pt'] = item['gather_time']
            #content = re.sub('{IMG:\d+}', "", item["content"], 0, re.S|re.M|re.I)
            #d['lng']   = get_langtect(content)
            d['lng']   = "zh" 
            d['sn']     = "LIHKG"
            self.exporter.export_item(d)
        return item
    def open_spider(self, spider):
        self.detailfile = open("output/article.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.detailfile, ensure_ascii=False)
    def close_spider(self, spider):
        self.detailfile.close()
        #return item

class ElasticsearchPipeline(object):
    def process_item(self,item,spider):
        item.save_to_es()
        return item
         
class Lihkg_reply:
    def process_item(self, reply_item, spider):
        if isinstance(reply_item, reply_Item):
            d = {}
            d['match_key']            = reply_item['match_key']
            d['kw']             = reply_item['key_word']
            d['reply_match_key']      = reply_item['reply_match_key']
            d['u_id']                 = reply_item['user_id']
            d['images']               = reply_item['images']
            d['reply_user']           = reply_item['reply_user']
            d['msg_num']              = reply_item['msg_num']
            d['reply_c']              = reply_item['reply_content']
            d['reply_c_zh']           = reply_item['reply_content_zh']
            d['reply_pt']             = reply_item['reply_pt']
            d['reply_url']            = reply_item['reply_url']
            d['like_count']           = reply_item['like_count']
            d['dislike_count']        = reply_item['dislike_count']
            item_content              = reply_item['reply_content']
            item_content              = item_content.replace('<br>','\n')
            item_content              = item_content.replace('<br/>','\n')
            item_content              = item_content.replace('<br />','\n')
            item_content              = item_content.replace('</P>','\n')
            item_content              = item_content.replace('</p>','\n')
            d['reply_c']              = item_content
            self.exporter.export_item(d)
        return reply_item
    def open_spider(self, spider):
        self.detailfile = open("output/reply.json", 'wb')
        self.exporter = JsonLinesItemExporter(self.detailfile, ensure_ascii=False)
    def close_spider(self, spider):
        self.detailfile.close()
class ElasticsearchPipeline_Reply(object):
    def process_item(self,reply_item,spider):
        reply_item.save_to_es()
        return reply_item
