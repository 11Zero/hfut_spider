# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#from scrapy.exception import DropItem
import codecs
import json
import xlwt
from collections import OrderedDict
from openpyxl import Workbook
from scrapy import signals
from scrapy.contrib.exporter import CsvItemExporter
from pyexcel_xls import get_data
from pyexcel_xls import save_data
from datetime import datetime
from hashlib import md5

from twisted.enterprise import adbapi


class JsonWriterPipeline(object):
    wb = Workbook()
    ws = wb.active
    ws.append(['time', 'title', 'url'])  # 设置表头

    # data = OrderedDict()
    # sheet_1 = []
    # row_1_data = [u"time", u"title", u"url"]  # 每一行的数据
    # table = data.add_sheet('name',cell_overwrite_ok=True)
    # def __init__(self):
    #     self.file = Workbook()
    #     self.file.active.append(['time', 'title', 'url'])  # 设置表头
        # self.ws.append(['time', 'title', 'url'])  # 设置表头
        # self.sheet_1.append(self.row_1_data)
        # self.file = codecs.open('ans.json', 'wb', encoding='utf-8')

    def process_item(self, item, spider):
        line = [item['pub_date'], item['title'], item['url']]
        self.ws.append(line)
        # self.wb.save('f.xlsx')
        # print line
        # self.file.active.append(line)  # 将数据以行的形式添加到xlsx中
        # self.file.save('test.xlsx')  # 保存xlsx文件
        # line = json.dumps(dict(item), ensure_ascii=False) + "\r\n"
        # self.file.write(line)
        # row_data = [item['pub_date'],item['title'],item['url']]
        # self.sheet_1.append(row_data)
        # self.data.update({u"表1": self.sheet_1})
        return item

    # def spider_closed(self, spider):
        self.file.save('test.xlsx')
        # self.file.close()
        # self.data.save('test.xls')

        #file = codecs.open('ans.json', 'wb', encoding='utf-8')


class KrPipeline(object):
    # @classmethod
    def __init__(self):
        self.file = open('output.csv', 'w+b')
        self.exporter = CsvItemExporter(self.file)

    def spider_opened(self, spider):
        self.exporter.start_exporting()

    def spider_closed(self, spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item
    # def process_item(self, item, spider):
    #     return item


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
