import scrapy
from whocalledus.items import *

class WhoCalledSpider(scrapy.Spider):
    name = "whocalled"
    allowed_domains = ["whocalled.us"]
    start_urls = ["https://whocalled.us/"]

    def parse(self, response):
    	for href in response.xpath('//a[contains(@href, "lookup")]/@href'):
    		url = response.urljoin(href.extract())
    		yield scrapy.Request(url, callback=self.parse_lookup)
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

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
    		print item['time']
    		item['name'] = comment.xpath('.//span[@class="commentName"]/text()').extract()
    		item['location'] = comment.xpath('.//span[@class="location"]/text()').extract()

    		phone_item['comments'].append(item)

    	#print phone_item
    	yield phone_item
