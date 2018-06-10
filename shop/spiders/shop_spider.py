import logging
import scrapy
from shop.items import ShopItem

logger = logging.getLogger('mycustomlogger')

class BrickSetSpider(scrapy.Spider):
    name = 'shop'

    def start_requests(self):
        urls = [
            'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print("user-agent: %s" % self.settings.get('USER_AGENT'))

        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open("tmp/" + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        for brickset in response.xpath(".//*[@data-id='catalog-item']"):
            # PIECES_SELECTOR = './/dl[dt/text() = "Pieces"]/dd/a/text()'
            # MINIFIGS_SELECTOR = './/dl[dt/text() = "Minifigs"]/dd[2]/a/text()'
            # IMAGE_SELECTOR = 'img ::attr(src)'
            # yield {
            #     'name': brickset.css(NAME_SELECTOR).extract_first()
            #     # 'pieces': brickset.xpath(PIECES_SELECTOR).extract_first(),
            #     # 'minifigs': brickset.xpath(MINIFIGS_SELECTOR).extract_first(),
            #     # 'image': brickset.css(IMAGE_SELECTOR).extract_first(),
            # }
            item = ShopItem()
            item["name"] = brickset.xpath(".//*[@data-product-param='name']/h3/text()").extract_first()
            item["price"] = brickset.xpath(".//*[@data-product-param='price']/text()").extract_first()

            yield item

            # logger.info('Parse function called on %s', response.url)
            # NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
            # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            # if next_page:
            #     yield scrapy.Request(
            #         response.urljoin(next_page),
            #         callback=self.parse
            #     )