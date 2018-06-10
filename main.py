import logging
import scrapy
from pymongo import MongoClient

logger = logging.getLogger('mycustomlogger')

conn = MongoClient('localhost',27017)
db = conn.shop
coll = db.products
coll.remove({})

class BrickSetSpider(scrapy.Spider):
    name = 'brick_spider'

    def start_requests(self):
        urls = [
            'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open("tmp/" + filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)

        print(response)
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

            productName = brickset.xpath(".//*[@data-product-param='name']/h3/text()").extract_first()
            productPrice = brickset.xpath(".//*[@data-product-param='price']/text()").extract_first()

            coll.save({
                "name": productName,
                "price": productPrice
            })

            # logger.info('Parse function called on %s', response.url)
            # NEXT_PAGE_SELECTOR = '.next a ::attr(href)'
            # next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
            # if next_page:
            #     yield scrapy.Request(
            #         response.urljoin(next_page),
            #         callback=self.parse
            #     )