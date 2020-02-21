# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
import datetime
from main.mongo.ptt_data import PttData
from main.redis_tool.redis_conn import RedisConn
import os
from dotenv import load_dotenv
load_dotenv()


class PttcrawlerPipeline(object):

    def __init__(self):
        self.ptt_data = PttData()
        self.redis_conn = RedisConn(os.getenv("REDIS_HOST"), os.getenv("REDIS_PORT"), os.getenv("REDIS_ERROR_DB"))

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        self.ptt_data.close()

    def process_item(self, item, spider):

        url = item.get('canonicalUrl')

        if item.get('authorId') is None:
            self.redis_conn.set(url)
            return item

        _id = item.get('_id')

        if self.ptt_data.select(_id):
            return item

        data = {
            '_id': item.get('_id'),
            'authorId': item.get('authorId'),
            'authorName': item.get('authorName'),
            'title': item.get('title'),
            'publishedTime': item.get('publishedTime'),
            'content': item.get('content'),
            'canonicalUrl': url,
            'createTime': datetime.datetime.utcnow(),
            'updateTime': datetime.datetime.utcnow(),
            'commentId': item.get('commentId'),
            'commentContent': item.get('commentContent'),
            'commentTime': item.get('commentTime'),
        }
        self.ptt_data.insert(data)

        return item
