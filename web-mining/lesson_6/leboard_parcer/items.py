# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, TakeFirst, MapCompose


def parse_params(value):
    dict_params = {}
    for i in range(0, len(value), 2):
        key = value[i]
        val = value[i + 1].split(' ')[1]
        if val == 'Да':
            val = True
        elif val == 'Нет':
            val = False
        else:
            try:
                val = float(val)
            except Exception:
                val = value[i + 1]
        dict_params[key] = val
    return dict_params


class LeboardParcerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    source = scrapy.Field(output_processor=TakeFirst())
    link = scrapy.Field(output_processor=TakeFirst())
    photos = scrapy.Field()
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(input_processor=MapCompose(float), output_processor=TakeFirst())
    currency = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=Compose(parse_params))
    _id = scrapy.Field()
    pass
