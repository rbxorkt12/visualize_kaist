import scrapy
from inavate.items import InavateItem

class KoreabiomedSpider(scrapy.Spider):
    name = "inavate"

    def start_requests(self):
        base_url = 'https://www.inavateonthenet.net/search?indexCatalogue=search&searchQuery=kaist&wordsMode=0'
        url = base_url
        yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('//*[@class="sfsearchResultUrl"]/a/@href').extract()
        for url in url_list:
            article_url = url
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = InavateItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//article/@title').extract()[0]
        article_title = article_title.strip()
        article_data = ''.join(response.xpath('//article/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item