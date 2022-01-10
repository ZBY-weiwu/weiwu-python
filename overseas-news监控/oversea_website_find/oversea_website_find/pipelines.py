# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import csv
from .items import OverseaWebsiteFindItem
from scrapy.exporters import JsonItemExporter
from scrapy.exporters import JsonLinesItemExporter


class CsvFilePipeline:

    def __init__(self):
        self.f = open("./output/oversea_site.csv", "w", encoding="utf-8",newline='')
        headers = ['country', 'site_name','site_url']
        self.f_csv = csv.DictWriter(self.f, headers)
        self.f_csv.writeheader()

    def process_item(self, item, spider):
        if isinstance(item, OverseaWebsiteFindItem):
            self.f_csv.writerow(item)
            return item

    def close(self, spider):
        self.f.close()


class JsonFilePipeline:
    def __init__(self):
        self.json_file = open('./output/oversea_site.json', 'wb')
        self.json_exporter = JsonLinesItemExporter(self.json_file, ensure_ascii=False, encoding='UTF-8')
        self.json_exporter.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, OverseaWebsiteFindItem):
            self.json_exporter.export_item(item)
            return item

    def close_spider(self, spider):
        self.json_exporter.finish_exporting()
        self.json_file.close()


