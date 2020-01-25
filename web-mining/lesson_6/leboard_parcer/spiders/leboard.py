# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from leboard_parcer.items import LeboardParcerItem
from scrapy.loader import ItemLoader

class LeboardSpider(scrapy.Spider):
    name = 'leboard'
    allowed_domains = ['leboard.ru']
    start_urls = ['https://leboard.ru/']

    def __init__(self, section):
        super(LeboardSpider,self).__init__()
        self.start_urls = [f'https://leboard.ru/{section}']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath('//a[@class="next-positions"]/@href').extract_first()
        yield response.follow(next_page, callback=self.parse)

        ads_links = response.xpath('//div[@itemprop="itemListElement"]//a[@itemprop="url"]/@href').extract()
        for link in ads_links:
            yield response.follow(link, callback=self.parse_ads)
        pass

    def parse_ads(self, response: HtmlResponse):
        loader = ItemLoader(item=LeboardParcerItem(), response=response)
        loader.add_value('link', response.url)
        loader.add_xpath('photos', '//img[contains(@class,"post-gallery__img")]/@src')
        loader.add_xpath('title', '//h1[@class="post-view__title"]/text()')
        loader.add_xpath('price', '//span[@itemprop="price"]/@content')
        loader.add_xpath('currency', '//span[@itemprop="priceCurrency"]/@content')
        loader.add_xpath('params', '//table[@class="filtr-list"]//text()')

        yield loader.load_item()


