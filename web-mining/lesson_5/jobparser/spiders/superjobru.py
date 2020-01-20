# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SjruSpider(scrapy.Spider):
    name = 'superjobru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=python&geo%5Bc%5D%5B0%5D=1']

    def parse(self, response: HtmlResponse):
        next_page = response.xpath("//a[@rel='next']/@href").extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css('a._1QIBo::attr(href)').extract()

        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse, cb_kwargs=dict(link=link))

    def vacansy_parse(self, response: HtmlResponse, link):
        name = response.xpath("//h1[@class='_3mfro rFbjy s1nFK _2JVkc']/text()").extract_first()
        location = response.xpath("//span[@class='_3mfro _1hP6a _2JVkc']/text()").extract_first()
        currency = response.xpath("//span[@class='_3mfro _2Wp8I ZON4b PlM3e _2JVkc']//text()").extract()

        date_posted = response.xpath("//div[@class='f-test-title _183s9 _3wZVt OuDXD _1iZ5S']"
                                     "/div[2]/span/text()").extract_first()
        company_name = response.xpath("//h2[@class='_3mfro PlM3e _2JVkc _2VHxz _3LJqf _15msI']/text()").extract_first()

        yield JobparserItem(location=location, currency=currency, link=link, date_posted=date_posted,
                            company_name=company_name, name=name)
