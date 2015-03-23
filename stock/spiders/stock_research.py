__author__ = 'anom'
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import MySQLdb
import datetime

class stock_r(BaseSpider):
    name = "stock_r"
    allowed_domains = ["http://www.topstockresearch.com"]
    start_urls = ["http://www.topstockresearch.com/PriceVolumeSurprisers/TopGainersIndianStockMarket.html"]
    def parse(self, response):
        self.conn = MySQLdb.connect(user='root', passwd='2361250', db='stock', host='localhost', charset="utf8", use_unicode=True)
        self.cursor = self.conn.cursor()
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
        time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

        for item_ in items_list:
            self.cursor.execute("""INSERT INTO stock_list (name,sector,current_price,previous_price,days_high,days_low,volume,date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""", (item_[0],item_[1],item_[2],item_[3],item_[4],item_[5],item_[6],time))
            self.conn.commit()
