import scrapy
from herald.items import HeraldItem

class HeraldSpider(scrapy.Spider):
    name = "herald"

    def start_requests(self):
        base_url = 'http://www.koreaherald.com/search/index.php?q=kaist&sort=1&mode=list&np='
        for i in range(11):
            if i>9:
                main_page = 2
            else:
                main_page = 1
            page_num = i+1
            url = base_url + str(page_num) + '&mp=' + str(main_page)
            yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('/html/body/div[3]/div/div[2]/ul/li/a/@href').extract()
        for url in url_list:
            article_url = 'http://www.koreaherald.com' + url
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = HeraldItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//*[@class="view_tit"]/text()').extract()[0]
        article_data = ''.join(response.xpath('//*[@class="view_con_t"]/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item