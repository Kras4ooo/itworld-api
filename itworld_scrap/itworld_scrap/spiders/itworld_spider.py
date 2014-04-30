from scrapy.spider import Spider
from scrapy.selector import Selector
from scrapy.http import Request

class ItworldSpider(Spider):
    name = "itworld"
    allowed_domains = ["itworld.com"]
    start_urls = [
        "http://www.itworld.com/news"
    ]

    def __init__(self):
        self.link = 'http://www.itworld.com'

    def parse(self, response):
        """ Only first page """
        sel = Selector(response)
        titles_links = sel.xpath('//*[@id="left-col"]/div/div/ul/li/div/h3/a/@href').extract()
        for link in titles_links:
            yield Request(self.link+link, callback=self.info_new)

    def info_new(self, response):
        sel = Selector(response)
        title = sel.xpath('//*[@id="article-title"]/text()').extract()
        author = sel.xpath('//*[@id="article-info"]//text()').extract()
        content = sel.xpath('//*[@id="article-content"]//text()').extract()
        post_date = sel.xpath('//*[@id="article-content"]/p[1]/span/strong/text()').extract()