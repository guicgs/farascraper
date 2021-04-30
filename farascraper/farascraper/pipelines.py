# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from pymongo import MongoClient
from scrapy.exceptions import NotConfigured


class FarascraperPipeline:
    collection_name = "afp_collection"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        # Pass a "db=mongo" argument if you want to save the data to a MongoBD collection
        db = getattr(crawler.spider, "db", None)
        if db == "mongo":
            return cls(
                mongo_uri=crawler.settings.get("MONGO_URI"),
                mongo_db=crawler.settings.get(
                    "MONGO_DATABASE", "afp_db"
                ),
            )
        raise NotConfigured

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
