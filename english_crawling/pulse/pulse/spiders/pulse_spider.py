import scrapy
from pulse.items import PulseItem

class PulseSpider(scrapy.Spider):
    name = "pulse"

    def start_requests(self):
        base_url = 'https://pulsenews.co.kr/search.php?schKeyword=kaist&page='
        for i in range(5):
            page_num = i
            url = base_url + str(page_num)
            yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('//*[@class="article"]/ul/li/p/a/@href').extract()
        for url in url_list:
            article_url = 'https:' + url
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = PulseItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//*[@id="s_view_top"]/h2/text()').extract()[0]
        article_title = article_title.strip()
        article_data = ''.join(response.xpath('//*[@class="art_txt"]/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item