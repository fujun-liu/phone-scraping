import scrapy

class Notes800Spider(scrapy.Spider):
    name = "notes800"
    allowed_domains = ["whocalled.us"]
    start_urls = ["https://whocalled.us/"]

    def parse(self, response):
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)