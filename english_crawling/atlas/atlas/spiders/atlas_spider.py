import scrapy
from atlas.items import AtlasItem

class AtlasSpider(scrapy.Spider):
    name = "atlas"

    def start_requests(self):
        base_url = 'https://newatlas.com/search/?q=kaist&s='
        for i in range(5):
            page_num = i + 1
            url = base_url + str(page_num)
            yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('//*[@class="PromoB-media"]/a/@href').extract()
        for url in url_list:
            article_url = url
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = AtlasItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//*[@class="ArticlePage-headline"]/text()').extract()[0]
        article_title = article_title.strip()
        article_data = ''.join(response.xpath('//*[@class="RichTextArticleBody-body RichTextBody"]/p/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item