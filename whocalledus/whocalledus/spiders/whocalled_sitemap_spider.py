import scrapy
from whocalledus.items import *
import re
from scrapy.spiders import SitemapSpider

class WhoCalledSpider(SitemapSpider):
    name = "whocalled"
    allowed_domains = ["whocalled.us"]
    sitemap_urls = ["https://whocalled.us/sitemap.xml"]
    sitemap_rules = [('/lookup/[0-9]+', 'parse_lookup')]

    def parse(self, response):
        # parse the main site map
        pass

    def parse_lookup(self, response):
    	phone_item = WhocalledItem()
    	# phone id
    	phone_item['phone'] = response.url.split("/")[-1]
    	# phone comments
    	phone_item['comments'] = []
    	# get all comments
    	for comment in response.xpath('//div[contains(@id, "comment") and @class="comment"]'):
    		item = CommentItem()
    		item['comment'] = comment.xpath('.//p/text()').extract()
    		item['time'] = comment.xpath('.//span[@title]/@title').extract()
    		#print item['time']
    		item['name'] = comment.xpath('.//span[@class="commentName"]/text()').extract()
    		item['location'] = comment.xpath('.//span[@class="location"]/text()').extract()

    		phone_item['comments'].append(item)

    	#print phone_item
    	yield phone_item
