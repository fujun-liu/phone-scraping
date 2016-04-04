import scrapy
from  callercomplaints.items import CallercomplaintsItem
import re
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas

class CallerComplaintsSpider(scrapy.Spider):
	name = "callercomplaints"
	allowed_domains = ["callercomplaints.com"]
	#start_urls = ['http://www.callercomplaints.com/SearchResult.aspx?Phone=888-821-8982']
	df = pd.read_csv('NpasInSvcByNumRpt.csv')
	npa = list(df['NPA'])
	npa = npa[:1]
	start_urls = ['http://www.callercomplaints.com/AreaCodeDetail.aspx?AreaCode={}'.format(area_code) for area_code in npa]

	def parse(self, response):
		# parse area main page which might contain many pages
		area_pages = response.xpath('//a[@class="pages" and contains(text(), "Page")]/@href').extract()
		for url in area_pages:
			yield scrapy.Request(url, callback=self.parse_area)

	def parse_area(self, response):
		phone_urls = response.xpath('//div[contains(@class, "report_listing_header")]/a/@href').extract()
		for url in phone_urls:
			yield scrapy.Request(url, callback=self.parse_page)

	def parse_page(self, response):
		# first test if this website is crawlable
		#filename = response.url.split('SearchResult.aspx?Phone=')[-1] + '.html'
		#with open(filename, 'wb') as f:
			#f.write(response.body)
		phone_item = CallercomplaintsItem()
			
		phone_str = response.url.split('/')[-1]
		page_id = '1'
		if re.search('&page=', phone_str):
			parts = phone_str.split('&page=')
			page_id = parts[1]
			phone_str = parts[0]	
		phone_id = phone_str.split('?Phone=')[-1]
		# remove non-digital characters, such as -, ., ( or space
		phone_id = re.sub('[^0-9]', '', phone_id)
		phone_id = phone_id + '-' + page_id
		phone_item['phone_id'] = phone_id
		phone_comments = []
		# parse each omplaint

		for tbl in response.xpath('//div[@class="tbl"]'):
			phone_comment = {}

			author_info = tbl.xpath('.//span[@class="author_info"]/text()').extract()
			if not author_info:
				continue

			author_info = author_info[0].strip()
			pos1 = author_info.find(' by ')
			pos2 = author_info.find(' at ')
			name = "unknown"
			if pos1 != -1:
				name = author_info[pos1+4:pos2].strip()
			time = author_info[pos2+4:].strip()
			phone_comment['name'] = name
			phone_comment['time'] = time
			#phone_comment['author_info'] = author_info
			text_content = tbl.xpath('.//div[@class="text_content"]')
			if not text_content:
				continue

			caller_type_sel = text_content.xpath('strong[contains(text(), "Type")]')
			caller_type = "unknown"
			if caller_type_sel:
				caller_type = caller_type_sel.xpath('following-sibling::text()').extract()
				caller_type = caller_type[0].strip()

			caller_owner_sel = text_content.xpath('strong[contains(text(), "Owner")]')
			caller_owner = "unknown"
			if caller_owner_sel:
				caller_owner = caller_owner_sel.xpath('following-sibling::text()').extract()
				caller_owner = caller_owner[0].strip()
			

			caller_report_sel = text_content.xpath('strong[contains(text(), "Report")]')
			caller_report = ''
			if caller_report_sel:
				caller_report = caller_report_sel.xpath('following-sibling::text()').extract()
				caller_report = caller_report[0].strip()

			phone_comment['caller_type'] = caller_type
			phone_comment['caller_owner'] = caller_owner
			phone_comment['caller_report'] = caller_report

			phone_comments.append(phone_comment)

		phone_item['phone_comments'] = phone_comments
		yield phone_item

		# more pages
		pages = response.xpath('//div[@class="pageBox"]/a[@class="pages"]/@href').extract()
		curr_page_id = int(page_id)
		if pages and curr_page_id < len(pages):
			yield scrapy.Request(pages[curr_page_id], callback=self.parse_page)
