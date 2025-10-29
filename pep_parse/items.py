# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PepParseItem(scrapy.Item):
    # номер PEP (например, 8)
    number = scrapy.Field()
    # название PEP (например, The Style Guide for Python Code)
    name = scrapy.Field()
    # статус PEP (например, Final)
    status = scrapy.Field()
