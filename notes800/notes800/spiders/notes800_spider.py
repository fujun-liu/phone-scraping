import scrapy
from notes800.items import Notes800Item 
from pandas import DataFrame, read_csv
import pandas as pd #this is how I usually import pandas
class Notes800Spider(scrapy.Spider):
    name = "notes800"
    allowed_domains = ["800notes.com"]
    start_urls = ['http://800notes.com/Phone.aspx/1-315-636-0147']

    #df = pd.read_csv('NpasInSvcByNumRpt.csv')
    #npa = list(df['NPA'])
    #npa = npa[:2]
    url_home = 'http://800notes.com'
    #url_area = 'http://800notes.com/AreaCode.aspx'
    #start_urls = ['{}/1-{}'.format(url_area, area_code) for area_code in npa]

    # this is for start_urls
    def parse_test(self, response):
    	# extract phone list for this page
    	phone_list = response.xpath('//div[@class="numberList"]/a/@href').extract()
    	phone_urls = ['{}/{}'.format(url_home, phone_id) for phone_id in phone_list]
        for phone_url in phone_urls:
        	yield scrapy.Request(phone_url, callback=self.parse_phone_url)

        # This next area code?
        area_next = response.xpath('//div[@id="pager" and @class="oos_pager"]/a[text()="Next"]')
        if area_next:
        	# in case pages put two next buttons (top and bottom)
        	area_next_url = '{}/{}'.format(url_home, area_next.xpath('@href').extract_first())
        	# use parse call back which is default
        	yield scrapy.Request(area_next_url)

    # this will only parse phone list and yield request for each phone
    def parse(self, response):
    	filename = response.url.split('/')[-1] + '.html'
    	with open(filename, 'wb') as f:
    		f.write(response.body)

        return
    	# this phone might have multiple comments
    	phone_item = Notes800Item()
    	tmp = response.url.split('/')
    	phone_id = tmp[-1]
    	if "-" not in tmp[-1]:
    		phone_id = tmp[-2] + '-' + tmp[-1]

    	phone_item['phone_id'] = phone_id
    	phone_comments = []
    	for contlet in response.xpath('//div[@class="oos_contlet"]'):
    		phone_comment = {}
    		# id of this message
    		phone_comment['cont_id'] = contlet.xpath('@id').extract()
    		phone_comment['cont_body'] = contlet.xpath('.//div[@class="contletBody"]/text()').extract()
    		phone_comment['cont_name'] = contlet.xpath('.//span[@class="oos_pd"]/text()').extract()
    		# is this a reply to someone
    		cont_reply_to_id = None
    		reply_to = contlet.xpath('.//a[contains(@href, "#p")]')
    		if reply_to:
    			cont_reply_to_id = reply_to.xpath('@href').extract()[2:]
    		phone_comment['cont_reply_to_id'] = cont_reply_to_id
    			
    		time_sel = contlet.xpath('.//time')
    		phone_comment['cont_time'] = time_sel.xpath('@datatime').extract()
    		
    		replies_str = re.search(' [0-9]+ replies', time_sel.xpath('../text()').extract())
    		cont_num_replies = 0
    		if replies_str:
    			cont_num_replies = int(replies_str.strip().split[0])

    		phone_comment['cont_num_replies'] = cont_num_replies
    		phone_comments.append(phone_comment)

    	phone_item['phone_comments'] = phone_comments
    	yield phone_item
    		

    	# check if there are more pages of comment
    	next_page = response.xpath('//div[@class="oos_pager"]/a[text()="Next"]')
    	if next_page:
    		next_url = '{}/{}'.format(url_home, next_page.xpath('@href').extract_first())
    		yield scrapy.Request(next_url, callback=self.parse)		
