import scrapy
from koreabiomed.items import KoreabiomedItem

class KoreabiomedSpider(scrapy.Spider):
    name = "koreabiomed"

    def start_requests(self):
        base_url = 'http://www.koreabiomed.com/news/articleList.html?page='
        search_option = '&total=38&box_idxno=&sc_area=A&view_type=sm&sc_word=kaist'
        for i in range(2):
            page_num = i + 1
            url = base_url + str(page_num) + search_option
            yield scrapy.Request(url, self.parse, dont_filter = True)

    def parse(self, response):
        url_list = response.xpath('//*[@id="section-list"]/ul/li/h4/a/@href').extract()
        for url in url_list:
            article_url = 'http://www.koreabiomed.com' + url
            yield scrapy.Request(article_url, self.parse_article, meta={'url' : article_url})
    
    def parse_article(self, response):

        item = KoreabiomedItem()
        
        article_url = response.meta['url']
        article_title = response.xpath('//*[@class="heading"]/text()').extract()[0]
        article_title = article_title.strip()
        article_data = ''.join(response.xpath('//*[@id="article-view-content-div"]/p/text()').extract())
        article_data = article_data.replace('\n', '')
        article_data = article_data.replace('\r', '')

        item['urls'] = article_url
        item['titles'] = article_title
        item['contents'] = article_data


        yield item