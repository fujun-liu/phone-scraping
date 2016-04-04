# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CallercomplaintsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone_id = scrapy.Field()
    phone_comments = scrapy.Field()
