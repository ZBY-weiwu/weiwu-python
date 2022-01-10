import scrapy
from fake_useragent import UserAgent
from urllib.parse import urljoin
import copy
from oversea_website_find.items import OverseaWebsiteFindItem
ua = UserAgent(path=r".\Tools\useragent.json")

class nihaowangSpider(scrapy.Spider):

    name = 'nihaowang'
    def __init__(self):
        self.headers = {"user-agent":ua.chrome}
        self.index_url = "http://site.nihaowang.com/"


    def start_requests(self):
        entryurl = "http://site.nihaowang.com/country.aspx"
        request = scrapy.Request(entryurl, callback=self.parse_board,headers=self.headers)
        yield request

    def parse_board(self, response):
        country_list = response.xpath("//*[@id=\"Country_nei\"]/div[@class=\"m10\"]/div[@class=\"gr6\"]/a")
        board_list = {}
        ctype_list = [1,2,3,12,45,47,49,50,51,52,53,55,56,60,61]
        # ctype_list = [1]
        for country_data in country_list:
            board_list["country_url"] = urljoin(self.index_url,"".join(country_data.xpath("./@href").extract()))
            board_list["country"] = "".join(country_data.xpath("./@title").extract())
            print(board_list)
            for ctype_data in ctype_list:
            # if True:
                # 正式地址
                url = board_list["country_url"]+"&ctype={}".format(ctype_data)
                # # 测试 用这个地址
                # url = board_list["country_url"]
                request = scrapy.Request(url, callback=self.list_parse,headers=self.headers)
                request.meta["board_list"] = copy.deepcopy(board_list)
                yield request

    def list_parse(self,response):

        board_list = response.meta["board_list"]
        site_list = {}
        site_list["country"] = board_list["country"]
        list_data = response.xpath("//*[@id=\"wrap_left\"]/div[@class=\"picture_lie\"]//h1/a[2]")
        for site_data in list_data:
            url  = "".join(site_data.xpath("./@href").extract())
            site_list["site_name"] = "".join(site_data.xpath("./@title").extract())
            url = urljoin(self.index_url,url)
            print(site_list)
            request = scrapy.Request(url, callback=self.detail_parse, headers=self.headers)
            request.meta["site_list"] = copy.deepcopy(site_list)
            yield request

        next_data = "".join(response.xpath("//*[@id=\"wrap_left\"]/div[@class=\"hxsc-pager\"]/a[@title=\"下一页\"]/@href").extract())
        if len(next_data)>=1:
            next_page = urljoin(self.index_url, next_data)
            request = scrapy.Request(next_page, callback=self.list_parse, headers=self.headers)
            request.meta["board_list"] = copy.deepcopy(board_list)
            yield request


    def detail_parse(self,response):
        site_list = response.meta["site_list"]
        item = OverseaWebsiteFindItem()
        item.init()
        item["country"] = site_list["country"]
        item["site_name"] = site_list["site_name"]
        try:
            item["site_url"] = response.xpath("//div[@class=\"st_txt\"]//a/text()").extract()[0].strip()
        except:
            item["site_url"] = ""
        yield item







