# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JobparserItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    source = scrapy.Field()
    currency = scrapy.Field()
    min_salary = scrapy.Field()
    max_salary = scrapy.Field()
    company_name = scrapy.Field()
    date_posted = scrapy.Field()
    link = scrapy.Field()
    location = scrapy.Field()
    _id = scrapy.Field()
