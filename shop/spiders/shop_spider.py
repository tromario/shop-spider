import logging
import scrapy
from shop.items import ShopItem

logger = logging.getLogger('mycustomlogger')

class ShopSpider(scrapy.Spider):
    name = 'shop'
    base_url = "https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?p="

    def start_requests(self):
        urls = [
            'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?p=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.get_pages)

    def get_pages(self, response):
        print("user-agent: %s" % self.settings.get('USER_AGENT'))

        count_pages = int(response.xpath("string(.//*[@class=' item edge']/@data-page-number)").extract_first())
        page = 1
        while page <= count_pages:
            url = self.base_url + str(page)
            yield response.follow(url, callback=self.parse)
            page += 1

    def parse(self, response):
        page = response.url.split("/")[-2]

        filename = 'page-%s.html' % page
        with open("tmp/" + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for product in response.xpath(".//*[@data-id='catalog-item']"):
            item = ShopItem()
            item["url"] = product.xpath(".//*[@data-product-param='name']/@href").extract_first()
            item["page"] = response.url
            item["name"] = product.xpath(".//*[@data-product-param='name']/h3/text()").extract_first()
            item["price"] = float(product.xpath(".//*[@data-product-param='price']/@data-value").extract_first())
            yield item