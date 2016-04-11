import scrapy
import re

class CallerComplaintsSpider(scrapy.Spider):
	name = "callferret"
	allowed_domains = ["callferret.com"]
	start_urls = ['http://www.callferret.com/area-codes']

	def parse(self, response):
		filename = response.url.split('/')[-1] + '.html'
		with open(filename, 'wb') as f:
			f.write(response.body)
