# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import re
import logging
from scrapy.contrib.pipeline.images import ImagesPipeline
from scrapy.exceptions import DropItem
from scrapy.http import Request

logger = logging.getLogger('mylogger')
logger.setLevel(logging.DEBUG)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console.setFormatter(formatter)
logger.addHandler(console)


# 数据处理
class MoviePipeline(object):
    # year_pattern = re.compile(r'\((\d+)\)')
    # name_pattern = re.compile(r'(.*)\(')

    def __init__(self):
        client = MongoClient()
        # db = client.movie_db
        self.movie_doc_collection = client.movie_db.movie_doc

    def process_item(self, item, spider):

        if not self.movie_doc_collection.find({'mtime_url': item['mtime_url']}).count():
            logger.info("insert the movie into db")

            result = self.movie_doc_collection.insert_one(
                {"movie": item['movie_name'],"enname": item['movie_enname'],
                 "type": item['movie_type'],"rate": item['movie_rate'],
                 "director": item['movie_director'],'year': item['movie_year'],
                 "country": item['movie_country'],'mtime_url': item['mtime_url']})
            logger.info(result.inserted_id)
        else:
            logger.info("movie:{0} is existing in db, jump it".format(item['mtime_url']))
        return item


# 图片处理
class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            yield Request(image_url)

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        return item

