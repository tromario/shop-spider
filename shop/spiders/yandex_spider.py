# coding=utf-8
import datetime
import json
import logging
import re

import scrapy
from shop.items import ShopItem

logger = logging.getLogger('mycustomlogger')


class YandexSpider(scrapy.Spider):
    name = 'market.yandex.ru'
    base_url = 'https://market.yandex.ru'
    search = '/search?text=%s&onstock=1&local-offers-first=1&how=aprice&page=%d'

    def __init__(self, *args, **kwargs):
        super(YandexSpider, self).__init__(**kwargs)
        self.query = kwargs['query']
        self.history = kwargs['history']

    def start_requests(self):
        yield scrapy.Request(url=self.base_url + self.search % (self.query, 1), callback=self.get_pages,
                             dont_filter=True)

    def get_pages(self, response):
        print("user-agent: %s" % self.settings.get('USER_AGENT'))

        pagination = response.xpath('.//*[contains(@class, "n-pager i-bem")]/@data-bem').extract_first()
        json_pagination = json.loads(pagination)

        count_pages = json_pagination['n-pager']['pagesCount']
        if count_pages != '':
            count_pages = int(count_pages)
        else:
            count_pages = 1

        for page in range(1, count_pages + 1):
            url = self.base_url + self.search % (self.query, page)
            yield response.follow(url, callback=self.parse)

    def parse(self, response):
        for product in response.xpath('//*[contains(@class, "n-snippet-card2 i-bem b-zone b-spy-visible")]'):
            item = ShopItem()
            item['resource'] = self.name
            item['history'] = self.history

            product_bem = product.xpath('.//@data-bem').extract_first()
            json_product_bem = json.loads(product_bem)
            product_type = json_product_bem['n-snippet-card2']['type']
            if product_type == 'offer':
                url = 'https:' + product.xpath('.//*[contains(@class, "link n-link_theme_blue")]/@href').extract_first()
            else:
                url = self.base_url + product.xpath(
                    './/*[contains(@class, "link n-link_theme_blue")]/@href').extract_first()

            item["url"] = url

            name = product.xpath('.//*[contains(@class, "link n-link_theme_blue")]/@title').extract_first()
            name = name.strip()
            item["name"] = name

            price = product.xpath('.//*[@class="price"]/text()').extract_first()
            if price is None:
                continue
            price = re.sub('[^\d]', '', price)
            item["price"] = float(price)

            item['created_date'] = datetime.datetime.now()
            yield item
