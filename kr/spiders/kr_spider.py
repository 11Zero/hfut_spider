# -*- coding:utf-8 -*-
from scrapy.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.http.request import Request
#from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor as sle
from scrapy.linkextractors import LinkExtractor
from kr.items import KrItem
from scrapy.exceptions import CloseSpider
from scrapy.crawler import CrawlerProcess
from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import urlparse
import scrapy


class krSpider(CrawlSpider):
    name = 'kr'
    allowed_domains = ['hfut.edu.cn']
    start_urls = ['http://news.hfut.edu.cn/list-2-1.html']

    #index = 1
    # for index in range(1,10):
    #     start_urls = backurl#['http://news.hfut.edu.cn/list-2-%(index)d.html'%{'index':index}]
    # rules = [
    #     Rule(LinkExtractor(allow=('list-2-\d+.html')), callback='parse_kr'),
    # ]


    def parse(self, response):
        urlparse.urljoin(response.url, 'http://news.hfut.edu.cn/')
        sel = Selector(response)
        this_li = sel.xpath('/html/body/div[5]/div[1]/ul/li')
        items = []
        for li in this_li:
            item = KrItem()
            item['title'] = li.xpath('./a/text()').extract()
            if len(item['title']) == 0:
                continue
            # item['author'] = site.xpath(
            #     '//div[@class="inner"]//span[@class="name"]/text()').extract()
            # item['intro_content'] = site.xpath(
            #     '//section[@class="article"]/p[1]').extract()

            url = li.xpath('./a/@href').extract()[0]

            if url[0] == '/':
                item['url'] = 'http://news.hfut.edu.cn' + url
            else:
                item['url'] = url
            item['pub_date'] = li.xpath('./span/text()').extract()
            if item is not None:
                yield item
                #items.append(item)
                # print items


        nexturl = 'http://news.hfut.edu.cn/' + sel.xpath('//*[@id="pages"]/a[13]/@href').extract()[0]


        #next_href = response.xpath('//li[@class="next"]/a/@href').extract_first()
        # 判断next_page的值是否存在
        if nexturl is not None:
            # 如果下一页属性值存在，则通过urljoin函数组合下一页的url:
            # www.quotes.toscrape.com/page/2
            next_page = response.urljoin(nexturl)
            # 回调parse处理下一页的url
            yield scrapy.Request(next_page, callback=self.parse)


# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# process.crawl(krSpider)
# process.start() # the script will block here until the crawling is finished
