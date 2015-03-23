__author__ = 'anom'
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector

class stock_r(BaseSpider):
    name = "stock_r"
    allowed_domains = ["http://www.topstockresearch.com"]
    start_urls = ["http://www.topstockresearch.com/PriceVolumeSurprisers/TopGainersIndianStockMarket.html"]
    def parse(self, response):
        sel = HtmlXPathSelector(response)
        sites = sel.xpath('//tr/td/text()').extract()
        items = []
        for item in sites:
            item = item.encode("utf-8")
            item = item.strip(" ")
            item = item.strip('\r\n')
            item = item.strip('\xc2\xa0')
            items.append(item)
            items = filter(None,items)
        items_list = [items[x:x+7] for x in range(0, len(items),7)]
        print items_list[49]