# coding=utf-8
import datetime
import pymongo
import shop.settings


class DataBaseService(object):
    def __init__(self):
        mongo_settings = shop.settings.MONGO

        self.client = pymongo.MongoClient(mongo_settings['host'])
        self.db = self.client[mongo_settings['data_base']]
        self.collection = self.db[mongo_settings['product_collection']]

    def insert_one(self, item):
        self.collection.insert(dict(item))

    def is_exists(self, url):
        return self.collection.find({"url": url}).count() > 0

    def close(self):
        self.client.close()
