# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from scrapy.exception import DropItem
import codecs
import json
from datetime import datetime
from hashlib import md5
from scrapy import log
from twisted.enterprise import adbapi


class JsonWriterPipeline(object):

    def __init__(self):
        self.file = codecs.open('ans.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False) + "\r\n"
        self.file.write(line)
        return item

    def spider_closed(self, spider):
        self.file.close()

        #file = codecs.open('ans.json', 'wb', encoding='utf-8')


class KrPipeline(object):

    def process_item(self, item, spider):
        return item


# class MySQLStorePipeline(object):
#     """A pipeline to store the item in a MySQL database.
#
#     This implementation uses Twisted's asynchronous database API.
#     """
#
#     def __init__(self, dbpool):
#         self.dbpool = dbpool
#
#     @classmethod
#     def from_settings(cls, settings):
#         dbargs = dict(
#             host=settings['MYSQL_HOST'],
#             db=settings['MYSQL_DBNAME'],
#             user=settings['MYSQL_USER'],
#             passwd=settings['MYSQL_PASSWD'],
#             charset='utf8',
#             use_unicode=True,
#         )
#         dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
#         return cls(dbpool)
#
#     def process_item(self, item, spider):
#         # run db query in the thread pool
#         d = self.dbpool.runInteraction(self._do_upsert, item, spider)
#         d.addErrback(self._handle_error, item, spider)
#         # at the end return the item in case of success or failure
#         d.addBoth(lambda _: item)
#         # return the deferred instead the item. This makes the engine to
#         # process next item (according to CONCURRENT_ITEMS setting) after this
#         # operation (deferred) has finished.
#         return d
#
#     def _do_upsert(self, conn, item, spider):
#         """Perform an insert or update."""
#         guid = self._get_guid(item)
#         now = datetime.utcnow().replace(microsecond=0).isoformat(' ')
#
#         conn.execute("""SELECT EXISTS(
#             SELECT 1 FROM kr WHERE guid = %s
#         )""", (guid, ))
#         ret = conn.fetchone()[0]
#
#         if ret:
#             conn.execute("""
#                 UPDATE kr
#                 SET title=%s, author=%s,link=%s,reply_count=%s
#                 WHERE guid=%s
#             """, (item['title'], item['author'], item['link'], item['reply_count'], guid))
#             spider.log("Item updated in db: %s %r" % (guid, item))
#         else:
#             conn.execute("""
#                 INSERT INTO kr (guid,product_url,image_url)
#                 VALUES (%s,%s,%s)
#             """, (guid, item['product_url'], item['image_url']))
#             spider.log("Item stored in db: %s %r" % (guid, item))
#
#     def _handle_error(self, failure, item, spider):
#         """Handle occurred on db interaction."""
#         # do nothing, just log
#         log.err(failure)
#
#     def _get_guid(self, item):
#         """Generates an unique identifier for a given item."""
#         # hash based solely in the url field
#         return md5(item['product_url']).hexdigest()
