# coding=utf-8

from multiprocessing import Queue, Process
from scrapy.utils.project import get_project_settings

from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess

from shop.spiders.markethot_spider import MarkethotSpider
from shop.spiders.megadrop24_spider import Megadrop24Spider
from shop.spiders.yandex_spider import YandexSpider
from web.manage import runserver


class CrawlRunner:
    def __init__(self, query, history):
        self.query = query
        self.history = history

    def run_spider(self):
        def f(q, spider):
            try:
                runner = CrawlerProcess(get_project_settings())
                deferred = runner.crawl(spider, query=self.query, history=self.history)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)

        for spider in [Megadrop24Spider, MarkethotSpider]:
            q = Queue()
            p = Process(target=f, args=(q, spider))
            p.start()
            result = q.get()
            p.join()

            if result is not None:
                raise result


if __name__ == '__main__':
    runserver()