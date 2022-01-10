import scrapy
from fake_useragent import UserAgent
from urllib.parse import urljoin
import copy
from oversea_website_find.items import OverseaWebsiteFindItem
ua = UserAgent(path=r".\Tools\useragent.json")

class nihaowangSpider(scrapy.Spider):

    name = 'world68'
    def __init__(self):
        self.headers = {"user-agent":ua.chrome}
        self.index_url = "http://www.world68.com/"


    def start_requests(self):
        entryurl = "http://www.world68.com/country.asp"
        request = scrapy.Request(entryurl, callback=self.country_parse,headers=self.headers)
        yield request

    def country_parse(self, response):
        country_list = response.xpath("//div[@class=\"content_all r\"]/dl/dd/a[1]")
        country_item = {}

        # ctype_list = [1]
        for country_data in country_list:
            country_item["country_url"] = urljoin(self.index_url,"".join(country_data.xpath("./@href").extract()))
            country_item["country"] = "".join(country_data.xpath("./text()").extract())
            url = country_item["country_url"]

            request = scrapy.Request(url, callback=self.board_parse,headers=self.headers)
            request.meta["country_item"] = copy.deepcopy(country_item)
            yield request

    def board_parse(self,response):

        country_item = response.meta["country_item"]
        board_list = {}
        board_list["country"] = country_item["country"]
        board_list_data = response.xpath("//div[@class=\"content_r_sort_c\"]/ul/li/a")
        board_in = ["政府机构", "军事国防", "新闻网站"]
        for board_data in board_list_data:
            url  = "".join(board_data.xpath("./@href").extract())
            board_name = "".join(board_data.xpath("./text()").extract())
            print(board_name)
            if board_name not in board_in:
                continue
            print(board_list)
            request = scrapy.Request(url, callback=self.list_parse, headers=self.headers)
            request.meta["board_list"] = copy.deepcopy(board_list)
            yield request


    def list_parse(self,response):
        board_list = response.meta["board_list"]
        next_page=0

        site_list = {}
        next_page += 1
        board_list["next_page"] = next_page
        site_list["country"] = board_list["country"]
        site_list_data = response.xpath("//div[@class=\"content_all_c\"]/dl/dt/a")
        for site_data in site_list_data:
            site_name = "".join(site_data.xpath("./text()").extract())
            site_list["site_name"] = site_name
            url = "".join(site_data.xpath("./@href").extract())
            request = scrapy.Request(url, callback=self.detail_parse, headers=self.headers)
            request.meta["site_list"] = copy.deepcopy(site_list)
            yield request

        next_data = response.xpath("//div[@class=\"page r\"]/a/@href").extract()
        page_url = response.url +"&page={}".format(board_list["next_page"])
        next_list_url = [urljoin("http://www.world68.com/list.asp?", next_url) for next_url in next_data]
        if page_url in next_list_url:
            request = scrapy.Request(page_url, callback=self.list_parse, headers=self.headers)
            request.meta["board_list"] = copy.deepcopy(board_list)
            yield request


    def detail_parse(self,response):
        site_list = response.meta["site_list"]
        item = OverseaWebsiteFindItem()
        item.init()
        item["country"] = site_list["country"]
        item["site_name"] = site_list["site_name"]
        try:
            item["site_url"] = "".join(response.xpath("//div[@class=\"url\"]/div[@class=\"url_r r\"]/a/@href").extract()).strip()
        except:
            item["site_url"] = ""
        yield item







