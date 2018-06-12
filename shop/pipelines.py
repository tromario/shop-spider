# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from elasticsearch import Elasticsearch

class MongoPipeline(object):
    collection_name = 'products'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DATABASE', 'shop')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[self.collection_name].remove({})

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

class ESPipeline(object):
    def __init__(self, es_settings):
        self.es_host = es_settings['host']
        self.es_port = es_settings['port']
        self.es_index = es_settings['index']
        self.es_doc_type = es_settings['doc_type']

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            es_settings = crawler.settings.get('ELASTIC_SEARCH')
        )

    def open_spider(self, spider):
        self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
        if self.es.indices.exists(index = self.es_index):
            self.es.indices.delete(index = self.es_index)

    def process_item(self, item, spider):
        self.es.index(index = self.es_index, doc_type = self.es_doc_type, body = dict(item))
        return item