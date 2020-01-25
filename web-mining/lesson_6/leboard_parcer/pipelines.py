# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import datetime
import hashlib
from scrapy.utils.python import to_bytes


class PrepareDataPipeline(object):
    def process_item(self, item, spider):

        item['source'] = spider.name
        item['_id'] = hashlib.sha1(to_bytes(item['link'])).hexdigest()

        return item


class LeboardPhotosPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        self.title = item['title'] #костыль, плохо умею в ооп, не разобрался как к объекту LeboardParcerItem обратиться
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item

    def file_path(self, request, response=None, info=None):
        today = datetime.datetime.utcnow().date().isoformat()
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{today}/{self.title}/{image_guid}.jpg'


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.ads

    def process_item(self, item, spider):
        collection = self.mongo_base[spider.name]
        try:
            collection.insert_one(item)
        except DuplicateKeyError:
            pass
        return item
