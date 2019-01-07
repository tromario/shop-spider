# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
# from elasticsearch import Elasticsearch
from scrapy.exceptions import DropItem

from shop.service.data_base_service import DataBaseService


class MongoPipeline(object):
    def __init__(self):
        self.data_base_service = DataBaseService()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.data_base_service.close()

    def process_item(self, item, spider):
        self.data_base_service.insert_one(item)
        return item

# class ESPipeline(object):
#     def __init__(self, es_settings):
#         self.es_host = es_settings['host']
#         self.es_port = es_settings['port']
#         self.es_index = es_settings['index']
#         self.es_doc_type = es_settings['doc_type']
#
#         self.settings = {
#             "settings": {
#                 "analysis": {
#                     "filter": {
#                         # "russian_stop": {
#                         #     "type":       "stop",
#                         #     "stopwords":  "_russian_"
#                         # },
#                         # "russian_stemmer": {
#                         #     "type":       "stemmer",
#                         #     "language":   "russian"
#                         # },
#                     },
#                     "analyzer": {
#                         "default": {
#                             "tokenizer": 'standard',
#                             "filter": ['lowercase']
#                         }
#                     }
#                 }
#             },
#             "mappings": {
#                 "products": {
#                     "properties": {
#                         "name": { "type": "string" },
#                         "price": { "type": "double" }
#                     }
#                 }
#             }
#         }
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             es_settings = crawler.settings.get('ELASTIC_SEARCH')
#         )
#
#     def open_spider(self, spider):
#         self.es = Elasticsearch([{'host': self.es_host, 'port': self.es_port}])
#         if self.es.indices.exists(index = self.es_index):
#             self.es.indices.delete(index = self.es_index)
#         self.es.indices.create(index=self.es_index, ignore=400, body=self.settings)
#
#     def process_item(self, item, spider):
#         self.es.index(index = self.es_index, doc_type = self.es_doc_type, body = dict(item))
#         return item


class DuplicatesPipeline(object):
    def __init__(self):
        self.data_base_service = DataBaseService()

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.data_base_service.close()

    def process_item(self, item, spider):
        if self.data_base_service.is_exists(item['url']):
            raise DropItem("Duplicate item found: %s" % item)
        else:
            return item

