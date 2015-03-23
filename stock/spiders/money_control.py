__author__ = 'jovin'
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import MySQLdb
import datetime

class stock_r(BaseSpider):
    name = "money"
    allowed_domains = ["http://www.moneycontrol.com"]
    start_urls = ["http://www.moneycontrol.com/terminal/index_v1.php?index=4"]
    def parse(self, response):
        self.conn = MySQLdb.connect(user='root', passwd='2361250', db='stock', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
        sel1 = HtmlXPathSelector(response)
        sel = sel1.select("//table[@class='mcTrmnlTbl']")
        sites = sel.xpath('.//tr/td/text()').extract()
        title = sel.xpath("//a[@class='bl_12']/b/text()").extract()
        items = []
        new_items = []
        for item in sites:
            item = item.encode("utf8")
            item = item.strip()
            item = item.split('\t')
            if item != ['']:
                items.append(item)
        print items
