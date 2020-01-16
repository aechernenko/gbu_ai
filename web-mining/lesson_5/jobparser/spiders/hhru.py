# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem

class HhruSpider(scrapy.Spider):
    name = 'hhru'
    allowed_domains = ['hh.ru']
    start_urls = ['https://sergievposad.hh.ru/search/vacancy?L_save_area=true&clusters=true&enable_snippets=true&text='
                  'Python&showClusters=true']

    def parse(self, response: HtmlResponse):
        next_page = response.css('a.HH-Pager-Controls-Next::attr(href)').extract_first()
        yield response.follow(next_page, callback=self.parse)

        vacansy = response.css('div.vacancy-serp div.vacancy-serp-item div.vacancy-'
                               'serp-item__row_header a.bloko-link::attr(href)').extract()



        for link in vacansy:
            yield response.follow(link, callback=self.vacansy_parse, cb_kwargs=dict(link=link))

    def vacansy_parse(self, response: HtmlResponse, link):
        name = response.xpath("//h1[@class='header']/descendant-or-self	::*/text()").extract_first()
        location = response.xpath("//div[contains(@class, 'vacancy-company')]/p//text()").extract()

        def meta(itemprop):
            return response.xpath(f"//meta[contains(@itemprop,'{itemprop}')]/@content").extract_first()

        currency = meta('currency')
        min_salary = meta('minValue')
        max_salary = meta('maxValue')
        date_posted = meta('datePosted')
        company_name = meta('name')

        yield JobparserItem(location=location, currency=currency, min_salary=min_salary, link=link,
                            max_salary=max_salary, date_posted=date_posted, company_name=company_name, name=name)
