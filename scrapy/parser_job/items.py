# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ParserJobItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    salary_from = scrapy.Field()
    salary_to = scrapy.Field()
    currency = scrapy.Field()
    _id = scrapy.Field()
