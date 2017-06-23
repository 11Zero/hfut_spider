# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class KrItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # product_url = Field()
    # image_url = Field()
    title = Field()
    url = Field()
    # author = Field()
    # intro_content = Field()
    pub_date = Field()

'''
create table kr(
	 guid CHAR(32) PRIMARY KEY,
     product_url TEXT,
     image_url TEXT) DEFAULT CHARSET=utf8;
     '''
