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
        titles = sel.xpath("//a[@class='bl_12']/b/text()").extract()
        items = []
        head = []
        i = 0
        for item in sites:
            item = item.encode("utf8")
            item = item.strip()
            item = item.split('\t')
            if item != ['']:
                items.append(item)
        items_list = [items[x:x+7] for x in range(0, len(items),7)]
        time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        for title in titles:
            title = title.encode("utf8")
            head.append(title)
        for item_ in items_list:
            self.cursor.executemany("""INSERT INTO money_control (COMPANY,
LTP,Change_,VOLUME,BUY_PRICE,
SELL_PRICE,BUY_QTY,SELL_QTY,date)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
ON DUPLICATE KEY UPDATE
LTP = values(LTP),
Change_ = values(Change_),
VOLUME = values(VOLUME),
BUY_PRICE = values(BUY_PRICE),
SELL_PRICE = values(SELL_PRICE),
BUY_QTY = values(BUY_QTY),
SELL_QTY = values(SELL_QTY),
date = values(date)
 """
, [(head[i],item_[0],item_[1],item_[2],item_[3],item_[4],item_[5],item_[6],time),
             ])

            self.conn.commit()
            i = i+1
