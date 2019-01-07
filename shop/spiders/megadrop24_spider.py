# coding=utf-8
import datetime
import logging
import scrapy
from shop.items import ShopItem

logger = logging.getLogger('mycustomlogger')


class Megadrop24Spider(scrapy.Spider):
    name = 'megadrop24.ru'
    base_url = 'https://megadrop24.ru'
    search = '/search/page%d?query=%s&minprice=1&maxprice=20000&submit='

    def __init__(self, *args, **kwargs):
        super(Megadrop24Spider, self).__init__(**kwargs)
        self.query=kwargs['query']
        self.history=kwargs['history']

    def start_requests(self):
        yield scrapy.Request(url=self.base_url + self.search % (1, self.query), callback=self.get_pages)

    def get_pages(self, response):
        print("user-agent: %s" % self.settings.get('USER_AGENT'))

        count_pages = response.xpath('string(.//*[@class="pagination"]/li[last()])').extract_first()
        if count_pages != '':
            count_pages = int(count_pages)
        else:
            count_pages = 0

        for page in range(count_pages + 1):
            url = self.base_url + self.search % (page, self.query)
            yield response.follow(url, callback=self.parse)

    def parse(self, response):
        for product in response.xpath('//*[@class="product-item"]'):
            item = ShopItem()
            item['resource'] = self.name
            item['history'] = self.history
            item["url"] = self.base_url + product.xpath('.//h3/a/@href').extract_first()
            item["name"] = product.xpath('.//h3/a/text()').extract_first()
            item["price"] = float(product.xpath('.//*[@class="pi-price"]/text()').extract_first())
            item['created_date'] = datetime.datetime.now()
            yield item
