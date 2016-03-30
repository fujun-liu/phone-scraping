# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class CommentItem(scrapy.Item):
	name = scrapy.Field()
	location = scrapy.Field()
	time = scrapy.Field()
	comment = scrapy.Field()

class WhocalledItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    phone = scrapy.Field()
    comments = scrapy.Field() 
