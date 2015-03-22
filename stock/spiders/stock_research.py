__author__ = 'anom'
from scrapy.spider import BaseSpider
from scrapy.selector import Selector

class stock_r(BaseSpider):
    name = "stock_r"
    allowed_domains = ["http://www.topstockresearch.com"]
    start_urls = ["http://www.topstockresearch.com/PriceVolumeSurprisers/TopGainersIndianStockMarket.html"]