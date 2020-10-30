import scrapy
from eurekalert.items import EurekalertItem

class HeraldSpider(scrapy.Spider):
    name = "eurekalert"

    def start_requests(self):
        base_url = 'https://srch.eurekalert.org/e3/query.html?charset=iso-8859-1&pw=100.101%25&qt=kaist&st='
        for i in range(10):
            if i==0:
                url = base_url + '1'
            else:
                url = base_url + str(i) + '1'
            yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('//*[@class="title"]/a/@href').extract()
        for url in url_list:
            article_url = 'https://www.eurekalert.org/' + url.split('&')[0][43:]
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = EurekalertItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//*[@class="page_title"]/text()').extract()[0].strip()
        article_data = ''.join(response.xpath('//*[@class="entry"]/p/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item