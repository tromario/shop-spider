# coding=utf-8
import datetime
import logging
import scrapy
from shop.items import ShopItem

logger = logging.getLogger('mycustomlogger')


class MarkethotSpider(scrapy.Spider):
    name = 'markethot.ru'
    base_url = 'https://markethot.ru'
    search = '/catalog/search?sort=price&order=asc&query=%s'

    def __init__(self, *args, **kwargs):
        super(MarkethotSpider, self).__init__(**kwargs)
        self.query=kwargs['query']
        self.history=kwargs['history']

    def start_requests(self):
        yield scrapy.Request(url=self.base_url + self.search % (self.query), callback=self.parse)

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
        for product in response.xpath('//*[@class="product-item\n                                                                                                        "]'):
            item = ShopItem()
            item['resource'] = self.name
            item['history'] = self.history
            item["url"] = self.base_url + product.xpath('.//a[@class="pi-inner"]/@href').extract_first()

            name = product.xpath('.//div[@class="product-description"]/text()').extract_first()
            name = name.strip()
            item["name"] = name

            item["price"] = float(product.xpath('.//span[@class="price"]/text()').extract_first())
            item['created_date'] = datetime.datetime.now()
            yield item
